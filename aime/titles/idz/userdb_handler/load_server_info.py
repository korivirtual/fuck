import struct

from aime.titles.idz.userdb_handler.base import IDZHandlerBase
from aime.data import Config
from aime.titles.idz.config import IDZConfig

class IDZHandlerLoadServerInfo1(IDZHandlerBase):
    cmd_code = bytes.fromhex("0006")
    rsp_code = bytes.fromhex("0007")
    name = "load_server_info1"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x04b0
    
    def handle(self, data: bytes) -> bytearray:
        ret = super().handle(data)
        
        news_str = f"http://{self.core_config.title.hostname}:{self.game_cfg.ports.news_tcp}"        
        err_str = f"http://{self.core_config.title.hostname}:{self.game_cfg.ports.error_tcp}"

        len_hostname = len(self.core_config.title.hostname)
        len_news = len(news_str)
        len_error = len(err_str)

        struct.pack_into("<I", ret, 0x2, 1) # Status
        struct.pack_into(f"{len_hostname}s", ret, 0x4, self.core_config.title.hostname.encode())
        struct.pack_into("<I", ret, 0x84, self.game_cfg.server.port)
        struct.pack_into("<I", ret, 0x86, self.game_cfg.ports.userdb_http)

        struct.pack_into(f"{len_hostname}s", ret, 0x88, self.core_config.title.hostname.encode())
        struct.pack_into("<I", ret, 0x108, self.game_cfg.ports.match_tcp)
        struct.pack_into("<I", ret, 0x10a, self.game_cfg.ports.match_udp_snd)
        struct.pack_into("<I", ret, 0x10c, self.game_cfg.ports.match_udp_rcv)

        struct.pack_into("<I", ret, 0x11e, self.game_cfg.ports.tag_match_tcp)
        struct.pack_into("<I", ret, 0x110, self.game_cfg.ports.tag_match_udp_snd)
        struct.pack_into("<I", ret, 0x112, self.game_cfg.ports.tag_match_udp_rcv)

        struct.pack_into(f"{len_hostname}s", ret, 0x114, self.core_config.title.hostname.encode())
        struct.pack_into("<I", ret, 0x194, self.game_cfg.ports.event_tcp)

        struct.pack_into(f"{len_hostname}s", ret, 0x0199, self.core_config.title.hostname.encode())
        struct.pack_into("<I", ret, 0x0219, self.game_cfg.ports.screenshot_tcp)

        struct.pack_into(f"{len_hostname}s", ret, 0x021c, self.core_config.title.hostname.encode())
        struct.pack_into(f"{len_hostname}s", ret, 0x029c, self.core_config.title.hostname.encode())
        struct.pack_into(f"{len_hostname}s", ret, 0x031c, self.core_config.title.hostname.encode())

        struct.pack_into("<I", ret, 0x39c, self.game_cfg.ports.echo1_udp)
        struct.pack_into("<I", ret, 0x39e, self.game_cfg.ports.echo2_udp)

        struct.pack_into(f"{len_news}s", ret, 0x03a0, news_str.encode())
        struct.pack_into(f"{len_error}s", ret, 0x0424, err_str.encode())

        return ret

class IDZHandlerLoadServerInfo2(IDZHandlerBase):
    cmd_code = bytes.fromhex("0006")
    rsp_code = bytes.fromhex("0007")
    name = "load_server_info2"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.cmd_code = bytes.fromhex("06")
        self.rsp_code = bytes.fromhex("07")
        self.size = 0x04b0
    
    def handle(self, data: bytes) -> bytearray:
        ret = super().handle(data)
        
        news_str = f"http://{self.core_config.title.hostname}:{self.game_cfg.ports.news_tcp}"        
        err_str = f"http://{self.core_config.title.hostname}:{self.game_cfg.ports.error_tcp}"

        len_hostname = len(self.core_config.title.hostname)
        len_news = len(news_str)
        len_error = len(err_str)

        struct.pack_into("<I", ret, 0x4, 1) # Status
        struct.pack_into(f"{len_hostname}s", ret, 0x6, self.core_config.title.hostname.encode())
        struct.pack_into("<I", ret, 0x86, self.game_cfg.server.port)
        struct.pack_into("<I", ret, 0x88, self.game_cfg.ports.userdb_http)

        struct.pack_into(f"{len_hostname}s", ret, 0x8a, self.core_config.title.hostname.encode())
        struct.pack_into("<I", ret, 0x10a, self.game_cfg.ports.match_tcp)
        struct.pack_into("<I", ret, 0x10c, self.game_cfg.ports.match_udp_snd)
        struct.pack_into("<I", ret, 0x10e, self.game_cfg.ports.match_udp_rcv)

        struct.pack_into("<I", ret, 0x110, self.game_cfg.ports.tag_match_tcp)
        struct.pack_into("<I", ret, 0x112, self.game_cfg.ports.tag_match_udp_snd)
        struct.pack_into("<I", ret, 0x114, self.game_cfg.ports.tag_match_udp_rcv)

        struct.pack_into(f"{len_hostname}s", ret, 0x116, self.core_config.title.hostname.encode())
        struct.pack_into("<I", ret, 0x196, self.game_cfg.ports.event_tcp)

        struct.pack_into(f"{len_hostname}s", ret, 0x019a, self.core_config.title.hostname.encode())
        struct.pack_into("<I", ret, 0x021a, self.game_cfg.ports.screenshot_tcp)

        struct.pack_into(f"{len_hostname}s", ret, 0x021e, self.core_config.title.hostname.encode())
        struct.pack_into(f"{len_hostname}s", ret, 0x029e, self.core_config.title.hostname.encode())
        struct.pack_into(f"{len_hostname}s", ret, 0x031e, self.core_config.title.hostname.encode())

        struct.pack_into("<I", ret, 0x39e, self.game_cfg.ports.echo1_udp)
        struct.pack_into("<I", ret, 0x3a0, self.game_cfg.ports.echo2_udp)

        struct.pack_into(f"{len_news}s", ret, 0x03a2, news_str.encode())
        struct.pack_into(f"{len_error}s", ret, 0x0426, err_str.encode())

        return ret
        
