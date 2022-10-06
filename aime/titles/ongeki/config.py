from aime.data import Config

class OngekiServerConfig():
    def __init__(self, parent_config: "OngekiConfig") -> None:
        self.__config = parent_config
    
    @property
    def enable(self) -> bool:
        return bool(self.__config.get('server', {}).get('enable', True))
        
    @property
    def port(self) -> int:
        return int(self.__config.get('server', {}).get('port', 9005))
    
    @property
    def loglevel(self) -> int:
        return Config.str_to_loglevel(self.__config.get('server', {}).get('loglevel', "info"))

class OngekiConfig(dict):
    def __init__(self) -> None:
        self.server = OngekiServerConfig(self)
