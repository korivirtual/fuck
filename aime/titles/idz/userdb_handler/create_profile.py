import json
import struct
from datetime import datetime

from aime.titles.idz.userdb_handler.base import IDZHandlerBase
from aime.data import Config
from aime.titles.idz.config import IDZConfig

class IDZHandlerCreateProfile1(IDZHandlerBase):
    cmd_code = bytes.fromhex("0066")
    rsp_code = bytes.fromhex("0067")
    name = "create_profile1"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x0020
    
    def handle(self, data: bytes) -> bytearray:
        ret = super().handle(data)
        return self.handle_common(data, ret)

    def handle_common(cls, req: bytes, ret: bytearray):
        aime_id = struct.unpack_from("<L", req, 0x04)[0]
        name = req[0x1E:0x0034].decode("shift-jis").replace("\x00", "")
        car = req[0x40:0xa0].hex()
        chara = req[0xa8:0xbc].hex()

        auto_team = cls.data.game.get_profile(cls.game, cls.version, user_id=aime_id)
        if not auto_team:
            team = {
                "bg": 0,
                "id": 0,
                "shop": ""
            }
        else:
            tdata = json.loads(auto_team["data"])
            
            team = {
                "bg": tdata["bg"],
                "id": tdata["fx"],
                "shop": ""
            }

        cls.data.game.put_profile(aime_id, cls.game, cls.version, name=name, data={
            "profile": {
                "xp": 0,
                "lv": 1,
                "fame": 0,
                "dpoint": 0,
                "milage": 0,
                "playstamps": 0,
                "last_login": int(datetime.now().timestamp()),
                "car_str": car, # These should probably be chaged to dicts
                "chara_str": chara, # But this works for now...
            },

            "options": {
                "music": 0,
                "pack": 13640,
                "aura": 0,
                "paper_cup": 0,
                "gauges": 5,
                "driving_style": 0
            },

            "missions": {
                "team": [],
                "solo": []
            },

            "story": {
                "x": 0,
                "y": 0,
                "rows": {}
            },

            "unlocks": {
                "auras": 1,
                "cup": 0,
                "gauges": 32,
                "music": 0,
                "last_mileage_reward": 0,
            },
            "team": team
        })
        
        if cls.version > 2:
            struct.pack_into("<L", ret, 0x04, aime_id)
        else:
            struct.pack_into("<L", ret, 0x08, aime_id)
        return ret


class IDZHandlerCreateProfile2(IDZHandlerBase):
    cmd_code = bytes.fromhex("0064")
    rsp_code = bytes.fromhex("0065")
    name = "create_profile2"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x0020
    
    def handle(self, data: bytes) -> bytearray:
        ret = super().handle(data)
        return IDZHandlerCreateProfile1.handle_common(self, data, ret)

class IDZHandlerCreateProfile3(IDZHandlerBase):
    cmd_code = bytes.fromhex("0064")
    rsp_code = bytes.fromhex("0065")
    name = "create_profile3"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x0030
    
    def handle(self, data: bytes) -> bytearray:
        ret = super().handle(data)
        return IDZHandlerCreateProfile1.handle_common(self, data, ret)