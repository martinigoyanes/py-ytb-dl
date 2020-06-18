import song as Song


def read_ytb_key(file, keynum):
    cnt = 0
    with open('./'+file) as fp:
        while cnt < keynum:
            key = fp.readline()
            cnt += 1
    return key


def json_to_song_list(json_data, last_song, song_list):
    finished = False
    for item in json_data['items']:
        song_name = item['track']['name']
        song_artists = []
        for artist in item['track']['artists']:
            song_artists.append(artist['name'])
        song = Song.Song(name=song_name, video_url='', artists=song_artists)
        song_list.append(song)
        # Last song to download inclusively
        if song_name in last_song:
            finished = True
            break

    return finished


# * Pull song untill desired (inclusively) song from SPOTI
def pull_user_songs(last_song, spoti):
    finished = False
    limit = 20
    offset = 0
    song_list = []
    while finished is False:
        spoti_saved_tracks = spoti.get_tracks_json(limit=limit, offset=offset)
        finished = json_to_song_list(spoti_saved_tracks, last_song, song_list)
        offset += 20
    return song_list
