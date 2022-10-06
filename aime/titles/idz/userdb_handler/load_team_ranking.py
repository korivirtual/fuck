import struct

from aime.titles.idz.userdb_handler.base import IDZHandlerBase
from aime.data import Config
from aime.titles.idz.config import IDZConfig

class IDZHandlerLoadTeamRanking1(IDZHandlerBase):
    cmd_code = bytes.fromhex("00b9")
    rsp_code = bytes.fromhex("00b1")
    name = "load_team_ranking1"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x0ba0
    
    def handle(self, data: bytes) -> bytearray:
        return super().handle(data)

class IDZHandlerLoadTeamRanking2(IDZHandlerBase):
    cmd_code = bytes.fromhex("00a7")
    rsp_code = bytes.fromhex("00b1")
    name = "load_team_ranking2"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x0ba0
    
    def handle(self, data: bytes) -> bytearray:
        return super().handle(data)

class IDZHandlerLoadTeamRanking3(IDZHandlerBase):
    cmd_code = bytes.fromhex("00bb")
    rsp_code = bytes.fromhex("00a8")
    name = "load_team_ranking3"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x0ba0
    
    def handle(self, data: bytes) -> bytearray:
        return super().handle(data)

class IDZHandlerLoadTeamRanking4(IDZHandlerBase):
    cmd_code = bytes.fromhex("00a9")
    rsp_code = bytes.fromhex("00a8")
    name = "load_team_ranking4"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x0ba0
    
    def handle(self, data: bytes) -> bytearray:
        return super().handle(data)