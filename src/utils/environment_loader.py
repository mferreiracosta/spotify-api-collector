"""Módulo responsável por carregar as variáveis de ambiente no código."""

import os

from dotenv import load_dotenv


class EnvLoader:
    """Classe responsável por carregar as variáveis de ambientes."""

    def __init__(self):
        """Inicializa as variáveis da classe."""
        self.root_path = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
        self._load_environment()

    def _load_environment(self):
        """Método privado que carrega as variáveis de ambiente para o código."""
        file_path = os.path.join(self.root_path, ".env")

        load_dotenv(dotenv_path=file_path)

    def get_spotify_client_id(self) -> str:
        """Método para buscar o client_id do spotify."""
        return os.getenv("CLIENT_ID")

    def get_spotify_client_secret(self) -> str:
        """Método para buscar o client_secret do spotify."""
        return os.getenv("CLIENT_SECRET")
