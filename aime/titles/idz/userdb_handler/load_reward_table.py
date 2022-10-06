import struct

from aime.titles.idz.userdb_handler.base import IDZHandlerBase
from aime.data import Config
from aime.titles.idz.config import IDZConfig

class IDZHandlerLoadRewardTable1(IDZHandlerBase):
    cmd_code = bytes.fromhex("0086")
    rsp_code = bytes.fromhex("0087")
    name = "load_reward_table1"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x01c0
    
    def handle(self, data: bytes) -> bytearray:
        return super().handle(data)

class IDZHandlerLoadRewardTable2(IDZHandlerBase):
    cmd_code = bytes.fromhex("007F")
    rsp_code = bytes.fromhex("0080")
    name = "load_reward_table2"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x01c0
    
    def handle(self, data: bytes) -> bytearray:
        return super().handle(data)
