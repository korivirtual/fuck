import json
import logging
import zlib
import inflection

from twisted.web import resource

from aime.titles.mai2.base import Mai2Base
from aime.titles.mai2.plus import Mai2Plus
from aime.titles.mai2.splash import Mai2Splash
from aime.titles.mai2.splashplus import Mai2SplashPlus
from aime.titles.mai2.universe import Mai2Universe
from aime.titles.mai2.config import Mai2Config
from aime.data import Config

class Mai2Dispatch(resource.Resource):
    isLeaf = True
    def __init__(self, cfg: Config, game_cfg: Mai2Config) -> None:
        self.core_config = cfg
        self.game_config = game_cfg
        self.base = Mai2Base(cfg, game_cfg)
        self.plus = Mai2Plus(cfg, game_cfg)
        self.splash = Mai2Splash(cfg, game_cfg)
        self.splashplus = Mai2SplashPlus(cfg, game_cfg)
        self.universe = Mai2Universe(cfg, game_cfg)
        self.logger = logging.getLogger("mai2")
        
    def render_POST(self, req) -> bytes:
        url = req.uri.decode()
        url_split = url.split("/")

        req_split = inflection.underscore(url_split[3]).split("_")
        func_to_find = "handle_"
        for s in req_split:
            func_to_find += f"{s}_"
        func_to_find += "request"

        resp = {"stat": 1}
        req.responseHeaders.addRawHeader(b"content-type", b"application/json")

        if int(url_split[1]) >= 100 and int(url_split[1]) < 105:
            version_str = f"Delux ({url_split[1]})"
            reqDecomp = zlib.decompress(req.content.getvalue()).decode()
            self.logger.info(f"{version_str} Request {url} - {reqDecomp}")

            try:
                handler = getattr(self.base, func_to_find)
                resp = handler(json.loads(reqDecomp))

            except AttributeError as e:
                self.logger.debug(e)
                self.logger.warning(f"{version_str} Unhandled request {url}")                

            except:
                self.logger.error(f"{version_str} Error handling method {url}")
                raise

        elif int(url_split[1]) >= 105 and int(url_split[1]) < 110:
            version_str = f"Delux PLUS ({url_split[1]})"
            reqDecomp = zlib.decompress(req.content.getvalue()).decode()
            self.logger.info(f"{version_str} Request {url} - {reqDecomp}")

            try:
                handler = getattr(self.plus, func_to_find)
                resp = handler(json.loads(reqDecomp))

            except AttributeError as e:
                self.logger.debug(e)
                self.logger.warning(f"{version_str} Unhandled request {url}")                

            except:
                self.logger.error(f"{version_str} Error handling method {url}")
                raise

        elif int(url_split[1]) >= 110 and int(url_split[1]) < 115:
            version_str = f"Splash ({url_split[1]})"
            reqDecomp = zlib.decompress(req.content.getvalue()).decode()
            self.logger.info(f"{version_str} Request {url} - {reqDecomp}")

            try:
                handler = getattr(self.splash, func_to_find)
                resp = handler(json.loads(reqDecomp))

            except AttributeError as e:
                self.logger.debug(e)
                self.logger.warning(f"{version_str} Unhandled request {url}")                

            except:
                self.logger.error(f"{version_str} Error handling method {url}")
                raise
        
        elif int(url_split[1]) >= 115 and int(url_split[1]) < 120:
            version_str = f"Splash PLUS ({url_split[1]})"
            reqDecomp = zlib.decompress(req.content.getvalue()).decode()
            self.logger.info(f"{version_str} Request {url} - {reqDecomp}")

            try:
                handler = getattr(self.splashplus, func_to_find)
                resp = handler(json.loads(reqDecomp))

            except AttributeError as e:
                self.logger.debug(e)
                self.logger.warning(f"{version_str} Unhandled request {url}")                

            except:
                self.logger.error(f"{version_str} Error handling method {url}")
                raise

        elif int(url_split[1]) >= 120 and int(url_split[1]) < 125:
            version_str = f"Universe ({url_split[1]})"
            reqDecomp = zlib.decompress(req.content.getvalue()).decode()
            self.logger.info(f"{version_str} Request {url} - {reqDecomp}")

            try:
                handler = getattr(self.universe, func_to_find)
                resp = handler(json.loads(reqDecomp))

            except AttributeError as e:
                self.logger.debug(e)
                self.logger.warning(f"{version_str} Unhandled request {url}")                

            except:
                self.logger.error(f"{version_str} Error handling method {url}")
                raise

        else:
            version_str = f"Universe ({url_split[1]})"
            reqDecomp = zlib.decompress(req.content.getvalue()).decode()
            self.logger.warning(f"Unhandled version {url_split[1]}, using latest")
            self.logger.info(f"{version_str} Request {url} - {reqDecomp}")

            try:
                handler = getattr(self.universe, func_to_find)
                resp = handler(json.loads(reqDecomp))

            except AttributeError as e:
                self.logger.debug(e)
                self.logger.warning(f"{version_str} Unhandled request {url}")                

            except:
                self.logger.error(f"{version_str} Error handling method {url}")
                raise
            
        if resp is None: resp = {"returnCode": 1, "apiName": url_split[3]}
        self.logger.info(f"{version_str} Response {resp}")
        return zlib.compress(json.dumps(resp).encode())

    def render_GET(self, request):
        return b""