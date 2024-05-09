from dotenv import load_dotenv
from pathlib import Path
import os
import requests


dotenv_path = Path.cwd() / ".env"
load_dotenv(dotenv_path=dotenv_path)

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

def get_token():
    auth_string = CLIENT_ID + ":" + CLIENT_SECRET
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = 'https://accounts.spotify.com/api/token'
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": 'client_credentials'}

    response = requests.post(url=url, headers=headers, data=data)

    token = response.json()["access_token"]

    return token

def get_auth_header(token):
    return {"Authorization": f"Bearer {token}"}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)

    query = f"q={artist_name}&type=artist&limit=1"
    query_url = f"{url}?{query}"

    response = requests.get(query_url, headers=headers)

    result = response.json()["artists"]["items"]

    if len(result) == 0:
        print("O artista escolhido não existe.")
        return None

    return result[0]

def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
    headers = get_auth_header(token)

    response = requests.get(url, headers=headers)

    return response.json()["tracks"]


token = get_token()
artist = search_for_artist(token, "Gusttavo Lima")
artist_id = artist["id"]
songs = get_songs_by_artist(token, artist_id)

for i, song in enumerate(songs):
    print(f"{i + 1}. {song["name"]}")
