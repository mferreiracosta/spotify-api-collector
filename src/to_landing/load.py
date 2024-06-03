"""Módulo responsável por realizar a carga dos dados na camada landing."""

import pandas as pd


class Load:
    """Classe responsável por realizar a carga dos dados baixados via API do Spotify para a camada landing."""

    def __init__(self):
        pass

    def save_df_as_json(
        self, df: pd.DataFrame, landing_path: str, folder_name: str
    ):
        df.to_json(
            f"{landing_path}/{folder_name}/data.json",
            orient="records",
            index=False,
        )
