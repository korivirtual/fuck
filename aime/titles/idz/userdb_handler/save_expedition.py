from aime.titles.idz.userdb_handler.base import IDZHandlerBase
from aime.data import Config
from aime.titles.idz.config import IDZConfig

class IDZHandlerSaveExpedition1(IDZHandlerBase):
    cmd_code = bytes.fromhex("008c")
    rsp_code = bytes.fromhex("0001")
    name = "save_expedition1"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        #self.size = 0x17c0
    
    def handle(self, data: bytes) -> bytearray:
        return super().handle(data)

class IDZHandlerSaveExpedition2(IDZHandlerBase):
    cmd_code = bytes.fromhex("013f")
    rsp_code = bytes.fromhex("0001")
    name = "save_expedition2"

    def __init__(self, core_cfg: Config, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        #self.size = 0x18ac
    
    def handle(self, data: bytes) -> bytearray:
        return super().handle(data)