import json
import logging
from typing import Dict
import zlib
import inflection

from twisted.web import resource

from aime.titles.idac.base import IDACBase
from aime.titles.idac.config import IDACConfig
from aime.data import Config

class IDACDispatch(resource.Resource):
    isLeaf = True
    def __init__(self, cfg: Config, game_cfg: IDACConfig) -> None:
        self.core_config = cfg
        self.game_config = game_cfg
        self.base = IDACBase(cfg, game_cfg)
        self.logger = logging.getLogger("idac")
    
    def render_POST(self, req) -> bytes:
        url = req.uri.decode()
        req_split = url.lower().split("/")
        func_to_find = "handle_"
        req_data = req.content.getvalue().decode()
        
        if req_split[1] == "initiald":
            self.logger.info(f"IDAC request from {req.getClientIP()}: {url} - {req_data}")
            header_application = self.decode_header(req.getAllHeaders())

            for x in req_split:
                func_to_find += f"{x}_" if not x == "" and not x == "initiald" else ""
            func_to_find += f"request"
            
            try:
                handler = getattr(self.base, func_to_find)
                resp = handler(json.loads(req_data), header_application)
                
            except AttributeError as e: 
                self.logger.warning(f"Unhandled IDAC request {url} - {e}")
                return "{\"status_code\": \"0\"}".encode("utf-8")

            except Exception as e:
                self.logger.error(f"Error handling IDAC method {url} - {e}")
                return "{\"status_code\": \"0\"}".encode("utf-8")
            
            if resp == None:
                resp = {"status_code": "0"}

            self.logger.info(f"IDAC Response {resp}")
            return json.dumps(resp, ensure_ascii=False).encode("utf-8")
        
        self.logger.info(f"IDAC unknown request from {req.getClientIP()}: {url} - {req.content.getvalue().decode()}")
        return "{\"status_code\": \"0\"}".encode("utf-8")
    
    def decode_header(self, data: Dict) -> Dict:
        app: str = data[b"application"].decode()
        ret = {}

        for x in app.split(", "):
            y = x.split("=")
            ret[y[0]] = y[1].replace("\"", "")

        return ret

        
