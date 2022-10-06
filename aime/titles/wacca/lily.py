from typing import Any, List, Dict
from datetime import datetime, timedelta
import json

from aime.data import Config
from aime.titles.wacca.base import WaccaBase
from aime.titles.wacca.config import WaccaConfig
from aime.titles.wacca.const import WaccaConstants

class WaccaLily(WaccaBase):
    def __init__(self, cfg: Config, game_cfg: WaccaConfig) -> None:
        super().__init__(cfg, game_cfg)
        self.version = WaccaConstants.VER_WACCA_LILY
        self.season = 2
    
    def handle_advertise_GetNews_request(self, data: Dict) -> List[Any]:
        return [
            # Notice name, title, message, something, something, show on title screen, welcome screen, start time, end time, voice?
            [], # Notices
            [], # Coppyright listings
            [], # Stopped song IDs
            [], # Stopped jacket IDs
            [], # Stopped movie IDs
            [], # Stopped icon IDs
            [], # Stopped product IDs
            [], # Stopped navigator IDs
            []  # Stopped navigator voice IDs
        ]