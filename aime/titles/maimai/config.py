from aime.data import Config

class MaimaiServerConfig():
    def __init__(self, parent_config: "MaimaiConfig") -> None:
        self.__config = parent_config
    
    @property
    def enable(self) -> bool:
        return bool(self.__config.get('server', {}).get('enable', True))
        
    @property
    def port(self) -> int:
        return int(self.__config.get('server', {}).get('port', 9008))
    
    @property
    def loglevel(self) -> int:
        return Config.str_to_loglevel(self.__config.get('server', {}).get('loglevel', "info"))

class MaimaiConfig(dict):
    def __init__(self) -> None:
        self.server = MaimaiServerConfig(self)