import song as Song
import config
import time
import threading


def read_ytb_key(file, keynum):
    cnt = 0
    with open('./'+file) as fp:
        while cnt < keynum:
            key = fp.readline()[:-1]
            cnt += 1
    return key


def json_to_song_list(json_data, last_song, song_list):
    finished = False
    for item in json_data['items']:
        song_name = item['track']['name']
        song_artists = []
        for artist in item['track']['artists']:
            song_artists.append(artist['name'])
        song_cover = item['track']['album']['images'][1]['url']
        song_album = item['track']['album']['name']
        song = Song.Song(name=song_name, video_url='', artists=song_artists, cover=song_cover, album=song_album)
        song_list.append(song)
        # Last song to download inclusively
        if song_name in last_song:
            finished = True
            break

    return finished


# * Pull song untill desired (inclusively) song from SPOTI
def pull_user_songs(last_song):
    finished = False
    limit = 20
    offset = 0
    song_list = []
    while finished is False:
        spoti_saved_tracks = config.spoti.get_tracks_json(limit=limit, offset=offset)
        finished = json_to_song_list(spoti_saved_tracks, last_song, song_list)
        offset += 20
    return song_list

def download_songs(song_list,verbose=False):
    #* Launch thread for each song that searches the song and downloads it into mp3 file
    threads = []
    for song in song_list:
        #* Only try to download a song if it has not been downloaded yet
        if song.downloaded is False:
            with config.downloaded_songs_lock:
                song.thread = threading.Thread(target=song.thread_handler, args=(len(song_list), verbose))
                song.thread.start()
                threads.append(song.thread)

            #* If number of songs we are trying to download is more than 25 we need to split the calls so we dont overflow the sockets
            if len(threads) == 10 and len(song_list) > 10:
                with config.started_songs_lock:
                    diff = len(song_list) - config.started_songs < 10
                    left = diff if diff else 10
                    print("\n\n\n [" + str(config.started_songs) + "/" + str(len(song_list)) + "]"
                          + " songs started to download.\n Waiting untill they are done to start downloading the following "
                          + str(left) + " ones \n\n\n")
                for thread in threads:
                    thread.join()
                
                threads.clear()
                #* Sleep for 5 s untill we launch the next songs
                # time.sleep(5)
