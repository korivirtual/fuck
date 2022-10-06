from aime.data import Config

class ChusanServerConfig():
    def __init__(self, parent_config: "ChusanConfig") -> None:
        self.__config = parent_config
    
    @property
    def enable(self) -> bool:
        return bool(self.__config.get('server', {}).get('enable', True))
        
    @property
    def port(self) -> int:
        return int(self.__config.get('server', {}).get('port', 9006))
    
    @property
    def loglevel(self) -> int:
        return Config.str_to_loglevel(self.__config.get('server', {}).get('loglevel', "info"))

class ChusanConfig(dict):
    def __init__(self) -> None:
        self.server = ChusanServerConfig(self)
