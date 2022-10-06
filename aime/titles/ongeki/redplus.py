from typing import Dict

from aime.data import Config
from aime.titles.ongeki.base import OngekiBase
from aime.titles.ongeki.const import OngekiConstants

from aime.titles.ongeki.data.events import events_redplus

class OngekiRedPlus(OngekiBase):
    def __init__(self, core_cfg: Config, game_cfg: Config) -> None:
        super().__init__(core_cfg, game_cfg)
        self.version = OngekiConstants.VER_ONGEKI_RED_PLUS
    
    def handle_get_game_setting_api_request(self, data: Dict) -> Dict:
        ret = super().handle_get_game_setting_api_request(data)
        ret["gameSetting"]["dataVersion"] = "1.25.00"
        ret["gameSetting"]["onlineDataVersion"] = "1.25.00"
        ret["gameSetting"]["maxCountCharacter"] = 50
        ret["gameSetting"]["maxCountCard"] = 300
        ret["gameSetting"]["maxCountItem"] = 300
        ret["gameSetting"]["maxCountMusic"] = 50
        ret["gameSetting"]["maxCountMusicItem"] = 300
        ret["gameSetting"]["macCountRivalMusic"] = 300
        return ret

    def handle_get_game_event_api_request(self, data: Dict) -> Dict:
        game_events: list[str, Any] = []
        for event in events_redplus:
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
