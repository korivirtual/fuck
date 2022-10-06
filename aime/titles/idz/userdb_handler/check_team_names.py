import struct

from aime.titles.idz.userdb_handler.base import IDZHandlerBase
from aime.data import Config
from aime.titles.idz.config import IDZConfig

class IDZHandlerCheckTeamName1(IDZHandlerBase):
    cmd_code = bytes.fromhex("00a2")
    rsp_code = bytes.fromhex("00a3")
    name = "check_team_name1"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x0010
    
    def handle(self, data: bytes) -> bytearray:
        ret = super().handle(data)
        return self.handle_common(ret)

    def handle_common(cls, data: bytearray) -> bytearray:
        struct.pack_into("<I", data, 0x4, 0x1)
        return data


class IDZHandlerCheckTeamName2(IDZHandlerBase):
    cmd_code = bytes.fromhex("0097")
    rsp_code = bytes.fromhex("0098")
    name = "check_team_name1"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x0010

    def handle(self, data: bytes) -> bytearray:
        ret = super().handle(data)
        return IDZHandlerCheckTeamName1.handle_common(self, ret)

