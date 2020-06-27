import spotify
import config
import helper



def connect_spotify():
    # Get spotify credentials through OAuth 2.0
    config.spoti.get_auth_code()
    config.spoti.get_tokens()

def setup():
    #! Use 1st key first time, and if we need to download more stuff change keynum to 2 or 3 so we use the second key
    config.init_globals(keynum=1)

def start_download(last_song):
    song_list = helper.pull_user_songs(last_song)
    # song_list = helper.pull_songs_from_file()

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
                    error_file.write(
                        f'{song.name} %% {song.artists} %% {song.video_url}\n')
            song.thread.join()
