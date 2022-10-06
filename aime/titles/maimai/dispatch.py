import zlib
import json
import logging
import inflection
import urllib.parse
import base64

from twisted.web import resource

from aime.titles.maimai.base import MaimaiBase
from aime.data import Config, Data

class MaimaiDispatch(resource.Resource):
    isLeaf = True

    def __init__(self, core_cfg: Config, game_cfg: Config):
        self.core_cfg = core_cfg
        self.game_cfg = game_cfg
        self.data = Data(core_cfg)
        self.logger = logging.getLogger("maimai")

        self.base = MaimaiBase(core_cfg, game_cfg)
    
    def render_POST(self, req) -> bytes:
        url: str = req.uri.decode()
        req_raw = req.content.getvalue()
        url_split = url.split("/")

        req_decomp = zlib.decompress(req_raw).decode()
        self.logger.info(f"Request {url} - {req_decomp}")

        req_split = inflection.underscore(url_split[2]).split("_")
        func_to_find = "handle_"
        for s in req_split:
            func_to_find += f"{s}_"
        func_to_find += "request"

        if url.endswith("oldServer"):
            self.logger.info("Old server request")
            return zlib.compress("{'stat': 1}".encode())

        try:
            handler = getattr(self.base, func_to_find)
            resp = handler(json.loads(req_decomp))

        except AttributeError as e:
            resp = None
            self.logger.debug(e)
            self.logger.warning(f"Unhandled request {url}")                

        except:
            self.logger.error(f"Error handling method {url}")
            raise
        
        if resp is None: resp = {"stat": 1}
        self.logger.info(f"Response {resp}")        
        return zlib.compress(json.dumps(resp).encode())

    def render_GET(self, request):
        return b""