from typing import Any, List, Dict
from datetime import datetime, timedelta
import pytz
import json

from aime.data import Config
from aime.titles.mai2.base import Mai2Base
from aime.titles.mai2.const import Mai2Constants
from aime.titles.mai2.config import Mai2Config

class Mai2Universe(Mai2Base):
    def __init__(self, cfg: Config, game_cfg: Mai2Config) -> None:
        super().__init__(cfg, game_cfg)
        self.version = Mai2Constants.VER_MAIMAI_DX_UNIVERSE