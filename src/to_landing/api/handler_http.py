"""Módulo responsável pela requisição da API do Spotify via HTTP."""



from enum import Enum
from pydantic import BaseModel


class HTTPMETHODS(Enum):
    pass


class HTTPRequest(BaseModel):
    pass


async def make_http_request(http_request: HTTPRequest) -> str:
    pass
