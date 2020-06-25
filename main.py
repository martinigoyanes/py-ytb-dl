import time, helper, threading, config, spotify, song as Song
# TODO: Add graphical interface
# TODO: Automatically run behind the scenes and download the new songs u add to spoti

#! Use 1st key first time, and if we need to download more stuff change keynum to 2 or 3 so we use the second key
config.init_globals(keynum=2)


last_song = input('What is the last song (inclusive) from your library to download?\n')
song_list = helper.pull_user_songs(last_song)

# Keep downloading untill all of the songs are downloaded
# If all songs have been downloaded just quit
# Launch all threads to start downloading each song
# Wait for all launched threads to quit before retrying to download any song
# If there is any error write the problematic song name %% artist %% videourl to file
while True:
    with config.downloaded_songs_lock:
        if config.downloaded_songs == len(song_list):
            break
    helper.download_songs(song_list) 
    for song in song_list:
        if config.DEBUGG and song.failed:
            with config.error_file_lock and open('failed_songs.txt', 'a+') as error_file:
                error_file.write(f'{song.name} %% {song.artists} %% {song.video_url}\n')       
        song.thread.join()



## For testing with the url set i have
##################################
# song_list = []
# with open('video_urls.txt') as fp:
#     for _ in range(42):
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
#         # Parsing album name
#         song_album = song_data[2]
#         # Parsing album cover url
#         song_cover = song_data[3]
#         # Parsing url data
#         url = [song_data[4][2:-2]] 
#         song = Song.Song(song_name,url,artists,song_cover,song_album)
#         song_list.append(song)
##################################



    
        


