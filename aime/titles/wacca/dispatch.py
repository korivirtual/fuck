import logging
import json
from typing import List
from datetime import datetime, timedelta
from hashlib import md5

from twisted.web import resource
import pytz

from aime.data import Config, Data
from aime.titles.wacca.config import WaccaConfig
from aime.titles.wacca.const import WaccaConstants
from aime.titles.wacca.reverse import WaccaReverse
from aime.titles.wacca.lilyr import WaccaLilyR
from aime.titles.wacca.lily import WaccaLily
from aime.titles.wacca.s import WaccaS
from aime.titles.wacca.base import WaccaBase

class WaccaDispatch(resource.Resource):
    isLeaf = True
    def __init__(self, core_cfg: Config, game_cfg: WaccaConfig) -> None:
        self.core_cfg = core_cfg
        self.game_cfg = game_cfg
        self.data = Data(core_cfg)
        self.logger = logging.getLogger("wacca")

        self.reverse = WaccaReverse(core_cfg, game_cfg)
        self.lilyr = WaccaLilyR(core_cfg, game_cfg)
        self.lily = WaccaLily(core_cfg, game_cfg)
        self.s = WaccaS(core_cfg, game_cfg)
        self.base = WaccaBase(core_cfg, game_cfg)
    
    def render_POST(self, request):
        version_full = []
        try:
            req_json = json.loads(request.content.getvalue())
            version_full = req_json["appVersion"].split(".")
        except:
            self.logger.error(f"Failed to parse request {request.content.getvalue()}")
            return b""

        url: str = request.uri.decode()
        url_split = url.split("/")
        start_req_idx = url_split.index("api") + 1

        func_to_find = "handle_"
        for x in range(len(url_split) - start_req_idx):

            func_to_find += f"{url_split[x + start_req_idx]}_"
        func_to_find += "request"

        version_major = int(version_full[0])
        version_minor = int(version_full[1])
        version_patch = int(version_full[2])
        version_region = version_full[3]

        # Beginning of the response is the same every time, it's just the params that change
        resp = {            
            "status": 0,
            "message": "",
            "serverTime": int(datetime.now().timestamp()),
            "maintNoticeTime": 0,
            "maintNotPlayableTime": 0,
            "maintStartTime": 0,
            "params": []
        }

        if version_major == 2:
            # WACCA Lily / R
            if version_minor >= 50:
                # Lily R
                version_str = f"Lily R ({version_major}.{version_minor}.{version_patch})"
                self.logger.info(f"{version_str} request {url} - {req_json}")

                try:
                    handler = getattr(self.lilyr, func_to_find)
                    params = handler(req_json)
                    if params is not None:
                        resp["params"] = params
                    
                    self.logger.info(f"{version_str} response {resp}")

                except AttributeError as e:
                    self.logger.warning(f"{version_str} Unhandled request {url} {e}")                

                except:
                    self.logger.error(f"{version_str} Error handling method {url}")
                    raise

            else:
                version_str = f"Lily ({version_major}.{version_minor}.{version_patch})"
                self.logger.info(f"{version_str} request {url} - {req_json}")
                self.logger.warn(f"{version_str} Not supported yet")

                try:
                    handler = getattr(self.lily, func_to_find)
                    params = handler(req_json)
                    if params is not None:
                        resp["params"] = params
                    
                    self.logger.info(f"{version_str} response {resp}")

                except AttributeError as e:
                    self.logger.warning(f"{version_str} Unhandled request {url} {e}")                

                except:
                    self.logger.error(f"{version_str} Error handling method {url}")
                    raise

        elif version_major == 1:
            # WACCA / S
            if version_minor >= 50:
                version_str = f"S ({version_major}.{version_minor}.{version_patch})"
                self.logger.info(f"{version_str} request {url} - {req_json}")

                try:
                    handler = getattr(self.s, func_to_find)
                    params = handler(req_json)
                    if params is not None:
                        resp["params"] = params
                    
                    self.logger.info(f"{version_str} response {resp}")

                except AttributeError as e:
                    self.logger.warning(f"{version_str} Unhandled request {url} {e}")                

                except:
                    self.logger.error(f"{version_str} Error handling method {url}")
                    raise
            else:
                version_str = f"Wacca ({version_major}.{version_minor}.{version_patch})"
                self.logger.info(f"{version_str} request {url} - {req_json}")

                try:
                    handler = getattr(self.base, func_to_find)
                    params = handler(req_json)
                    if params is not None:
                        resp["params"] = params
                    
                    self.logger.info(f"{version_str} response {resp}")

                except AttributeError as e:
                    self.logger.warning(f"Unhandled request {url} {e}")                

                except:
                    self.logger.error(f"Error handling method {url}")
                    raise

        elif version_major == 3:
            # Reverse
            version_str = f"Reverse ({version_major}.{version_minor}.{version_patch})"
            self.logger.info(f"{version_str} request {url} - {req_json}")
            
            try:
                handler = getattr(self.reverse, func_to_find)
                params = handler(req_json)
                if params is not None:
                    resp["params"] = params
                
                self.logger.info(f"{version_str} response {resp}")

            except AttributeError as e:
                self.logger.debug(e)
                self.logger.warning(f"Unhandled request {url}")                

            except:
                self.logger.error(f"Error handling method {url}")
                raise
                
        hash = md5(json.dumps(resp).encode()).digest()
        request.responseHeaders.addRawHeader(b"X-Wacca-Hash", hash.hex().encode())
        return json.dumps(resp).encode()

    def render_GET(self, request):
        return b""
