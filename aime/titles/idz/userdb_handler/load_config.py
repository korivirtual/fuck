import struct

from aime.titles.idz.userdb_handler.base import IDZHandlerBase
from aime.data import Config
from aime.titles.idz.config import IDZConfig

class IDZHandlerLoadConfigA1(IDZHandlerBase):
    cmd_code = bytes.fromhex("0004")
    rsp_code = bytes.fromhex("0005")
    name = "load_config_a1"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x01a0
    
    def handle(self, data: bytes) -> bytearray:
        ret = super().handle(data)
        struct.pack_into("<H", ret, 0x02, 1)
        struct.pack_into("<I", ret, 0x16, 230)
        return ret

class IDZHandlerLoadConfigB1(IDZHandlerBase):
    cmd_code = bytes.fromhex("00a0")
    rsp_code = bytes.fromhex("00ac")
    name = "load_config_b1"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x0230
    
    def handle(self, data: bytes) -> bytearray:
        ret = super().handle(data)
        struct.pack_into("<H", ret, 0x02, 1)
        return ret

class IDZHandlerLoadConfigA2(IDZHandlerBase):
    cmd_code = bytes.fromhex("0004")
    rsp_code = bytes.fromhex("0005")
    name = "load_config_a2"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x05e0
    
    def handle(self, data: bytes) -> bytearray:
        ret = super().handle(data)
        struct.pack_into("<H", ret, 0x02, 1)
        struct.pack_into("<I", ret, 0x16, 230)
        return ret

class IDZHandlerLoadConfigB2(IDZHandlerBase):
    cmd_code = bytes.fromhex("00a0")
    rsp_code = bytes.fromhex("00a1")
    name = "load_config_b2"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x0240
    
    def handle(self, data: bytes) -> bytearray:
        ret = super().handle(data)
        struct.pack_into("<H", ret, 0x02, 1)
        return ret

class IDZHandlerLoadConfigA3(IDZHandlerBase):
    cmd_code = bytes.fromhex("0004")
    rsp_code = bytes.fromhex("0005")
    name = "load_config_a3"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x05e0
    
    def handle(self, data: bytes) -> bytearray:
        ret = super().handle(data)
        struct.pack_into("<H", ret, 0x02, 1)
        struct.pack_into("<I", ret, 0x16, 230)
        return ret