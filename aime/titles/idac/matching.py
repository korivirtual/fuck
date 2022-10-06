import json
import logging
from typing import Dict
import zlib
import inflection

from twisted.web import resource

from aime.titles.idac.base import IDACBase
from aime.titles.idac.config import IDACConfig
from aime.data import Config

class IDACMatching(resource.Resource):
    isLeaf = True
    def __init__(self, cfg: Config, game_cfg: IDACConfig) -> None:
        self.core_config = cfg
        self.game_config = game_cfg
        self.base = IDACBase(cfg, game_cfg)
        self.logger = logging.getLogger("idac")

    def render_POST(self, req) -> bytes:
        url = req.uri.decode()
        req_data = req.content.getvalue().decode()
        header_application = self.decode_header(req.getAllHeaders())

        self.logger.info(f"IDAC Matching request from {req.getClientIP()}: {url} - {req_data}")

        if url == "/regist":
            return json.dumps({"status_code": "0"}, ensure_ascii=False).encode("utf-8")
        elif url == "/status":
            return json.dumps({"status_code": "0", "host": req.getClientIP(), "port": 20002, "room_name": "asdg", "state": 0}, ensure_ascii=False).encode("utf-8")
    
    def decode_header(self, data: Dict) -> Dict:
        app: str = data[b"application"].decode()
        ret = {}

        for x in app.split(", "):
            y = x.split("=")
            ret[y[0]] = y[1].replace("\"", "")

        return ret