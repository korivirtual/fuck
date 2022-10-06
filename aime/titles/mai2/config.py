from aime.data import Config

class Mai2ServerConfig():
    def __init__(self, parent: "Mai2Config") -> None:
        self.__config = parent

    @property
    def enable(self) -> bool:
        return bool(self.__config.get('server', {}).get('enable', True))
        
    @property
    def port(self) -> int:
        return int(self.__config.get('server', {}).get('port', 9004))
    
    @property
    def loglevel(self) -> int:
        return Config.str_to_loglevel(self.__config.get('server', {}).get('loglevel', "info"))

class Mai2Config(dict):
    def __init__(self) -> None:
        self.server = Mai2ServerConfig(self)