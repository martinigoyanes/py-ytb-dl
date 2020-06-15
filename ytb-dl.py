import spotify, song

def json_to_song_list(json_data):
    song_list = []
    index = 0
    for item in json_data['items']:
        song_name = json_data['items'][index]['name']
        song_artist = json_data['items'][index]['artists'][0]['name']
        song = song.Song(name=song_name,video_url='',artist=song_artist)
        song_list.append(song)
        index += 1
        

video_url = ['https://www.youtube.com/watch?v=oNg3M9IJJlY']



client_id = 'c6c3f6355e3349ce8160f0f2504e442b'
client_secret = '2da4af43872a462ab652f579aa4b9d04'

spoti = spotify.Spotify(client_id,client_secret)
spoti.get_auth_code()
spoti.get_tokens()
json = spoti.get_tracks_json()
print('hola')