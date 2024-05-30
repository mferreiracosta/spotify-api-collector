"""Módulo responsável pela centralização dos códigos de todo projeto."""


import json
from dotenv import load_dotenv
from pathlib import Path
import os
import pandas as pd
import requests

import base64


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

def search_for_item(token, item, limit):
    
    headers = get_auth_header(token)

    url = "https://api.spotify.com/v1/search"
    query = f"q={item}&type=artist&limit={limit}&offset=0"
    query_url = f"{url}?{query}"

    response = requests.get(query_url, headers=headers)
    result = response.json()["artists"]["items"]

    return result

    # all_results = []

    # while query_url is not None:

    #     response = requests.get(query_url, headers=headers)
    #     result = response.json()["artists"]
    #     query_url = result["next"]
    #     print(query_url)

    #     all_results.extend(result["items"])

    # return all_results

def get_artists_by_artist_id(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = get_auth_header(token)

    response = requests.get(url, headers=headers)

    return response.json()  #["tracks"]

def get_albums_by_artist_id(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums"
    headers = get_auth_header(token)

    response = requests.get(url, headers=headers)

    return response.json()  #["tracks"]

def get_album_tracks_by_album_id(token, album_id):
    url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
    headers = get_auth_header(token)

    response = requests.get(url, headers=headers)

    return response.json()  #["tracks"]

def get_songs_by_artist_id(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
    headers = get_auth_header(token)

    response = requests.get(url, headers=headers)

    return response.json()  #["tracks"]

def get_related_artists_by_artist_id(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/related-artists"
    headers = get_auth_header(token)

    response = requests.get(url, headers=headers)

    return response.json()  #["tracks"]

def main():

    token = get_token()
    artists = search_for_item(token, "sertanejo", 5)

    df = pd.DataFrame(artists)
    df.to_json("data/landing/data.json", orient="records", index=False)

    rows = []

    with open("data/landing/data.json", "r") as file:
        json_data = json.load(file)

    for data in json_data:
        row = {
            "id": data["id"],
            "name": data["name"],
            "popularity": data["popularity"],
            "type": data["type"],
            "uri": data["uri"],
            "external_urls": data["external_urls"]["spotify"] if "external_urls" in data else None,
            "total_followers": data["followers"]["total"] if 'followers' in data else None,
            "genres": data["genres"] if "genres" in data else None,
        }

        rows.append(row)

    df = pd.DataFrame(rows)
    print(df.head())
    print(df.info())

    # for i, song in enumerate(songs):
    #     print(f"{i + 1}. {song["name"]}")

    # 2LweFzHQTdOl0LSqwOS5uM


if __name__== "__main__":
    main()
