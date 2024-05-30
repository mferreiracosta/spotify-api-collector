"""Módulo responsável por extrair os dados do Spotify."""


class Extract:
    """Classe responsável por extrair os dados do Spotify via API."""

    def __init__(self):
        self.headers = self.get_auth_headers()

    def get_auth_headers(self):
        pass

    def search_for_item(self):
        pass

    def get_artist(self):
        pass

    def get_artist_albums(self):
        pass

    def get_artist_top_tracks(self):
        pass
