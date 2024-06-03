"""Módulo responsável por extrair os dados do Spotify."""

import base64
from typing import Any, Dict, List

from to_landing.api.handler_http import HTTPMETHODS, HTTPRequest, make_http_request
from utils.environment_loader import EnvLoader


class Extract:
    """Classe responsável por extrair os dados do Spotify via API."""

    def __init__(self):
        env_loader = EnvLoader()
        self.client_id = env_loader.get_spotify_client_id()
        self.client_secret = env_loader.get_spotify_client_secret()
        self.headers = self.get_auth_headers()

    def get_auth_headers(self) -> Dict[str, str]:
        auth_string = self.client_id + ":" + self.client_secret
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": f"Basic {auth_base64}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {"grant_type": "client_credentials"}

        token = make_http_request(
            HTTPRequest(
                url=url,
                method=HTTPMETHODS.POST,
                headers=headers,
                data=data,
            )
        ).json()["access_token"]

        return {"Authorization": f"Bearer {token}"}

    def search_for_artists_id(
        self, item: str, limit: int, full_extract: bool = False
    ) -> List[str]:
        url = "https://api.spotify.com/v1/search"
        query = f"q={item}&type=artist&limit={limit}&offset=0"
        query_url = f"{url}?{query}"

        if not full_extract:
            response = make_http_request(
                HTTPRequest(
                    url=query_url,
                    method=HTTPMETHODS.GET,
                    headers=self.headers,
                )
            ).json()

            artists_id = [item["id"] for item in response["artists"]["items"]]

            return artists_id

        else:
            all_results = []

            while query_url is not None:

                response = make_http_request(
                    HTTPRequest(
                        url=query_url,
                        method=HTTPMETHODS.GET,
                        headers=self.headers,
                    )
                ).json()["artists"]

                query_url = response["next"]

                all_results.extend(response["items"])

            return all_results

    def get_artist(self, artist_id: str) -> Dict[str, Any]:
        url = f"https://api.spotify.com/v1/artists/{artist_id}"

        return make_http_request(
            HTTPRequest(
                url=url,
                method=HTTPMETHODS.GET,
                headers=self.headers,
            )
        ).json()

    def get_artist_albums(self, artist_id: str) -> List[Dict[str, Any]]:
        url = f"https://api.spotify.com/v1/artists/{artist_id}/albums"

        return make_http_request(
            HTTPRequest(
                url=url,
                method=HTTPMETHODS.GET,
                headers=self.headers,
            )
        ).json()["items"]

    def get_artist_top_tracks(self, artist_id: str) -> List[Dict[str, Any]]:
        url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"

        return make_http_request(
            HTTPRequest(
                url=url,
                method=HTTPMETHODS.GET,
                headers=self.headers,
            )
        ).json()["tracks"]
