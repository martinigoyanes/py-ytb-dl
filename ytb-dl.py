import time, threading, spotify, song as songlib
from googleapiclient.discovery import build

def json_to_song_list(json_data):
    song_list = []
    for item in json_data['items']:
        song_name = item['track']['name']
        song_artists = []
        for artist in item['track']['artists']:
            song_artists.append(artist['name'])
        song = songlib.Song(name=song_name,video_url='',artists=song_artists)
        song_list.append(song)
    return song_list    

def read_ytb_key(file, keynum):
    cnt = 0
    with open('./'+file) as fp:
        while cnt < keynum:
            key = fp.readline()
            cnt += 1
    return key
    
#! Store keys in file which doesnt go to github so my keys are not stolen 
# Use 1st key first time, and if we need to download more stuff change keynum to 2 so we use the second key
ytb_key = read_ytb_key('keys.txt', keynum=1)
youtube = build('youtube', 'v3', developerKey=ytb_key)

client_id = 'c6c3f6355e3349ce8160f0f2504e442b'
client_secret = '2da4af43872a462ab652f579aa4b9d04'

spoti = spotify.Spotify(client_id,client_secret)
spoti.get_auth_code()
spoti.get_tokens()
saved_tracks = spoti.get_tracks_json(limit=10)

song_list = json_to_song_list(saved_tracks)

# Launch thread for each song that searches the song and downloads it into mp3 file
for song in song_list:
    song_thread = threading.Thread(target=song.thread_handler, args=(youtube,))
    song_thread.start()

# TODO: Keep track of how many threads/songs pending to end/download
num_threads_prev = threading.active_count()
while True:
    num_threads = threading.active_count() 
    if num_threads == 1:
        print("Finished downloading " + str(len(song_list)) + " songs")
        break
    if num_threads != num_threads_prev: 
        num_threads_prev = threading.active_count() 
        print( "[" + str(num_threads - 1) + "/" + str(len(song_list)) + "]" + " songs downloading....")
