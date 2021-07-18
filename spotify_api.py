import os
import requests
import base64
import datetime
from urllib.parse import urlencode


class SpotifyAPI(object):
    token = None
    expires = datetime.datetime.now()
    client_id = None
    client_secret = None

    def __init__(self, client_id, client_secret, *args, **kwargs):
        self.client_id = client_id
        self.client_secret = client_secret

    def authenticate(self):
        client_id = self.client_id
        client_secret = self.client_secret
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        token_url = "https://accounts.spotify.com/api/token"
        token_data = {
            "grant_type": "client_credentials"
        }
        token_headers = {
            "Authorization": f"Basic {client_creds_b64.decode()}"
        }
        r = requests.post(token_url, data=token_data, headers=token_headers)
        if r.status_code not in range(200, 299):
            return False
        token_response_data = r.json()
        access_token = token_response_data['access_token']
        expires_in = token_response_data['expires_in']
        self.token, self.expires = access_token, datetime.datetime.now() + datetime.timedelta(seconds=expires_in)
        return True

    def get_album(self, name):
        if datetime.datetime.now() >= self.expires - datetime.timedelta(seconds=5):
            self.authenticate()

        header = {
            "Authorization": f"Bearer {self.token}"
        }
        name = name.split('–')
        name = name[0] + name[1]
        data = urlencode({"q": name, "type": "album"})
        lookup_url = f"https://api.spotify.com/v1/search?{data}"
        r = requests.get(lookup_url, headers=header)
        return r.json()['albums']['items'][0]['external_urls']['spotify']