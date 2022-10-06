from aime.data import Config

class IDZServerConfig():
    def __init__(self, parent_config: "IDZConfig") -> None:
        self.__config = parent_config
    
    @property
    def enable(self) -> bool:
        return bool(self.__config.get('server', {}).get('enable', True))
    
    @property
    def loglevel(self) -> int:
        return Config.str_to_loglevel(self.__config.get('server', {}).get('loglevel', "info"))

    @property
    def port(self) -> int:
        return int(self.__config.get('ports', {}).get('userdb_tcp', 10000))

class IDZPortsConfig():
    def __init__(self, parent_config: "IDZConfig") -> None:
        self.__config = parent_config

    @property
    def userdb_http(self) -> int:
        return int(self.__config.get('ports', {}).get('userdb_http', 10002))
        
    @property
    def match_tcp(self) -> int:
        return int(self.__config.get('ports', {}).get('match_tcp', 10003))

    @property
    def match_udp_snd(self) -> int:
        return int(self.__config.get('ports', {}).get('match_udp_snd', 10004))

    @property
    def match_udp_rcv(self) -> int:
        return int(self.__config.get('ports', {}).get('match_udp_rcv', 10005))

    @property
    def tag_match_tcp(self) -> int:
        return int(self.__config.get('ports', {}).get('tag_match_tcp', 10006))

    @property
    def tag_match_udp_snd(self) -> int:
        return int(self.__config.get('ports', {}).get('tag_match_udp_snd', 10007))

    @property
    def tag_match_udp_rcv(self) -> int:
        return int(self.__config.get('ports', {}).get('tag_match_udp_rcv', 10008))

    @property
    def event_tcp(self) -> int:
        return int(self.__config.get('ports', {}).get('event_tcp', 10009))

    @property
    def screenshot_tcp(self) -> int:
        return int(self.__config.get('ports', {}).get('screenshot_tcp', 10010))

    @property
    def echo1_udp(self) -> int:
        return int(self.__config.get('ports', {}).get('echo1_udp', 10011))

    @property
    def echo2_udp(self) -> int:
        return int(self.__config.get('ports', {}).get('echo2_udp', 10012))

    @property
    def news_tcp(self) -> int:
        return int(self.__config.get('ports', {}).get('news_tcp', 10013))

    @property
    def error_tcp(self) -> int:
        return int(self.__config.get('ports', {}).get('error_tcp', 10013))

class IDZConfig(dict):
    def __init__(self) -> None:
        self.server = IDZServerConfig(self)
        self.ports = IDZPortsConfig(self)