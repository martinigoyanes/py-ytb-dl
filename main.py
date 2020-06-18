import time, concurrent.futures, threading, config, spotify, song as songlib
from googleapiclient.discovery import build

def json_to_song_list(json_data,last_song,song_list):
    finished = False
    for item in json_data['items']:
        song_name = item['track']['name']
        song_artists = []
        for artist in item['track']['artists']:
            song_artists.append(artist['name'])
        song = songlib.Song(name=song_name,video_url='',artists=song_artists)
        song_list.append(song)
        # Last song to download inclusively 
        if song_name in last_song:
            finished = True
            break
        
    return finished    

def read_ytb_key(file, keynum):
    cnt = 0
    with open('./'+file) as fp:
        while cnt < keynum:
            key = fp.readline()
            cnt += 1
    return key
    
def pull_user_songs(last_song):    #* Pull song untill desired (inclusively) song from SPOTI
    finished = False
    limit = 20
    offset = 0
    song_list = []
    while finished is False:
        spoti_saved_tracks = spoti.get_tracks_json(limit=limit, offset=offset)
        finished = json_to_song_list(spoti_saved_tracks, last_song, song_list)
        offset += 20    
    return song_list
    
# TODO: Get album data to have covers
# TODO: Add graphical interface
# TODO: Doesnt download all the songs if you do of the range of 100 songs (socket timeouts?)
        #? Idea to solve this issue ^ , when ever there is an error downloading song, write song name
        #? to disk so after program runs we can go and get them

config.init_globals()
client_id = 'c6c3f6355e3349ce8160f0f2504e442b'
client_secret = '2da4af43872a462ab652f579aa4b9d04'

#! Store keys in file which doesnt go to github so my keys are not stolen 
# Use 1st key first time, and if we need to download more stuff change keynum to 2 so we use the second key
ytb_key = read_ytb_key('keys.txt', keynum=1)
youtube = build('youtube', 'v3', developerKey=ytb_key)

spoti = spotify.Spotify(client_id,client_secret)
spoti.get_auth_code()
spoti.get_tokens()

last_song = input('What is the last song (inclusive) from your library to download?\n')
song_list = pull_user_songs(last_song)

#* Launch thread for each song that searches the song and downloads it into mp3 file
cnt = 0
downloaded_songs = 0
for song in song_list:
    cnt =+ 1
    config.downloaded_songs_lock.acquire() 
    song_thread = threading.Thread(target=song.thread_handler, args=(youtube, len(song_list)))
    config.downloaded_songs_lock.release()
    song_thread.start() 
    #! This sleep does not work
    #* If number of songs we are trying to download is more than 25 we need to split the calls so we dont overflow the sockets
    if cnt == 15 and len(song_list) > 20:
        cnt = 0
        #* Sleep for 15 s untill we launch the next songs
        print("\n\n\n 15 songs downloaded \n\n\n")
        time.sleep(15)
    
        


