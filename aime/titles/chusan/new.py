from datetime import datetime, timedelta
from typing import Dict
import pytz

from aime.data import Config
from aime.titles.chusan.base import ChusanBase
from aime.titles.chusan.const import ChusanConstants

from aime.titles.chusan.data.events import EVENTS_NEW

class ChusanNew(ChusanBase):
    def __init__(self, core_cfg: Config, game_cfg: Config) -> None:
        super().__init__(core_cfg, game_cfg)
        self.version = ChusanConstants.VER_CHUNITHM_NEW
    
    def handle_get_game_setting_api_request(self, data: Dict) -> Dict:
        ret = super().handle_get_game_setting_api_request(data)
        ret["gameSetting"]["romVersion"] = "2.00.00"
        ret["gameSetting"]["dataVersion"] = "2.00.00"
        ret["gameSetting"]["matchingUri"] = f"http://{self.core_cfg.server.hostname}:{self.game_cfg.server.port}/200/ChuniServlet/"
        ret["gameSetting"]["matchingUriX"] = f"http://{self.core_cfg.server.hostname}:{self.game_cfg.server.port}/200/ChuniServlet/"
        ret["gameSetting"]["udpHolePunchUri"] = f"http://{self.core_cfg.server.hostname}:{self.game_cfg.server.port}/200/ChuniServlet/"
        ret["gameSetting"]["reflectorUri"] = f"http://{self.core_cfg.server.hostname}:{self.game_cfg.server.port}/200/ChuniServlet/"
        return ret

    def handle_get_game_event_api_request(self, data: Dict) -> Dict:
        game_events: list[str, Any] = []
        for event in EVENTS_NEW:
                game_events.append({
                "type": event["type"], 
                "id": event["id"], 
                "startDate": "2017-12-05 07:00:00.0", 
                "endDate": "2099-12-31 00:00:00.0"})
        return {
            "type": data["type"], 
            "length": len(game_events), 
            "gameEventList": game_events
        }
