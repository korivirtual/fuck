import struct

from aime.titles.idz.userdb_handler.base import IDZHandlerBase
from aime.data import Config
from aime.titles.idz.config import IDZConfig

class IDZHandlerUpdateStoryClearNum1(IDZHandlerBase):
    cmd_code = bytes.fromhex("007f")
    rsp_code = bytes.fromhex("0080")
    name = "update_story_clear_num1"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x0220
    
    def handle(self, data: bytes) -> bytearray:
        return super().handle(data)

class IDZHandlerUpdateStoryClearNum2(IDZHandlerBase):
    cmd_code = bytes.fromhex("097f")
    rsp_code = bytes.fromhex("013e")
    name = "update_story_clear_num2"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x04f0
    
    def handle(self, data: bytes) -> bytearray:
        return super().handle(data)

class IDZHandlerUpdateStoryClearNum3(IDZHandlerBase):
    cmd_code = bytes.fromhex("013d")
    rsp_code = bytes.fromhex("013e")
    name = "update_story_clear_num3"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x0510
    
    def handle(self, data: bytes) -> bytearray:
        return super().handle(data)

class IDZHandlerUpdateStoryClearNum4(IDZHandlerBase):
    cmd_code = bytes.fromhex("0144")
    rsp_code = bytes.fromhex("0145")
    name = "update_story_clear_num4"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x800
    
    def handle(self, data: bytes) -> bytearray:
        return super().handle(data)

