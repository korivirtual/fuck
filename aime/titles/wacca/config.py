from typing import Dict, List
from aime.data import Config

class WaccaServerConfig():
    def __init__(self, parent_config: "WaccaConfig") -> None:
        self.__config = parent_config
    
    @property
    def enable(self) -> bool:
        return bool(self.__config.get('server', {}).get('enable', True))
        
    @property
    def port(self) -> int:
        return int(self.__config.get('server', {}).get('port', 9002))
    
    @property
    def loglevel(self) -> int:
        return Config.str_to_loglevel(self.__config.get('server', {}).get('loglevel', "info"))

class WaccaConfig(dict):
    def __init__(self) -> None:
        self.server = WaccaServerConfig(self)
    
    @property
    def safe_song_load(self) -> bool:
        return bool(self.get('safe_song_load', True))

    @property
    def always_vip(self) -> bool:
        return bool(self.get('always_vip', True))
    
    @property
    def enabled_gates(self) -> List[int]:
        return self.get('enabled_gates', [])