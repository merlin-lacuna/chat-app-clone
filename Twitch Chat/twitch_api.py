import os
import requests
from typing import List

CLIENT_ID = os.environ["TwitchAppClientId"]
CLIENT_SECRET = os.environ["TwitchAppClientSecret"]
BASE_URL = 'https://api.twitch.tv/helix/'

HEADERS = {
    'Client-ID': CLIENT_ID,
    'Content-Type': 'application/json',
}

def get_oauth_token(client_id, client_secret):
    url = 'https://id.twitch.tv/oauth2/token'
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, params=payload)
    return response.json().get('access_token')

def _get_top_streams(oauth_token: str, limit: int):
    headers = {
        **HEADERS,
        'Authorization': f"Bearer {oauth_token}"
    }
    params = {
        'first': limit,
        'type': 'live'
    }
    response = requests.get(f"{BASE_URL}streams", headers=headers, params=params)
    return response.json().get('data', [])

def _get_live_streams_by_users(oauth_token: str, user_logins: List[str]):
    headers = {
        **HEADERS,
        'Authorization': f"Bearer {oauth_token}"
    }
    params = {
        'user_login': user_logins,
        'type': 'live'
    }
    response = requests.get(f"{BASE_URL}streams", headers=headers, params=params)
    return response.json().get('data', [])

def get_top_streams(limit: int = 50):
    oauth_token = get_oauth_token(CLIENT_ID, CLIENT_SECRET)
    top_streams = _get_top_streams(oauth_token, limit)

    return [stream["user_login"] for stream in top_streams]

def get_live_streams_by_users(user_logins: List[str]):
    oauth_token = get_oauth_token(CLIENT_ID, CLIENT_SECRET)
    live_streams = _get_live_streams_by_users(oauth_token, user_logins)

    return [stream["user_login"] for stream in live_streams]
