import spotify, song as songlib

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

video_url = ['https://www.youtube.com/watch?v=oNg3M9IJJlY']



client_id = 'c6c3f6355e3349ce8160f0f2504e442b'
client_secret = '2da4af43872a462ab652f579aa4b9d04'

spoti = spotify.Spotify(client_id,client_secret)
spoti.get_auth_code()
spoti.get_tokens()
saved_tracks = spoti.get_tracks_json(limit=50)

song_list = json_to_song_list(saved_tracks)
print('hola')