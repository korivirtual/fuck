from aime.data import Config

class ChuniServerConfig():
    def __init__(self, parent_config: "ChuniConfig") -> None:
        self.__config = parent_config
    
    @property
    def enable(self) -> bool:
        return bool(self.__config.get('server', {}).get('enable', True))
        
    @property
    def port(self) -> int:
        return int(self.__config.get('server', {}).get('port', 9001))
    
    @property
    def loglevel(self) -> int:
        return Config.str_to_loglevel(self.__config.get('server', {}).get('loglevel', "info"))

class ChuniConfig(dict):
    def __init__(self) -> None:
        self.server = ChuniServerConfig(self)