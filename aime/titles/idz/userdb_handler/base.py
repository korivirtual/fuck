import logging
import struct
from aime.data import Config, Data
from aime.titles.idz.config import IDZConfig
from aime.titles.idz.const import IDZConstants

class IDZHandlerBase():
    name = "generic"
    cmd_code = bytes(0)
    rsp_code = bytes([1])

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        self.core_config = core_cfg
        self.game_cfg = game_cfg
        self.data = Data(core_cfg)
        self.logger = logging.getLogger("idz")
        self.game = IDZConstants.GAME_CODE
        self.version = version
        self.size = 0x30
    
    def handle(self, data: bytes) -> bytearray:
        ret = bytearray([0] * self.size)
        struct.pack_into("<H", ret, 0x0, int.from_bytes(self.rsp_code, "big"))
        return ret