import struct

from aime.titles.idz.userdb_handler.base import IDZHandlerBase
from aime.data import Config
from aime.titles.idz.config import IDZConfig

class IDZHandlerLoadProfile1(IDZHandlerBase):
    cmd_code = bytes.fromhex("0067")
    rsp_code = bytes.fromhex("0065")
    name = "load_profile1"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x0d30
    
    def handle(self, data: bytes) -> bytearray:
        ret = super().handle(data)
        aime_id = struct.unpack_from("<L", data, 0x04)[0]
        return ret

class IDZHandlerLoadProfile2(IDZHandlerBase):
    cmd_code = bytes.fromhex("012f")
    rsp_code = bytes.fromhex("012e")
    name = "load_profile2"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x0ea0
    
    def handle(self, data: bytes) -> bytearray:
        ret = super().handle(data)
        aime_id = struct.unpack_from("<L", data, 0x04)[0]
        return ret

class IDZHandlerLoadProfile3(IDZHandlerBase):
    cmd_code = bytes.fromhex("012f")
    rsp_code = bytes.fromhex("012e")
    name = "load_profile2"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x1360
    
    def handle(self, data: bytes) -> bytearray:
        ret = super().handle(data)
        aime_id = struct.unpack_from("<L", data, 0x04)[0]
        return ret

class IDZHandlerLoadProfile4(IDZHandlerBase):
    cmd_code = bytes.fromhex("0142")
    rsp_code = bytes.fromhex("0141")
    name = "load_profile4"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x1640
    
    def handle(self, data: bytes) -> bytearray:
        ret = super().handle(data)
        aime_id = struct.unpack_from("<L", data, 0x04)[0]
        return ret