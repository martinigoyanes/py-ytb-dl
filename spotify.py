import webbrowser
import requests
import base64

from urllib.parse import urlencode

class Spotify:
    id = None
    secret = None
    auth_code = None
    access_token = None
    refresh_token = None
    access_token_expires = None

    def __init__(self,id,secret):
        self.id = id
        self.secret = secret
        
    def get_auth_code(self):
        auth_endpoint = 'https://accounts.spotify.com/authorize'
        auth_body = {
            'client_id': self.id,
            'response_type': 'code',
            'redirect_uri': 'http://localhost:8888/callback',
            'scope': 'user-library-read'
        }
        auth_body_urlencoded = urlencode(auth_body)
        auth_url = f"{auth_endpoint}?{auth_body_urlencoded}"
        # TODO: Automate the process of getting an authorization code maybe with selenium
        webbrowser.open(auth_url)
        self.auth_code = input('Authentication code:\n')

    def get_tokens(self):
        tokens_endpoint = 'https://accounts.spotify.com/api/token'
        tokens_body = {
            'grant_type': 'authorization_code',
            'code': self.auth_code,
            'redirect_uri': 'http://localhost:8888/callback'
        }
        client_creds_b64 = base64.b64encode(f'{self.id}:{self.secret}'.encode())
        tokens_headers = {
            # Authorization: Basic *<base64 encoded client_id:client_secret>*
            'Authorization': f'Basic {client_creds_b64.decode()}'
        }
        resp = requests.post(tokens_endpoint, data=tokens_body, headers=tokens_headers)
        tokens_resp_data = resp.json()
        self.access_token = tokens_resp_data['access_token']
        self.refresh_token = tokens_resp_data['refresh_token']
        self.access_token_expires= tokens_resp_data['expires_in']

    def get_tracks_json(self,limit=1,offset=None):
        user_tracks_endpoint = 'https://api.spotify.com/v1/me/tracks'
        user_tracks_headers = {
            # Authorization: Bearer {your access token}
            'Authorization': f'Bearer {self.access_token}'
        }
        # TODO: Use the limit and offset parameters to get the whole list of saved songs
        user_tracks_body = {
            'limit': limit
        }
        if offset is not None:
            user_tracks_body.update({'offset':offset})

        user_tracks_body_urlencoded = urlencode(user_tracks_body)
        user_tracks_url = f"{user_tracks_endpoint}?{user_tracks_body_urlencoded}"
        resp = requests.get(user_tracks_url, headers=user_tracks_headers)

        return resp.json()
