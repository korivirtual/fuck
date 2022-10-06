import struct

from aime.titles.idz.userdb_handler.base import IDZHandlerBase
from aime.data import Config
from aime.titles.idz.config import IDZConfig

class IDZHandlerSaveTopic1(IDZHandlerBase):
    cmd_code = bytes.fromhex("009A")
    rsp_code = bytes.fromhex("009B")
    name = "update_provisional_store_ranking1"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x05d0
    
    def handle(self, data: bytes) -> bytearray:
        return  super().handle(data)
    
    def handle_common(cls, aime_id: int, ret: bytearray) -> bytearray:
        pass

class IDZHandlerSaveTopic2(IDZHandlerBase):
    cmd_code = bytes.fromhex("0091")
    rsp_code = bytes.fromhex("0092")
    name = "update_provisional_store_ranking1"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x05d0
    
    def handle(self, data: bytes) -> bytearray:
        return  super().handle(data)