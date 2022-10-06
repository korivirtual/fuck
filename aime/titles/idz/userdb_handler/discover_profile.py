import struct
from typing import Tuple, List, Dict

from aime.titles.idz.userdb_handler.base import IDZHandlerBase
from aime.data import Config
from aime.titles.idz.config import IDZConfig

class IDZHandlerDiscoverProfile1(IDZHandlerBase):
    cmd_code = bytes.fromhex("006b")
    rsp_code = bytes.fromhex("006c")
    name = "discover_profile1"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x0010
    
    def handle(self, data: bytes) -> bytearray:
        ret = super().handle(data)
        user_id = struct.unpack_from("<I", data, 0x04)[0]
        profile = self.data.game.get_profile(self.game, self.version, user_id=user_id)
        struct.pack_into("<H", ret, 0x04, int(profile is not None))
        return ret

class IDZHandlerDiscoverProfile2(IDZHandlerBase):
    cmd_code = bytes.fromhex("0067")
    rsp_code = bytes.fromhex("0068")
    name = "discover_profile2"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x0010
    
    def handle(self, data: bytes) -> bytearray:
        ret = super().handle(data)
        user_id = struct.unpack_from("<I", data, 0x04)[0]
        profile = self.data.game.get_profile(self.game, self.version, user_id=user_id)
        struct.pack_into("<H", ret, 0x04, int(profile is not None))
        return ret

class IDZHandlerDiscoverProfile3(IDZHandlerBase):
    cmd_code = bytes.fromhex("0067")
    rsp_code = bytes.fromhex("0068")
    name = "discover_profile3"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x0010
    
    def handle(self, data: bytes) -> bytearray:
        ret = super().handle(data)
        user_id = struct.unpack_from("<I", data, 0x04)[0]
        profile = self.data.game.get_profile(self.game, self.version, user_id=user_id)
        struct.pack_into("<H", ret, 0x04, int(profile is not None))
        return ret