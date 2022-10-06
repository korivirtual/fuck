from operator import indexOf
import struct
import json
from random import choice, randrange

from aime.titles.idz.userdb_handler.base import IDZHandlerBase
from aime.titles.idz.userdb_handler.load_team import IDZHandlerLoadTeam1
from aime.data import Config
from aime.titles.idz.config import IDZConfig

AUTO_TEAM_NAMES = ["スピードスターズ", "レッドサンズ", "ナイトキッズ"]
FULL_WIDTH_NUMS = ["\uff10", "\uff11", "\uff12", "\uff13", "\uff14", "\uff15", "\uff16", "\uff17", "\uff18", "\uff19"]

class IDZHandlerCreateAutoTeam1(IDZHandlerBase):
    cmd_code = bytes.fromhex("007b")
    cmd_code = bytes.fromhex("007c")
    name = "create_auto_team1"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x0ca0
    
    def handle(self, data: bytes) -> bytearray:
        ret = super().handle(data)
        return ret
    
    def handle_common(cls, data: bytearray, ret: bytearray) -> bytearray:
        aime_id = struct.unpack_from("<I", data, 0x04)[0]
        name = choice(AUTO_TEAM_NAMES)
        bg = indexOf(AUTO_TEAM_NAMES, name)
        number = choice(FULL_WIDTH_NUMS) + choice(FULL_WIDTH_NUMS) + choice(FULL_WIDTH_NUMS)

        tdata = {
            "id": aime_id,
            "bg": bg,
            "fx": 0,
        }

        cls.data.game.put_profile(aime_id, cls.game, cls.version, data=tdata, name=(name + number))
        
        tdata = {
            "id": aime_id,
            "name": (name + number),
            "bg": bg,
            "fx": 0,
        }
        tname = tdata['name'].encode("shift-jis")

        struct.pack_into("<I", ret, 0x0C, tdata["id"])
        struct.pack_into(f"{len(tname)}s", ret, 0x24, tname)
        struct.pack_into("<I", ret, 0x80, tdata["id"])
        struct.pack_into(f"<I", ret, 0xD8, tdata["bg"])
        struct.pack_into(f"<I", ret, 0xDC, tdata["fx"])

        return ret


class IDZHandlerCreateAutoTeam2(IDZHandlerBase):
    cmd_code = bytes.fromhex("0077")
    rsp_code = bytes.fromhex("0078")
    name = "create_auto_team2"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x0ca0
    
    def handle(self, data: bytes) -> bytearray:
        ret = super().handle(data)
        return IDZHandlerCreateAutoTeam1.handle_common(self, data, ret)

class IDZHandlerCreateAutoTeam3(IDZHandlerBase):
    cmd_code = bytes.fromhex("0077")
    rsp_code = bytes.fromhex("0078")
    name = "create_auto_team3"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x0ca0
    
    def handle(self, data: bytes) -> bytearray:
        ret = super().handle(data)
        return IDZHandlerCreateAutoTeam1.handle_common(self, data, ret)