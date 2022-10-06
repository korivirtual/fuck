import base64
import json
import logging, coloredlogs
import os
import yaml
from typing import Any, Dict
import zlib
from twisted.web import resource
import importlib
from datetime import datetime
import pytz
from logging.handlers import TimedRotatingFileHandler

from aime.data import Config, Data
from aime.deliver import NetDeliver

registry: Dict[str, Any] = {}

class Allnet(resource.Resource):
    isLeaf = True

    def __init__(self, cfg: Config, cfg_dir: str) -> None:
        self.config = cfg
        self.data = Data(cfg)        
        self.logger = logging.getLogger("allnet")

        if self.config.allnet.ota_delivery:
            self.deliver = NetDeliver(cfg)
        else:
            self.deliver = None

        log_fmt_str = "[%(asctime)s] Allnet | %(levelname)s | %(message)s"
        log_fmt = logging.Formatter(log_fmt_str)        

        fileHandler = TimedRotatingFileHandler("{0}/{1}.log".format(self.config.server.logs, "allnet"), when="d", backupCount=10)
        fileHandler.setFormatter(log_fmt)
        
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(log_fmt)

        self.logger.addHandler(fileHandler)
        self.logger.addHandler(consoleHandler)
        
        self.logger.setLevel(cfg.allnet.loglevel)
        coloredlogs.install(level=cfg.allnet.loglevel, logger=self.logger, fmt=log_fmt_str)

        self.logger.info("Allnet started")

        for root, dirs, files in os.walk("./aime/titles"):
            for dir in dirs: 
                if not dir.startswith("__"):
                    try:
                        mod = importlib.import_module(f"aime.titles.{dir}")
                        
                        try:
                            if self.config.server.develop:
                                self.register(mod.game_code, mod.dev_uri_hosts, f"{cfg_dir}/{mod.config_name}", mod.dev_alt_uri_hosts)

                            else:
                                self.register(mod.game_code, mod.uri_hosts, f"{cfg_dir}/{mod.config_name}", mod.alt_uri_hosts)

                        except Exception as e:
                            self.logger.warning(f"Could not load title server info from {dir} - {e}")

                    except ImportError as e:
                        self.logger.warning(f"Failed to import from dir {dir} - {e}")
            break

        self.logger.info(f"Registered {len(registry)} game startup urls and alts")
    
    def render_POST(self, request):
        request.responseHeaders.addRawHeader(b"content-type", b"text/plain;charset=utf-8")
        request.responseHeaders.removeHeader(b"server")

        url = request.uri.decode()
        urlSplit = url.split("/")

        if url == "/report-api/Report":
            return self.deliver.receive_delivery_report(json.loads(request.content.getvalue().decode()), request.getClientIP())

        try:
            req_raw = request.content.getvalue().decode()
            req_data = self.aime_req_preprocessing(req_raw)
        except:
            self.logger.warn(f"Error decoding allnet request: {request.uri} - {request.content.getvalue()}")
            return b""

        try:
            handler = getattr(self, f"handle_{urlSplit[1]}_{urlSplit[2]}_{urlSplit[3]}_request")
            processed = self.aime_req_postprocessing(handler(req_data, request.getClientIP())).encode("utf-8")
            return processed
        except AttributeError as e:
            self.logger.warn(f"Unhandled method {url} - {e}")
            return b""

    def render_GET(self, request):
        if request.uri.decode() == "/naomitest.html":
            self.logger.info(f"Naominet service test from {request.getClientIP()}")
            return b"naomi ok"

        elif request.uri.decode().startswith("/deliver/content"):            
            ret = self.deliver.get_delivery_content(request.uri.decode(), request.getClientIP())

            request.responseHeaders.addRawHeader(b"content-type", b"binary/octet-stream")
            request.responseHeaders.addRawHeader(b"Accept-Ranges", b"bytes")
            request.responseHeaders.addRawHeader(b"content-length", len(ret))
            return ret

        elif request.uri.decode().startswith("/deliver/ini"):
            request.responseHeaders.addRawHeader(b"content-type", b"text/plain")
            return self.deliver.get_delivery_ini(request.uri.decode(), request.getClientIP())

        else:
            self.logger.debug(f"Allnet GET request, ip: {request.getClientIP()} url: {request.uri.decode()} body: {request.content.getvalue()}")
            return b""

    def handle_sys_servlet_PowerOn_request(self, data: Dict, ip: str) -> Dict:
        self.logger.info(f"Startup request: {ip} {data}")
        req = AllnetPowerOnRequest(data)

        if req.serial == "A69E-01A8888" and not self.config.server.allow_default_keychip:
            return {"stat": 0}

        if req.format_ver == 3:
            resp = AllnetPowerOnResponse3(req.token)
        else:
            resp = AllnetPowerOnResponse2()

        try:
            game_cfg = dict()
            game_cfg.update(yaml.safe_load(open(registry[req.game_id][1])))
            replacers = {"$v": req.ver.replace(".", ""), "$h": self.config.title.hostname, "$p": str(game_cfg["server"]["port"])}
            resp.uri = registry[req.game_id][0][0]
            resp.host = registry[req.game_id][0][1]

            # Check for games that use different URL schemes for different versions
            if f"{req.game_id}_alts" in registry:
                for k,v in registry[f"{req.game_id}_alts"][0].items():

                    if req.ver == k:
                        resp.uri = v[0]
                        resp.host = v[1]
                        break

        except KeyError:
            self.logger.error(f"Unsupported game {req.game_id}")
            return {"stat": 0}
        
        if req.serial != "A69E-01A8888":
            mach = self.data.arcade.get_machine(req.serial)
            
            if mach is None and not self.config.server.allow_any_keychip:
                self.logger.warn(f"Reject non-whitelisted keychip {req.serial}")
                return {"stat": 0}

            if mach is not None:
                arcade = self.data.arcade.get_arcade(mach["arcade"])
                mdata = json.loads(mach["data"])

                if "country" in mdata: resp.country = mdata["country"]
                if arcade["name"] is not None: resp.name = str(arcade["name"])
                if arcade["description"] is not None: resp.nickname = str(arcade["description"])

        for k,v in replacers.items():
            resp.uri = resp.uri.replace(k,v)
            resp.host = resp.host.replace(k,v)
        
        self.logger.info(f"Startup response: {vars(resp)}")

        return vars(resp)

    def handle_sys_servlet_DownloadOrder_request(self, data: Dict, ip: str) -> Dict:
        self.logger.info(f"DownloadOrder request: {ip} {data}")
        req = AllnetDownloadOrderRequest(data["game_id"], data["ver"], data["serial"], data["encode"])
        resp = AllnetDownloadOrderResponse(serial=req.serial)

        if self.deliver is not None:
            resp.uri = self.deliver.get_delivery_ini_url(req.game_id, req.ver, req.serial, ip)

        self.logger.info(f"DownloadOrder response {vars(resp)}")
        return vars(resp)

    def aime_req_preprocessing(self, data: str) -> Dict:
        kvp_dict = {}
        zip = base64.b64decode(data)
        unzip = zlib.decompress(zip)
        kvp = unzip.decode('utf-8')[:-2].split("&") # go from bytes obj to str, remove the /r/n, and split on &

        for val in kvp:
            split = val.split("=")
            kvp_dict[split[0]] = split[1]
        
        return kvp_dict

    def aime_req_postprocessing(self, data: Dict) -> str:
        res_str = ""
        for key, val in data.items():
            res_str += f"{key}={val}&"
        res_str = res_str[:-1] + '\n'

        return res_str

    def register(self, game: str, uri_hosts: tuple, cfg_file: str, alts: Dict = None) -> None:
        registry[game] = (uri_hosts, cfg_file)
        if alts is not None:
            registry[f"{game}_alts"] = (alts, cfg_file)

class AllnetPowerOnRequest():
    def __init__(self, req: Dict) -> None:
        self.game_id = req["game_id"]
        self.ver = req["ver"]
        self.serial = req["serial"]
        self.ip = req["ip"]
        self.firm_ver = req["firm_ver"]
        self.boot_ver = req["boot_ver"]
        self.encode = req["encode"]
        
        try:
            self.format_ver = int(req["format_ver"])
        except:
            self.format_ver = 2
        self.hops = int(req["hops"])

        try:
            self.token = int(req["token"])
        except:
            self.token = ""

class AllnetPowerOnResponse3():
    def __init__(self, token) -> None:
        self.stat = 1
        self.uri = ""
        self.host = ""
        self.place_id = "123"
        self.name = ""
        self.nickname = ""
        self.region0 = "1"
        self.region_name0 = "W"
        self.region_name1 = "X"
        self.region_name2 = "Y"
        self.region_name3 = "Z"
        self.country = "JPN"
        self.allnet_id = "123"
        self.client_timezone = "+0900"
        self.utc_time = datetime.now(tz=pytz.timezone('UTC')).strftime("%Y-%m-%dT%H:%M:%SZ")
        self.setting = ""
        self.res_ver = "3"
        self.token = str(token)

class AllnetPowerOnResponse2():
    def __init__(self) -> None:
        self.stat = 1
        self.uri = ""
        self.host = ""
        self.place_id = "123"
        self.name = ""
        self.nickname = ""
        self.region0 = "1"
        self.region_name0 = "W"
        self.region_name1 = "X"
        self.region_name2 = "Y"
        self.region_name3 = "Z"
        self.country = "JPN"
        self.year = datetime.now().year
        self.month = datetime.now().month
        self.day = datetime.now().day
        self.hour = datetime.now().hour
        self.minute = datetime.now().minute
        self.second = datetime.now().second
        self.setting = "1"
        self.timezone = "+09:00"
        self.res_class = "PowerOnResponseV2"

class AllnetDownloadOrderRequest():
    def __init__(self, game_id: str = "", ver: str = "", serial: str = "", encode: str = "UTF-8") -> None:
        self.game_id = game_id
        self.ver = ver
        self.serial = serial
        self.encode = encode

class AllnetDownloadOrderResponse():
    def __init__(self, stat: int = 1, serial: str = "", uri: str = "null") -> None:
        self.stat = stat
        self.serial = serial
        self.uri = uri
