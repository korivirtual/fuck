from aime.data import Config

class IDACServerConfig():
    def __init__(self, parent: "IDACConfig") -> None:
        self.__config = parent

    @property
    def enable(self) -> bool:
        return bool(self.__config.get('server', {}).get('enable', True))
    
    @property
    def loglevel(self) -> int:
        return Config.str_to_loglevel(self.__config.get('server', {}).get('loglevel', "info"))

    @property
    def ssl(self) -> bool:
        return bool(self.__config.get('server', {}).get('ssl', False))

    @property
    def ssl_key(self) -> str:
        return self.__config.get('server', {}).get('ssl_key', 'cert/title.key')

    @property
    def ssl_cert(self) -> str:
        return self.__config.get('server', {}).get('ssl_cert', 'cert/title.crt')

class IDACPortConfig():
    def __init__(self, parent: "IDACConfig") -> None:
        self.__config = parent

    @property
    def main(self) -> int:
        return int(self.__config.get('ports', {}).get('main', 9009))

    @property
    def matching(self) -> int:
        return int(self.__config.get('ports', {}).get('matching', 20001))

    @property
    def echo1(self) -> int:
        return int(self.__config.get('ports', {}).get('echo1', 20002))

    @property
    def echo2(self) -> int:
        return int(self.__config.get('ports', {}).get('echo2', 20003))

class IDACConfig(dict):
    def __init__(self) -> None:
        self.server = IDACServerConfig(self)
        self.ports = IDACPortConfig(self)