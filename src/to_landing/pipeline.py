"""Módulo responsável pela centralização de todo o pipeline para camada landing."""

from to_landing.extract import Extract
from to_landing.load import Load
from to_landing.transform import Transform
from utils.environment_loader import EnvLoader


class Spotify2Landing:
    """Classe responsável por centralizar a extração e carga dos dados do Spotify via API na camada landing."""

    def __init__(self):
        env_loader = EnvLoader()
        self.landing_path = env_loader.get_to_landing_path

    def start(self):
        # Realiza as requisições de todos métodos da classe Extract
        extract = Extract()
        artists_id = extract.search_for_artists_id(
            "sertanejo", 5, full_extract=False
        )

        artist_list = []
        artist_albums_list = []
        artist_top_tracks_list = []
        for artist_id in artists_id:
            artist_list.append(extract.get_artist(artist_id))
            artist_albums_list.append(extract.get_artist_albums(artist_id))
            artist_top_tracks_list.append(
                extract.get_artist_top_tracks(artist_id)
            )

        # Transforma os responses das requisições em DataFrame do pandas
        transform = Transform()
        artist_df = transform.artist_response_to_df(artist_list)
        artist_albums_df = transform.artist_albums_response_to_df(
            artist_albums_list
        )
        artist_top_tracks_df = transform.artist_top_tracks_response_to_df(
            artist_top_tracks_list
        )

        # Carrega os dados baixados para o datalake local (camada landing)
        load = Load()
        load.save_df_as_json(
            artist_df, landing_path=self.landing_path, folder_name="artists"
        )
        load.save_df_as_json(
            artist_albums_df,
            landing_path=self.landing_path,
            folder_name="artists_albums",
        )
        load.save_df_as_json(
            artist_top_tracks_df,
            landing_path=self.landing_path,
            folder_name="artists_top_tracks",
        )
