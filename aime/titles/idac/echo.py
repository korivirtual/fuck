import logging

from twisted.internet.protocol import DatagramProtocol
from socketserver import BaseRequestHandler, TCPServer
import socket
from typing import Tuple

from aime.data import Config, Data
from aime.titles.idac.config import IDACConfig

class IDACEchoUDP(DatagramProtocol):
    def __init__(self, cfg: Config, game_cfg: IDACConfig, port:int) -> None:
        super().__init__()
        self.port = port
        self.core_config = cfg
        self.game_config = game_cfg
        self.logger = logging.getLogger("idac")

    def datagramReceived(self, data, addr):
        self.logger.info(f"UDP Ping from from {addr[0]}:{addr[1]} -> {self.port} - {data.hex()}")
        self.transport.write(data, addr)

class IDACEchoTCP(BaseRequestHandler):
    def __init__(self, request, client_address, server, cfg: Config, game_cfg: IDACConfig) -> None:
        self.core_config = cfg
        self.game_config = game_cfg
        self.logger = logging.getLogger("idac")
        self.data = Data(cfg)
        super().__init__(request, client_address, server)
    
    def handle(self):
        data = self.request.recv(1024).strip()
        self.logger.debug(f"TCP Ping from {self.client_address[0]}:{self.client_address[1]} -> {self.server.server_address[1]}: {data.hex()}")
        self.request.sendall(data)
        self.request.shutdown(socket.SHUT_WR)

class IDACEchoTCPFactory(TCPServer):
    def __init__(self, server_address: Tuple[str, int], RequestHandlerClass, cfg: Config, game_cfg: IDACConfig, bind_and_activate: bool = ...) -> None:
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)
        self.core_config = cfg
        self.game_config = game_cfg

    def finish_request(self, request, client_address):
        self.RequestHandlerClass(request, client_address, self, self.core_config, self.game_config)