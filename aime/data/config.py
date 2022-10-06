import logging

class ServerConfig:
    def __init__(self, parent_config: "Config") -> None:
        self.__config = parent_config
    
    @property
    def hostname(self) -> str:
        return str(self.__config.get('server', {}).get('hostname', '127.0.0.1'))
    
    @property
    def allow_any_keychip(self) -> bool:
        return bool(self.__config.get('server', {}).get('allow_any_keychip', True))

    @property
    def allow_default_keychip(self) -> bool:
        return bool(self.__config.get('server', {}).get('allow_default_keychip', True))
    
    @property
    def name(self) -> str:
        return str(self.__config.get('server', {}).get('name', "MegAime"))

    @property
    def develop(self) -> bool:
        return bool(self.__config.get('server', {}).get('develop', True))

    @property
    def logs(self) -> str:
        return str(self.__config.get('server', {}).get('logs', "log"))

class TitleConfig:
    def __init__(self, parent_config: "Config") -> None:
        self.__config = parent_config
    
    @property
    def loglevel(self) -> int:
        return Config.str_to_loglevel(str(self.__config.get('title', {}).get('loglevel', "info")))

    @property
    def hostname(self) -> str:
        return str(self.__config.get('title', {}).get('hostname', '127.0.0.1'))

class DatabaseConfig:
    def __init__(self, parent_config: "Config") -> None:
        self.__config = parent_config
    
    @property
    def host(self) -> str:
        return str(self.__config.get('database', {}).get('host', 'localhost'))
    
    @property
    def username(self) -> str:
        return str(self.__config.get('database', {}).get('username', 'aime'))

    @property
    def password(self) -> str:
        return str(self.__config.get('database', {}).get('password', 'aime'))

    @property
    def name(self) -> str:
        return str(self.__config.get('database', {}).get('name', 'aime'))

    @property
    def port(self) -> int:
        return int(self.__config.get('database', {}).get('port', 3306))

    @property
    def type(self) -> str:
        return self.__config.get('database', {}).get('type', "mysql")
    
    @property
    def sha2_password(self) -> bool:
        return bool(self.__config.get('database', {}).get('sha2_password', False))
    
    @property
    def loglevel(self) -> int:
        return Config.str_to_loglevel(str(self.__config.get('database', {}).get('loglevel', "info")))

class FrontendConfig:
    def __init__(self, parent_config: "Config") -> None:
        self.__config = parent_config
    
    @property
    def enable(self) -> int:
        return bool(self.__config.get('frontend', {}).get('enable', False))

    @property
    def port(self) -> int:
        return int(self.__config.get('frontend', {}).get('port', 8080))
    
    @property
    def https(self) -> bool:
        return str(self.__config.get('frontend', {}).get('https', False))

    @property
    def loglevel(self) -> int:
        return Config.str_to_loglevel(str(self.__config.get('frontend', {}).get('loglevel', "info")))
    
    @property
    def ssl_key(self) -> str:
        return (str(self.__config.get('frontend', {}).get('ssl_key', "")))

    @property
    def ssl_cert(self) -> str:
        return (str(self.__config.get('frontend', {}).get('ssl_cert', "")))

class AllnetConfig:
    def __init__(self, parent_config: "Config") -> None:
        self.__config = parent_config

    @property
    def loglevel(self) -> int:
        return Config.str_to_loglevel(str(self.__config.get('allnet', {}).get('loglevel', "info")))

    @property
    def ota_delivery(self) -> bool:
        return bool(self.__config.get('allnet', {}).get('ota_delivery', False))

    @property
    def ota_config_folder(self) -> str:
        return self.__config.get('allnet', {}).get('ota_config_folder', "deliver/ini")

    @property
    def ota_content_folder(self) -> str:
        return self.__config.get('allnet', {}).get('ota_content_folder', "deliver/content")

class BillingConfig:
    def __init__(self, parent_config: "Config") -> None:
        self.__config = parent_config

    @property
    def loglevel(self) -> int:
        return Config.str_to_loglevel(str(self.__config.get('billing', {}).get('loglevel', "info")))
    
    @property
    def ssl_key(self) -> str:
        return (str(self.__config.get('billing', {}).get('ssl_key', "cert/server.key")))

    @property
    def ssl_cert(self) -> str:
        return (str(self.__config.get('billing', {}).get('ssl_cert', "cert/server.pem")))
    
    @property
    def sign_key(self) -> str:
        return str(self.__config.get('billing', {}).get('sign_key', "cert/billing.key"))
        
class AimedbConfig:
    def __init__(self, parent_config: "Config") -> None:
        self.__config = parent_config

    @property
    def loglevel(self) -> int:
        return Config.str_to_loglevel(str(self.__config.get('aimedb', {}).get('loglevel', "info")))

    @property
    def key(self) -> str:
        return str(self.__config.get('aimedb', {}).get('key', ""))

class Config(dict):
    def __init__(self) -> None:
        self.server = ServerConfig(self)
        self.title = TitleConfig(self)
        self.database = DatabaseConfig(self)
        self.frontend = FrontendConfig(self)
        self.allnet = AllnetConfig(self)
        self.billing = BillingConfig(self)
        self.aimedb = AimedbConfig(self)
    
    @classmethod
    def str_to_loglevel(cls, level_str: str):
        if level_str == "error":
            return logging.ERROR
        elif level_str == "warn":
            return logging.WARN
        elif level_str == "debug":
            return logging.DEBUG
        else:
             return logging.INFO
