import threading
import helper
import os
import spotify

from googleapiclient.discovery import build

downloaded_songs= 0
downloaded_songs_lock= None
started_songs= None
started_songs_lock= None
error_file_lock= None
url_file_lock= None
youtube= None
youtube_lock= None 
client_id= None
client_secret= None
spoti = None
longsongs_file_lock = None
song_list_len = 1

progress_label_lock = None
warnings_label_lock = None
errors_label_lock   = None

progress_label = ""
warnings_label = ""
errors_label = ""

DEBUGG = None
VERBOSE = None
OUT_FOLDER = None

# Inits global variables and locks, and gets access tokens for Spotify and Youtube APIs
def init_globals(keynum):
    global downloaded_songs, downloaded_songs_lock,started_songs, started_songs_lock, error_file_lock, url_file_lock, youtube, client_id, client_secret
    global youtube_lock
    global spoti
    global longsongs_file_lock

    global DEBUGG 
    global VERBOSE
    global OUT_FOLDER

    global song_list_len 

    global progress_label
    global warnings_label
    global errors_label 

    global progress_label_lock
    global warnings_label_lock
    global errors_label_lock
    
    downloaded_songs_lock = threading.Lock()
    started_songs_lock = threading.Lock()
    error_file_lock = threading.Lock()
    url_file_lock = threading.Lock()
    longsongs_file_lock = threading.Lock()
    youtube_lock = threading.Lock()
    progress_label_lock= threading.Lock()
    warnings_label_lock= threading.Lock()
    errors_label_lock= threading.Lock()

    downloaded_songs = 0
    started_songs = 0
    client_id = 'c6c3f6355e3349ce8160f0f2504e442b'
    client_secret = '2da4af43872a462ab652f579aa4b9d04'
    DEBUG = False
    VERBOSE = False
    OUT_FOLDER = '/Users/martin/Desktop/'

    # Parse arguments into global variables
    # DEBUGG, VERBOSE, OUT_FOLDER = helper.argparser()

    #! Store keys in file which doesnt go to github so my keys are not stolen
    # Use 1st key first time, and if we need to download more stuff change keynum to 2 so we use the second key
    ytb_key = helper.read_ytb_key('keys.txt', keynum=keynum)
    youtube = build('youtube', 'v3', developerKey=ytb_key)
    
    # Create global spotify instance
    spoti = spotify.Spotify(client_id,client_secret)

    # * Delete failed_songs file and if exist at the beginning
    if os.path.exists('failed_songs.txt'):
        os.remove('failed_songs.txt')
    if os.path.exists('long_songs.txt'):
        os.remove('long_songs.txt')
