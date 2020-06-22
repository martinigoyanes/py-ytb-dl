import threading
import helper
import os
from googleapiclient.discovery import build

global downloaded_songs, downloaded_songs_lock, started_songs, started_songs_lock, error_file_lock, url_file_lock, youtube, client_id, client_secret


def init_globals(keynum):
    global downloaded_songs, downloaded_songs_lock,started_songs, started_songs_lock, error_file_lock, url_file_lock, youtube, client_id, client_secret

    downloaded_songs_lock = threading.Lock()
    started_songs_lock = threading.Lock()
    error_file_lock = threading.Lock()
    url_file_lock = threading.Lock()
    downloaded_songs = 0
    started_songs = 0
    client_id = 'c6c3f6355e3349ce8160f0f2504e442b'
    client_secret = '2da4af43872a462ab652f579aa4b9d04'

    #! Store keys in file which doesnt go to github so my keys are not stolen
    # Use 1st key first time, and if we need to download more stuff change keynum to 2 so we use the second key
    ytb_key = helper.read_ytb_key('keys.txt', keynum=keynum)
    youtube = build('youtube', 'v3', developerKey=ytb_key)

    # * Delete failed_songs file and if exist at the beginning
    if os.path.exists('failed_songs.txt'):
        os.remove('failed_songs.txt')
