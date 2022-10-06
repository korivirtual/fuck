import struct

from aime.titles.idz.userdb_handler.base import IDZHandlerBase
from aime.data import Config
from aime.titles.idz.config import IDZConfig

class IDZHandlerLoadGhost1(IDZHandlerBase):
    cmd_code = bytes.fromhex("00a0")
    rsp_code = bytes.fromhex("00a1")
    name = "load_ghost1"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x0070
    
    def handle(self, data: bytes) -> bytearray:
        ret = super().handle(data)
        return self.handle_common(ret)
    
    def handle_common(cls, data: bytearray) -> bytearray:
        struct.pack_into("<I", data, 0x02, 0x5)

        struct.pack_into("<L", data, 0x04, 0x0)
        struct.pack_into("<l", data, 0x08, -1)
        struct.pack_into("<L", data, 0x0C, 0x1D4C0)
        struct.pack_into("<L", data, 0x10, 0x1D4C0)
        struct.pack_into("<L", data, 0x14, 0x1D4C0)

        struct.pack_into("<L", data, 0x38, 0x0)
        struct.pack_into("<l", data, 0x3C, -1)
        struct.pack_into("<L", data, 0x40, 0x1D4C0)
        struct.pack_into("<L", data, 0x44, 0x1D4C0)
        struct.pack_into("<L", data, 0x48, 0x1D4C0)

        struct.pack_into("<L", data, 0x4C, 0x1D4C0)
        struct.pack_into("<i", data, 0x50, -1)
        struct.pack_into("<H", data, 0x52, 0)
        struct.pack_into("<H", data, 0x53, 0)
        struct.pack_into("<H", data, 0x54, 0)
        struct.pack_into("<H", data, 0x55, 0)
        struct.pack_into("<H", data, 0x58, 0)
        return data

class IDZHandlerLoadGhost2(IDZHandlerBase):
    cmd_code = bytes.fromhex("0095")
    rsp_code = bytes.fromhex("0096")
    name = "load_ghost2"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x0070
    
    def handle(self, data: bytes) -> bytearray:
        ret = super().handle(data)
        return IDZHandlerLoadGhost1.handle_common(self, ret)