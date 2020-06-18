import time, helper, threading, config, spotify, song as Song
# TODO: Get album data to have covers
# TODO: Add graphical interface
# TODO: Doesnt download all the songs if you do of the range of 100 songs (socket timeouts?)
        #? Idea to solve this issue ^ , when ever there is an error downloading song, write song name
        #? to disk so after program runs we can go and get them
# TODO: Automatically run behind the scenes and download the new songs u add to spoti

#* Use 1st key first time, and if we need to download more stuff change keynum to 2 so we use the second key
config.init_globals(keynum=1)

spoti = spotify.Spotify(config.client_id,config.client_secret)
spoti.get_auth_code()
spoti.get_tokens()

# last_song = input('What is the last song (inclusive) from your library to download?\n')
# song_list = helper.pull_user_songs(last_song, spoti)

### For testing with the url set i have
###################################
song_list = []
with open('video_urls.txt') as fp:
    for _ in range(97):
        url = fp.readline()[:-1]
        song = Song.Song('',[url],'')
        song_list.append(song)
###################################

#* Launch thread for each song that searches the song and downloads it into mp3 file
launched_threads = 0
for song in song_list:
    launched_threads =+ 1
    with config.downloaded_songs_lock:
        song_thread = threading.Thread(target=song.thread_handler, args=(len(song_list),))
        song_thread.start() 

    #! This sleep does not work
    #* If number of songs we are trying to download is more than 25 we need to split the calls so we dont overflow the sockets
    if launched_threads == 15 and len(song_list) > 20:
        launched_threads = 0
        #* Sleep for 15 s untill we launch the next songs
        print("\n\n\n 15 songs downloaded \n\n\n")
        time.sleep(15)



    
        


