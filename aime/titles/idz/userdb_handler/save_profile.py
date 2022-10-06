import struct

from aime.titles.idz.userdb_handler.base import IDZHandlerBase
from aime.data import Config
from aime.titles.idz.config import IDZConfig

class IDZHandlerSaveProfile1(IDZHandlerBase):
    cmd_code = bytes.fromhex("0068")
    name = "save_profile1"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
    
    def handle(self, data: bytes) -> bytearray:
        return super().handle(data)

class IDZHandlerSaveProfile2(IDZHandlerBase):
    cmd_code = bytes.fromhex("0138")
    name = "save_profile1"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
    
    def handle(self, data: bytes) -> bytearray:
        return super().handle(data)

class IDZHandlerSaveProfile3(IDZHandlerBase):
    cmd_code = bytes.fromhex("0138")
    name = "save_profile1"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
    
    def handle(self, data: bytes) -> bytearray:
        return super().handle(data)

class IDZHandlerSaveProfile4(IDZHandlerBase):
    cmd_code = bytes.fromhex("0143")
    name = "save_profile1"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
    
    def handle(self, data: bytes) -> bytearray:
        return super().handle(data)