import struct
from typing import Dict
from datetime import datetime, timedelta

from aime.titles.idz.userdb_handler.base import IDZHandlerBase
from aime.data import Config
from aime.titles.idz.config import IDZConfig

class IDZHandlerLockProfile1(IDZHandlerBase):
    PROFILE_STATUS = {
        "LOCKED": 0,
        "UNLOCKED": 1,
        "OLD": 2
    }

    cmd_code = bytes.fromhex("0069")
    rsp_code = bytes.fromhex("006a")
    name = "lock_profile1"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x0020
    
    def handle(self, data: bytes) -> bytearray:
        ret = super().handle(data)
        profile_data = {
            "status": self.PROFILE_STATUS["UNLOCKED"], 
            "expire_time": int((datetime.now() + timedelta(hours=1)).timestamp() / 1000)
        }
        user_id = struct.unpack_from("<I", data, 0x04)[0]
        profile = self.data.game.get_profile(self.game, self.version, user_id=user_id)

        if profile is None and self.version > 0:
            old_profile = self.data.game.get_profile(self.game, self.version - 1, user_id=user_id)
            if old_profile is not None:
                profile_data["status"] = self.PROFILE_STATUS["OLD"]
        
        return self.handle_common(data, profile_data)
    
    def handle_common(cls, data: Dict, ret: bytearray) -> bytearray:
        struct.pack_into("<B", ret, 0x18, data["status"])
        struct.pack_into("<h", ret, 0x1a, -1)
        struct.pack_into("<I", ret, 0x1c, data["expire_time"])
        return ret

class IDZHandlerLockProfile2(IDZHandlerBase):
    cmd_code = bytes.fromhex("0065")
    rsp_code = bytes.fromhex("0066")
    name = "lock_profile2"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x0020
    
    def handle(self, data: bytes) -> bytearray:
        ret = super().handle(data)
        profile_data = {
            "status": IDZHandlerLockProfile1.PROFILE_STATUS["UNLOCKED"], 
            "expire_time": int((datetime.now() + timedelta(hours=1)).timestamp() / 1000)
        }
        user_id = struct.unpack_from("<I", data, 0x04)[0]
        profile = self.data.game.get_profile(self.game, self.version, user_id=user_id)

        if profile is None and self.version > 0:
            old_profile = self.data.game.get_profile(self.game, self.version - 1, user_id=user_id)
            if old_profile is not None:
                profile_data["status"] = IDZHandlerLockProfile1.PROFILE_STATUS["OLD"]
        
        return IDZHandlerLockProfile1.handle_common(self, profile_data, ret)
