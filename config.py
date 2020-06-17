import threading

global downloaded_songs
global downloaded_songs_lock 

def init_globals():
    global downloaded_songs
    global downloaded_songs_lock 
    downloaded_songs_lock = threading.Lock()
    downloaded_songs = 0