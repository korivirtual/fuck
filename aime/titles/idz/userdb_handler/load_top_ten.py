import struct
from typing import Tuple, List, Dict

from aime.titles.idz.userdb_handler.base import IDZHandlerBase
from aime.data import Config
from aime.titles.idz.config import IDZConfig

class IDZHandlerLoadTopTen1(IDZHandlerBase):
    cmd_code = bytes.fromhex("012c")
    rsp_code = bytes.fromhex("00ce")
    name = "load_top_ten"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x1720
    
    def handle(self, data: bytes) -> bytearray:
        ret = super().handle(data)
        tracks_dates: List[Tuple[int, int]] = []
        for i in range(32):
            tracks_dates.append(
                (struct.unpack_from("<H", data, 0x04 + (2 * i))[0], "little", 
                struct.unpack_from("<I", data, 0x44 + (4 * i))[0], "little")
            )
        # TODO: Best scores
        for i in range (3):
            offset = 0x16c0 + 0x1c * i
            struct.pack_into("<B", ret, offset + 0x02, 0xff)

        return ret
    
    @classmethod
    def common_handle(cls, data: Dict) -> bytearray:
        """
        1 and 2 have the same output, but different input.
        This is so I don't have to write the same thing 500 times
        """
        pass

class IDZHandlerLoadTopTen2(IDZHandlerBase):
    cmd_code = bytes.fromhex("012c")
    rsp_code = bytes.fromhex("00ce")
    name = "load_top_ten"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x1720
    
    def handle(self, data: bytes) -> bytearray:
        ret = super().handle(data)
        tracks_dates: List[Tuple[int, int]] = []
        for i in range(32):
            tracks_dates.append(
                (struct.unpack_from("<H", data, 0x04 + (2 * i))[0], "little", 
                struct.unpack_from("<I", data, 0x44 + (4 * i))[0], "little")
            )
        # TODO: Best scores
        for i in range (3):
            offset = 0x16c0 + 0x1c * i
            struct.pack_into("<B", ret, offset + 0x02, 0xff)

        return ret

class IDZHandlerLoadTopTen3(IDZHandlerBase):
    cmd_code = bytes.fromhex("012c")
    rsp_code = bytes.fromhex("00ce")
    name = "load_top_ten"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x1720
    
    def handle(self, data: bytes) -> bytearray:
        ret = super().handle(data)

        tracks_dates: List[Tuple[int, int]] = []
        for i in range(32):
            tracks_dates.append(
                (struct.unpack_from("<H", data, 0x04 + (2 * i))[0], 
                struct.unpack_from("<I", data, 0x44 + (4 * i))[0])
            )
        for i in range (3):
            offset = 0x16c0 + 0x1c * i
            struct.pack_into("<B", ret, offset + 0x02, 0xff)

        return ret
    
    @classmethod
    def common_handle(cls, data: Dict = {}) -> bytearray:
        """
        3 and 4 have the same output, but different input.
        This is so I don't have to write the same thing 500 times
        """

        pass

class IDZHandlerLoadTopTen4(IDZHandlerBase):
    cmd_code = bytes.fromhex("012c")
    rsp_code = bytes.fromhex("00ce")
    name = "load_top_ten"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x1720
    
    def handle(self, data: bytes) -> bytearray:
        ret = super().handle(data)
        tracks_dates: List[Tuple[int, int]] = []
        for i in range(32):
            tracks_dates.append(
                (struct.unpack_from("<H", data, 0x04 + (2 * i))[0], "little", 
                struct.unpack_from("<I", data, 0x44 + (4 * i))[0], "little")
            )
        # TODO: Best scores
        for i in range (3):
            offset = 0x16c0 + 0x1c * i
            struct.pack_into("<B", ret, offset + 0x02, 0xff)

        return ret