import spotify
import config



def connect_spotify():
    # Get spotify credentials through OAuth 2.0
    spoti = spotify.Spotify(config.client_id,config.client_secret)
    spoti.get_auth_code()
    spoti.get_tokens()

def setup():
    #! Use 1st key first time, and if we need to download more stuff change keynum to 2 or 3 so we use the second key
    config.init_globals(keynum=1)