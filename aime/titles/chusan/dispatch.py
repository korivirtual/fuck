import logging

from twisted.web import resource
import zlib
import inflection
import json

from aime.data import Config, Data
from aime.titles.chusan.base import ChusanBase
from aime.titles.chusan.new import ChusanNew

class ChusanDispatch(resource.Resource):
    isLeaf = True

    def __init__(self, core_cfg: Config, game_cfg: Config):
        self.core_cfg = core_cfg
        self.game_cfg = game_cfg
        self.data = Data(core_cfg)
        self.logger = logging.getLogger("chusan")

        self.base = ChusanBase(core_cfg, game_cfg)
        self.new = ChusanNew(core_cfg, game_cfg)
 
    def render_POST(self, request):
        url = request.uri.decode()
        func_to_find = "handle_"
        index = -1
        compress = True
        version = 0
        version_string = ""

        if "Api" not in url:
            if "MatchingServer" in url:
                self.logger.info(f"{version_string} Request {url}")
                self.logger.info(f'{version_string} Response "returnCode":"1"')
                return zlib.compress("{\"returnCode\": \"1\"}".encode("utf-8"))
            else:
                self.logger.warn("TITLE SERVER ENCRYPTION NOT SUPPORTED!!")
                return zlib.compress("{\"stat\": \"0\"}".encode("utf-8"))
        
        url_split = url.split("/")
        req_raw = request.content.getvalue()

        # Find where the part we care about is        
        for i, s in enumerate(url_split):
            if "Api" in s:
                index = i
                break
        
        if index == -1:
            self.logger.error(f"Unknown error occoured processing url: {url_split}")
            return zlib.compress("{\"stat\": \"0\"}".encode("utf-8"))
        
        try:
            version = int(url_split[1])
        except:
            self.logger.warn(f"Cannot decipher version {url_split[1]}, using latest (550)")
            version = 550

        req_split = inflection.underscore(url_split[index]).split("_")
        for x in req_split:
            func_to_find += f"{x}_" if not x == "" else ""
        func_to_find += f"request"

        try:            
            unzip = zlib.decompress(req_raw)
        except zlib.error:
            self.logger.warn("No compression used, somebody is probably poking at you.")
            compress = False
            unzip = req_raw

        req_data = json.loads(unzip)

        if version >= 200 and version < 205:
            version_string = "New"
            self.logger.info(f"{version_string} Request {url} - {req_data}")

            try:
                handler = getattr(self.new, func_to_find)
                resp = handler(req_data)
                
            except AttributeError as e: 
                self.logger.warning(f"Unhandled {version_string} request {url} - {e}")
                return zlib.compress("{\"stat\": \"0\"}".encode("utf-8"))

            except Exception as e:
                self.logger.error(f"Error handling {version_string} method {url} - {e}")
                return zlib.compress("{\"stat\": \"0\"}".encode("utf-8"))

        elif version < 200 :
            version_string = "Base"
            self.logger.info(f"{version_string} Request {url} - {req_data}")

            try:
                handler = getattr(self.base, func_to_find)
                resp = handler(req_data)
                
            except AttributeError as e: 
                self.logger.warning(f"Unhandled {version_string} request {url} - {e}")
                return zlib.compress("{\"stat\": \"0\"}".encode("utf-8"))

            except Exception as e:
                self.logger.error(f"Error handling {version_string} method {url} - {e}")
                return zlib.compress("{\"stat\": \"0\"}".encode("utf-8"))

        else:
            self.logger.warning(f"Unhandled version {version}")
            return zlib.compress("{\"stat\": \"0\"}".encode("utf-8"))
        
        self.logger.info(f"{version_string} Response {resp}")
        
        if compress:
            return zlib.compress(json.dumps(resp, ensure_ascii=False).encode("utf-8"))
        else:
            return json.dumps(resp, ensure_ascii=False).encode("utf-8")

    def render_GET(self, request):
        return b""