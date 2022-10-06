import logging
import json
import zlib
from typing import Dict
import re

import inflection
from twisted.web import resource

from aime.data import Config, Data
from aime.titles.cxb.config import CxbConfig
from aime.titles.cxb.base import CxbBase
from aime.titles.cxb.rev import CxbRev
from aime.titles.cxb.rss1 import CxbRevSunriseS1
from aime.titles.cxb.rss2 import CxbRevSunriseS2

class CxbDispatch(resource.Resource):
    isLeaf = True
    def __init__(self, core_cfg: Config, game_cfg: CxbConfig) -> None:
        self.core_cfg = core_cfg
        self.game_cfg = game_cfg
        self.data = Data(core_cfg)
        self.logger = logging.getLogger("cxb")

        self.base = CxbBase(core_cfg, game_cfg)
        self.rev = CxbRev(core_cfg, game_cfg)
        self.rss1 = CxbRevSunriseS1(core_cfg, game_cfg)
        self.rss2 = CxbRevSunriseS2(core_cfg, game_cfg)
    
    def render_POST(self, request):
        version = 0
        req_url = request.uri.decode()
        req_bytes = request.content.readlines()[0]
        try:
            req_json: Dict = json.loads(req_bytes)

        except Exception as e:
            try:
                req_json: Dict = json.loads(req_bytes.decode().replace('"', '\\"').replace("'", '"'))

            except Exception as f:
                self.logger.warn(f"Error decoding json: {e} / {f} - {req_url} - {req_bytes}")
                return b""

        func_to_find = "handle_"

        if "data" in req_url:
            func_to_find += "data_"

            if "dldate" in req_json:
                filetype = req_json["dldate"]["filetype"]
                filetype_split = req_json["dldate"]["filetype"].split("/")
                version = filetype_split[0]
                self.logger.debug(int(version) == 10104)
                filetype_inflect_split = inflection.underscore(filetype).split("/")

                match = re.match("^([A-Za-z]*)(\d\d\d\d)$", filetype_split[len(filetype_split) - 1])
                if match:
                    func_to_find += f"{inflection.underscore(match.group(1))}xxxx_"
                else:
                    func_to_find += f"{filetype_inflect_split[len(filetype_inflect_split) - 1]}_"
            
            elif "putlog" in req_json:
                func_to_find += "putlog_"

            else:
                self.logger.warn(f"Unknown data request {req_json}")
                return b""
        
        elif "action" in req_url:
            func_to_find += f"action_{list(req_json)[0]}_"
        
        elif "auth" in req_url:
            func_to_find += f"auth_{list(req_json)[0]}_"
        
        else:
            self.logger.warn(f"Unknown endpoint {req_url} - {req_json}")
            return b""

        func_to_find += "request"
        
        if int(version) <= 10102:
            version_string = "REV"
            self.logger.info(f"{version_string} Request {req_url} - {req_json}")
            
            try:
                handler = getattr(self.rev, func_to_find)
                resp = handler(req_json)
            
            except AttributeError as e: 
                self.logger.warning(f"Unhandled {version_string} request {req_url} - {e}")
                return { "data": "" }

            except Exception as e:
                self.logger.error(f"Error handling {version_string} method {req_url} - {e}")
                return { "data": "" }
            
            self.logger.info(f"{version_string} Response {resp}")

        elif int(version) > 10102 and int(version) < 10104:
            version_string = "SunriseS1"
            self.logger.info(f"{version_string} Request {req_url} - {req_json}")
        
            try:
                handler = getattr(self.rss1, func_to_find)
                resp = handler(req_json)
            
            except AttributeError as e: 
                self.logger.warning(f"Unhandled {version_string} request {req_url} - {e}")
                return { "data": "" }

            except Exception as e:
                self.logger.error(f"Error handling {version_string} method {req_url} - {e}")
                return { "data": "" }
            
            self.logger.info(f"{version_string} Response {resp}")
            
        elif int(version) >= 10104:
            version_string = "SunriseS2"
            self.logger.info(f"{version_string} Request {req_url} - {req_json}")
        
            try:
                handler = getattr(self.rss2, func_to_find)
                resp = handler(req_json)
            
            except AttributeError as e: 
                self.logger.warning(f"Unhandled {version_string} request {req_url} - {e}")
                return { "data": "" }

            except Exception as e:
                self.logger.error(f"Error handling {version_string} method {req_url} - {e}")
                return { "data": "" }
            
            self.logger.info(f"{version_string} Response {resp}")
            
        else:
            version_string = "Base"
            self.logger.info(f"{version_string} Request {req_url} - {req_json}")
        
            try:
                handler = getattr(self.base, func_to_find)
                resp = handler(req_json)
            
            except AttributeError as e: 
                self.logger.warning(f"Unhandled {version_string} request {req_url} - {e}")
                return { "data": "" }

            except Exception as e:
                self.logger.error(f"Error handling {version_string} method {req_url} - {e}")
                return { "data": "" }
            
            self.logger.info(f"{version_string} Response {resp}")
        
        return json.dumps(resp, ensure_ascii=False).encode("utf-8")

    def render_GET(self, request):
        return b""
