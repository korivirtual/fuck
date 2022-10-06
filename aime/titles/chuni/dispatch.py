import logging

from twisted.web import resource
import zlib
import inflection
import json

from aime.data import Config, Data
from aime.titles.chuni.base import ChuniBase
from aime.titles.chuni.amazon import ChuniAmazon
from aime.titles.chuni.amazonplus import ChuniAmazonPlus
from aime.titles.chuni.crystal import ChuniCrystal
from aime.titles.chuni.crystalplus import ChuniCrystalPlus
from aime.titles.chuni.paradise import ChuniParadise

class ChuniDispatch(resource.Resource):
    isLeaf = True

    def __init__(self, core_cfg: Config, game_cfg: Config):
        self.core_cfg = core_cfg
        self.game_cfg = game_cfg
        self.data = Data(core_cfg)
        self.logger = logging.getLogger("chuni")

        self.base = ChuniBase(core_cfg, game_cfg)
        self.amazon = ChuniAmazon(core_cfg, game_cfg)
        self.amazonplus = ChuniAmazonPlus(core_cfg, game_cfg)
        self.crystal = ChuniCrystal(core_cfg, game_cfg)
        self.crystalplus = ChuniCrystalPlus(core_cfg, game_cfg)
        self.paradise = ChuniParadise(core_cfg, game_cfg)

    def render_POST(self, request):
        url = request.uri.decode()
        func_to_find = "handle_"
        index = -1
        compress = True
        version = 0
        version_string = ""

        if "Api" not in url:
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

        if version >= 130 and version < 135:
            version_string = "Amazon"
            self.logger.info(f"{version_string} Request {url} - {req_data}")

            try:
                handler = getattr(self.amazon, func_to_find)
                resp = handler(req_data)
                
            except AttributeError as e: 
                self.logger.warning(f"Unhandled {version_string} request {url} - {e}")
                return zlib.compress("{\"stat\": \"0\"}".encode("utf-8"))

            except Exception as e:
                self.logger.error(f"Error handling {version_string} method {url} - {e}")
                return zlib.compress("{\"stat\": \"0\"}".encode("utf-8"))

        elif version >= 135 and version < 140:
            version_string = "AmazonPlus"
            self.logger.info(f"{version_string} Request {url} - {req_data}")

            try:
                handler = getattr(self.amazonplus, func_to_find)
                resp = handler(req_data)
                
            except AttributeError as e: 
                self.logger.warning(f"Unhandled {version_string} request {url} - {e}")
                return zlib.compress("{\"stat\": \"0\"}".encode("utf-8"))

            except Exception as e:
                self.logger.error(f"Error handling {version_string} method {url} - {e}")
                return zlib.compress("{\"stat\": \"0\"}".encode("utf-8"))

        elif version >= 140 and version < 145:
            version_string = "Crystal"
            self.logger.info(f"{version_string} Request {url} - {req_data}")

            try:
                handler = getattr(self.crystal, func_to_find)
                resp = handler(req_data)
                
            except AttributeError as e: 
                self.logger.warning(f"Unhandled {version_string} request {url} - {e}")
                return zlib.compress("{\"stat\": \"0\"}".encode("utf-8"))

            except Exception as e:
                self.logger.error(f"Error handling {version_string} method {url} - {e}")
                return zlib.compress("{\"stat\": \"0\"}".encode("utf-8"))

        elif version >= 145 and version < 150:
            version_string = "CrystalPlus"
            self.logger.info(f"{version_string} Request {url} - {req_data}")

            try:
                handler = getattr(self.crystalplus, func_to_find)
                resp = handler(req_data)
                
            except AttributeError as e: 
                self.logger.warning(f"Unhandled {version_string} request {url} - {e}")
                return zlib.compress("{\"stat\": \"0\"}".encode("utf-8"))

            except Exception as e:
                self.logger.error(f"Error handling {version_string} method {url} - {e}")
                return zlib.compress("{\"stat\": \"0\"}".encode("utf-8"))

        elif version >= 150 and version < 155:
            version_string = "Paradise"
            self.logger.info(f"{version_string} Request {url} - {req_data}")

            try:
                handler = getattr(self.paradise, func_to_find)
                resp = handler(req_data)
                
            except AttributeError as e: 
                self.logger.warning(f"Unhandled {version_string} request {url} - {e}")
                return zlib.compress("{\"stat\": \"0\"}".encode("utf-8"))

            except Exception as e:
                self.logger.error(f"Error handling {version_string} method {url} - {e}")
                return zlib.compress("{\"stat\": \"0\"}".encode("utf-8"))

        elif version < 130 :
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
        
        if resp == None:
            resp = {'returnCode': 1}
        
        self.logger.info(f"{version_string} Response {resp}")
        
        if compress:
            return zlib.compress(json.dumps(resp, ensure_ascii=False).encode("utf-8"))
        else:
            return json.dumps(resp, ensure_ascii=False).encode("utf-8")

    
    def render_GET(self, request):
        return b""
