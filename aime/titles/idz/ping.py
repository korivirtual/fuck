import logging

from twisted.internet.protocol import DatagramProtocol

from aime.data import Config, Data
from aime.titles.idz.config import IDZConfig

class IDZPing(DatagramProtocol):
    def __init__(self, cfg: Config, game_cfg: IDZConfig, port:int) -> None:
        super().__init__()
        self.port = port
        self.core_config = cfg
        self.game_config = game_cfg
        self.logger = logging.getLogger("idz")

    def datagramReceived(self, data, addr):
        self.logger.info(f"Ping from from {addr[0]}:{addr[1]} -> {self.port} - {data.hex()}")
        self.transport.write(data, addr)