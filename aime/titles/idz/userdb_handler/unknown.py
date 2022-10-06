import struct

from aime.titles.idz.userdb_handler.base import IDZHandlerBase
from aime.data import Config
from aime.titles.idz.config import IDZConfig

class IDZHandlerUnknown1(IDZHandlerBase):
    cmd_code = bytes.fromhex("00ad")
    name = "unknown1"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)

class IDZHandlerUnknown2(IDZHandlerBase):
    cmd_code = bytes.fromhex("00a2")
    name = "unknown2"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)