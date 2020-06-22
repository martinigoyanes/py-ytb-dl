import time, helper, threading, config, spotify, song as Song
# TODO: Get album data to have covers
# TODO: Add graphical interface
# TODO: Parse the verbose option correctly
# TODO: Automatically run behind the scenes and download the new songs u add to spoti

#* Use 1st key first time, and if we need to download more stuff change keynum to 2 so we use the second key
config.init_globals(keynum=2)
verbose = False

spoti = spotify.Spotify(config.client_id,config.client_secret)
spoti.get_auth_code()
spoti.get_tokens()

last_song = input('What is the last song (inclusive) from your library to download?\n')
song_list = helper.pull_user_songs(last_song, spoti)

## For testing with the url set i have
##################################
# song_list = []
# with open('video_urls.txt') as fp:
#     for _ in range(98):
#         song_data = fp.readline()[:-1].split(' %% ')
#         # Parsing song name
#         song_name = song_data[0]
#         # Parsing artists data 
#         artists = song_data[1][1:-1]
#         artists = artists.split(',')
#         index = 0 
#         for i in range(len(artists)):
#             if index == 0:
#                 artists[i] = artists[i][1:-1]
#             else:
#                 artists[i] = artists[i][2:-1]
#             index += 1
#         # Parsing url data
#         url = [song_data[2][2:-2]] 
#         song = Song.Song(song_name,url,artists,None,None)
#         song_list.append(song)
##################################
#* Download untill all of the songs are downloaded
while True:
    #* If all songs have been downloaded just quit
    with config.downloaded_songs_lock:
        if config.downloaded_songs == len(song_list):
            break
    #* Launch all threads to start downloading each song
    helper.download_songs(song_list, verbose=verbose)

    #* Wait for all launched threads to quit before retrying to download any song
    for song in song_list:
        song.thread.join()



    
        


