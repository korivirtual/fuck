from operator import indexOf
import struct
import json
from random import choice, randrange
from typing import Dict

from aime.titles.idz.userdb_handler.base import IDZHandlerBase
from aime.data import Config
from aime.titles.idz.config import IDZConfig

class IDZHandlerLoadTeam1(IDZHandlerBase):
    cmd_code = bytes.fromhex("0077")
    cmd_code = bytes.fromhex("0078")
    name = "load_team1"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x0ca0
    
    def handle(self, data: bytes) -> bytearray:
        ret = super().handle(data)
        return ret
    
    def handle_common(cls, data: Dict, ret: bytearray) -> bytearray:
        if not "name" in data or not data["name"]:
            # TODO: Load team from database
            pass
        
        tname = bytes(data["name"], "shift-jis")
        lname = bytes(data["leader_name"], "shift-jis")

        struct.pack_into("<I", ret, 0x0C, data["id"])
        struct.pack_into(f"{len(tname)}s", ret, 0x10, tname)
        struct.pack_into(f"{len(lname)}s", ret, 0x24, lname)
        struct.pack_into("<I", ret, 0x80, data["leader_id"])
        struct.pack_into(f"<I", ret, 0xD8, data["bg"])
        struct.pack_into(f"<I", ret, 0xDC, data["fx"])

        for x in range(0x00e0, 0x0102):
            struct.pack_into(f"<H", ret, x, 0xFF)
        
        for x in range(len(data["members"])):
            member: Dict = data["members"][x]

            if cls.version == 0:
                offset = 0x011c + (x * 0x005c)
            else:
                offset = 0x0120 + (x * 0x005c)
            
            name = bytes(member["name"], "shift-jis")
            chara_bytes = bytes.fromhex(member["chara"])

            struct.pack_into("<I", ret, offset, member["id"])
            struct.pack_into(f"{len(name)}s", ret, offset + 0x0004, name)
            struct.pack_into("<I", ret, offset + 0x18, member["lv"])
            struct.pack_into("<I", ret, offset + 0x34, member["last_login"])
            struct.pack_into(f"{len(chara_bytes)}s", ret, offset + 0x0044, chara_bytes)
        
        return ret

class IDZHandlerLoadTeam2(IDZHandlerBase):
    cmd_code = bytes.fromhex("0075")
    cmd_code = bytes.fromhex("0074")
    name = "load_team2"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x0ca0
    
    def handle(self, data: bytes) -> bytearray:
        ret = super().handle(data)
        return ret

class IDZHandlerLoadTeam3(IDZHandlerBase):
    cmd_code = bytes.fromhex("0075")
    cmd_code = bytes.fromhex("0074")
    name = "load_team3"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x0ca0
    
    def handle(self, data: bytes) -> bytearray:
        ret = super().handle(data)
        return ret