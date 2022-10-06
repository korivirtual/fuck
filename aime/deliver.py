import logging, coloredlogs, json
from random import randrange
from time import strftime
from logging.handlers import TimedRotatingFileHandler
from os.path import exists
from datetime import datetime
from typing import Any, Dict

from aime.data import Config, Data

class NetDeliver():
    def __init__(self, cfg: Config) -> None:
        self.config = cfg
        self.data = Data(cfg)
        self.logger = logging.getLogger("deliver")

        log_fmt_str = "[%(asctime)s] NetDeliver | %(levelname)s | %(message)s"
        log_fmt = logging.Formatter(log_fmt_str)        

        fileHandler = TimedRotatingFileHandler("{0}/{1}.log".format(self.config.server.logs, "allnet"), when="d", backupCount=10)
        fileHandler.setFormatter(log_fmt)
        
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(log_fmt)

        self.logger.addHandler(fileHandler)
        self.logger.addHandler(consoleHandler)
        
        self.logger.setLevel(cfg.allnet.loglevel)
        coloredlogs.install(level=cfg.allnet.loglevel, logger=self.logger, fmt=log_fmt_str)

        self.logger.info(f"NetDelivery service enabled, will serve from folder '{self.config.allnet.ota_config_folder}'")

    def get_delivery_ini_url(self, game: str, version: str, keychip: str, ip: str) -> str:
        cab = self.data.arcade.get_machine(keychip)

        if cab is not None:
            cab_data = json.loads(cab["data"])
            print(cab_data)

            if "ota_enable" in cab_data and cab_data["ota_enable"]:
                if exists(f"{self.config.allnet.ota_config_folder}/{game}-{version}.json"):
                    return f"http://{self.config.title.hostname}/deliver/ini/{game}-{version}"

                else:
                    self.logger.info(f"No update is available for {game} v{version}")
                    return "null"
                
            else:
                self.logger.warn(f"Machine with keychip {keychip} does not have OTA updates enabled!")
                return "null"

        else:
            self.logger.warn(f"Non-whitelisted keychip {keychip} sent download request!")
            return "null"
    
    def get_delivery_ini(self, url: str, ip: str) -> bytes:
        self.logger.info(f"Delivery ini request from {ip} -> {url}")
        url_split = url.split("/")
        file = url_split[-1]
        ret = ""

        if file == "":
            file = url_split[-2]

        file_formatted = file.replace("%0A", "")

        if exists(f"{self.config.allnet.ota_config_folder}/{file_formatted}.json"):
            
            
            with open(f"{self.config.allnet.ota_config_folder}/{file_formatted}.json", mode="r", encoding='utf8') as f:
                data = json.load(f)

                ret = f"[COMMON]\r\nDLFORMAT={data['install']['format_ver']}\r\nREPORT_INTERVAL=3600\r\nINTERVAL=5000,10000,15000,20000\r\n"
                ret += f"PART_SIZE=4096,8192,8192\r\nREPORT=http://{self.config.title.hostname}/report-api/Report\r\nRELEASE_WITH_OPTION=0\r\n"
                ret += f"CLOUD=000000000000000000000000000000000000000000000000\r\nRELEASE_TYPE=1\r\nBB_INTERVAL=1500,-1\r\nDSL_INTERVAL=1500,-1\r\n\r\n"
                
                ret += f"GAME_ID={data['game']['id']}\r\n"
                ret += f"GAME_DESC=\"{data['install']['description']}\"\r\n"
                ret += f"ORDER_TIME={datetime.strftime(datetime.now(), '%Y-%m-%dT%H:%M:%S')}\r\n"
                ret += f"RELEASE_TIME={datetime.strftime(datetime.fromtimestamp(data['install']['release_time']), '%Y-%m-%dT%H:%M:%S')}\r\n"
                ret += f"IMMEDIATELY_RELEASE={int(data['install']['immedate_release'])}\r\n"
                ret += f"DOWNLOAD_ID={randrange(1111111111,9999999999)}\r\n\r\n"

                for x in range(len(data['install']['files'])):
                    ret += f"INSTALL{x + 1}=http://{self.config.title.hostname}/deliver/content/{data['install']['files'][x]}\r\n"
                for x in range(len(data['install']['prereqs'])):
                    ret += f"EXIST{x + 1}={data['install']['prereqs'][x]}\r\n"

            return ret.encode(encoding='utf8')
        
        return b""
    
    def get_delivery_content(self, url: str, ip: str) -> bytes:
        self.logger.info(f"Content request: {ip} {url}")
        url_split = url.split("/")
        file = url_split[-1]
        ret = ""

        if file == "":
            file = url_split[-2]

        file_formatted = file.replace("%0A", "")

        with open(f"{self.config.allnet.ota_content_folder}/{file_formatted}", mode="rb") as f:
            ret = f.read()

        return ret

    def receive_delivery_report(self, data: Dict, ip: str) -> bytes:
        self.logger.info(f"Delivery report: {data}")
        return b""