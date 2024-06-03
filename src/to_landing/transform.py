"""Módulo responsável por transformar os response em dataframe e adicionar colunas de qualidade."""

from datetime import datetime
from typing import Any, Dict, List

import pandas as pd


class Transform:
    """Classe responsável por transformar em dataframe os response e adicionar colunas de qualidade."""

    def __init__(self):
        pass

    def _add_metadada(self, df: pd.DataFrame):
        df["_source_type"] = "api"
        df["_source_name"] = "spotify"
        df["_extracted_at"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[
            :-3
        ]
        return df

    def artist_response_to_df(self, response: List[str]):
        artists_df = pd.DataFrame([artist for artist in response])
        artists_df = self._add_metadada(artists_df)
        return artists_df

    def artist_albums_response_to_df(
        self, response: List[List[Dict[str, Any]]]
    ):
        artists_albums_df = pd.DataFrame(
            [
                artist_albums
                for artist_albums_sublist in response
                for artist_albums in artist_albums_sublist
            ]
        )
        artists_albums_df = self._add_metadada(artists_albums_df)
        return artists_albums_df

    def artist_top_tracks_response_to_df(
        self, response: List[List[Dict[str, Any]]]
    ):
        artists_top_tracks_df = pd.DataFrame(
            [
                artist_top_tracks
                for artist_top_tracks_sublist in response
                for artist_top_tracks in artist_top_tracks_sublist
            ]
        )
        artists_top_tracks_df = self._add_metadada(artists_top_tracks_df)
        return artists_top_tracks_df
