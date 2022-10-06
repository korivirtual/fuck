
from aime.data import Config

class DivaServerConfig():
    def __init__(self, parent_config: "DivaConfig") -> None:
        self.__config = parent_config
    
    @property
    def enable(self) -> bool:
        return bool(self.__config.get('server', {}).get('enable', True))
        
    @property
    def port(self) -> int:
        return int(self.__config.get('server', {}).get('port', 9007))
    
    @property
    def loglevel(self) -> int:
        return Config.str_to_loglevel(self.__config.get('server', {}).get('loglevel', "info"))

class DivaConfig(dict):
    def __init__(self) -> None:
        self.server = DivaServerConfig(self)