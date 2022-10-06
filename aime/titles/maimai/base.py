from datetime import datetime, timedelta, date
import pytz
import json
from typing import Dict
import logging

from aime.data import Config, Data
from aime.titles.maimai.const import MaimaiConstants
from aime.titles.maimai.config import MaimaiConfig
class MaimaiBase():
    def __init__(self, core_cfg: Config, game_cfg: MaimaiConfig):
        self.core_cfg = core_cfg
        self.game_cfg = game_cfg
        self.data = Data(core_cfg)        
        self.game = MaimaiConstants.GAME_CODE
        self.version = MaimaiConstants.VER_MAIMAI_FINALE
        self.logger = logging.getLogger("maimai")
        self.date_time_format = "%Y-%m-%d %H:%M:%S"

    def handle_get_game_setting_api_request(self, data: Dict):
        reboot_start = date.strftime(datetime.now() - timedelta(hours=3), self.date_time_format)
        reboot_end = date.strftime(datetime.now() - timedelta(hours=2), self.date_time_format)
        return {
        "gameSetting": {
            "isMaintenance": "false",
            "requestInterval": 1800,
            "rebootStartTime": reboot_start,
            "rebootEndTime": reboot_end,
            "movieUploadLimit": 0,
            "movieStatus": 0,
            "movieServerUri": "",
            "deliverServerUri": "",
            # TODO: Differentiate between prod and dev urls
            "oldServerUri": f"http://{self.core_cfg.title.hostname}:{self.game_cfg.server.port}/MaimaiServlet/oldServer",
            "usbDlServerUri": "",      
            }
        }

    def handle_get_game_event_api_request(self, data: Dict) -> Dict:
        #events = self.data.static.get_game_events(self.game, self.version)
        #if events is None:
        events = []
        events.append({"type": data["type"], 
            "id": 100803, 
            "startDate": "2017-12-05 07:00:00.0", 
            "endDate": "2099-12-31 00:00:00.0"})

        return {"type":data["type"],"length":len(events),"gameEventList":events}
    
    def handle_get_game_ranking_api_request(self, data: Dict) -> Dict:
        return {"length": 0, "gameRankingList": []}
        
    def handle_upsert_client_setting_api_request(self, data: Dict) -> Dict:
        pass

    def handle_upsert_client_upload_api_request(self, data: Dict) -> Dict:
        pass

    def handle_upsert_client_bookkeeping_api_request(self, data: Dict) -> Dict:
        pass

    def handle_upsert_client_testmode_api_request(self, data: Dict) -> Dict:
        pass

    def handle_user_logout_api_request(self, data: Dict) -> Dict:
        pass
    
    def handle_get_user_preview_api_request(self, data: Dict) -> Dict:
        p = self.data.game.get_profile(self.game, self.version, user_id = data["userId"])
        if p is None: return {} # Register
        profile = json.loads(p["data"])

        return {
            "userId": data["userId"],            
            "userName": profile["userData"]["userName"],
            "isLogin": False,
            "lastGameId": profile["userData"]["lastGameId"],
            "lastDataVersion": profile["userData"]["lastDataVersion"],
            "lastRomVersion": profile["userData"]["lastRomVersion"],
            "lastLoginDate": profile["userData"]["lastLoginDate"],
            "lastPlayDate": profile["userData"]["lastPlayDate"],            
            "playerRating": profile["userData"]["playerRating"],
            "nameplateId": 0,            
            "iconId": profile["userData"]["iconId"],
            "trophyId": 0,
            "partnerId": profile["userData"]["partnerId"],
            "frameId": profile["userData"]["frameId"],
            "dispRate": profile["userOption"]["dispRate"], # 0: all, 1: disprate, 2: dispDan, 3: hide, 4: end
            "totalAwake": profile["userData"]["totalAwake"],
            "isNetMember": profile["userData"]["isNetMember"],
            "dailyBonusDate": profile["userData"]["dailyBonusDate"],
            "headPhoneVolume": profile["userOption"]["headPhoneVolume"],
            "isInherit": False
        }