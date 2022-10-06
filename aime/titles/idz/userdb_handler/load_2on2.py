import struct

from aime.titles.idz.userdb_handler.base import IDZHandlerBase
from aime.data import Config
from aime.titles.idz.config import IDZConfig

class IDZHandlerLoad2on21(IDZHandlerBase):
    cmd_code = bytes.fromhex("00b0")
    rsp_code = bytes.fromhex("00b1")
    name = "load_2on21"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x04c0
    
    def handle(self, data: bytes) -> bytearray:
        return super().handle(data)

class IDZHandlerLoad2on22(IDZHandlerBase):
    cmd_code = bytes.fromhex("0132")
    rsp_code = bytes.fromhex("0133")
    name = "load_2on22"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x04c0
    
    def handle(self, data: bytes) -> bytearray:
        return super().handle(data)

class IDZHandlerLoad2on23(IDZHandlerBase):
    cmd_code = bytes.fromhex("00a3")
    rsp_code = bytes.fromhex("00a4")
    name = "load_2on23"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x1290
    
    def handle(self, data: bytes) -> bytearray:
        return super().handle(data)

class IDZHandlerLoad2on24(IDZHandlerBase):
    cmd_code = bytes.fromhex("0132")
    rsp_code = bytes.fromhex("0133")
    name = "load_2on24"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x0540
    
    def handle(self, data: bytes) -> bytearray:
        return super().handle(data)