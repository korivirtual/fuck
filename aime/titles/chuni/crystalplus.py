from datetime import datetime, timedelta
from typing import Dict
import pytz

from aime.data import Config
from aime.titles.chuni.base import ChuniBase
from aime.titles.chuni.const import ChuniConstants

from aime.titles.chuni.data.events import EVENTS_CRYSTALPLUS

class ChuniCrystalPlus(ChuniBase):
    def __init__(self, core_cfg: Config, game_cfg: Config) -> None:
        super().__init__(core_cfg, game_cfg)
        self.version = ChuniConstants.VER_CHUNITHM_CRYSTAL_PLUS
    
    def handle_get_game_setting_api_request(self, data: Dict) -> Dict:
        ret =  super().handle_get_game_setting_api_request(data)
        ret["gameSetting"]["dataVersion"] = "1.45.00"
        return ret

    def handle_get_game_event_api_request(self, data: Dict) -> Dict:
        game_events: list[str, Any] = []
        for event in EVENTS_CRYSTALPLUS:
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