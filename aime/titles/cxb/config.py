from aime.data import Config

class CxbServerConfig():
    def __init__(self, parent_config: "CxbConfig"):
        self.__config = parent_config
    
    @property
    def enable(self) -> bool:
        return bool(self.__config.get('server', {}).get('enable', True))
        
    @property
    def port(self) -> int:
        return int(self.__config.get('server', {}).get('port', 443))

    @property
    def hostname(self) -> str:
        return self.__config.get('server', {}).get('hostname', "localhost")
    
    @property
    def loglevel(self) -> int:
        return Config.str_to_loglevel(self.__config.get('server', {}).get('loglevel', "info"))
    
    @property
    def ssl_key(self) -> str:
        return self.__config.get('server', {}).get('ssl_key', 'cert/title.key')

    @property
    def ssl_cert(self) -> str:
        return self.__config.get('server', {}).get('ssl_cert', 'cert/title.crt')

class CxbConfig(dict):
    def __init__(self) -> None:
        self.server = CxbServerConfig(self)