import logging

from twisted.web import resource

from aime.data import Config
from aime.titles.idz.config import IDZConfig

class IDZNews(resource.Resource):
    isLeaf = True
    def __init__(self, cfg: Config, game_cfg: IDZConfig) -> None:
        self.core_config = cfg
        self.game_config = game_cfg
        self.logger = logging.getLogger("idz")
    
    def render_GET(self, request):
        client = request.getClientAddress()
        url: str = request.uri.decode()
        self.logger.info(f"News request from {client[0]}:{client[1]} - {url}")
        request.responseHeaders.addRawHeader(b"Content-Type", b"text/plain; charset=utf-8")

        resp_jp = u"ようこそ Initial D Arcade Stage Zero".encode()
        resp_ex = b"Welcome to Initial D Arcade Stage Zero"

        if url.endswith("JP.txt"):
            return resp_jp
        else:
            return resp_ex