import logging
import struct
from socketserver import BaseRequestHandler, TCPServer
from typing import Tuple
import socket

from Crypto.Cipher import AES

from aime.data import Config, Data
from aime.titles.idz.config import IDZConfig
from aime.titles.idz.const import IDZConstants
from aime.titles.idz.util import slide_to_the_left
from aime.titles.idz.userdb_handler import v110, v130, v210, v230, IDZHandlerBase

class IDZUserdbTCP(BaseRequestHandler):
    rsa_key = {
        "N": 4922323266120814292574970172377860734034664704992758249880018618131907367614177800329506877981986877921220485681998287752778495334541127048495486311792061,
        "d": 1163847742215766215216916151663017691387519688859977157498780867776436010396072628219119707788340687440419444081289736279466637153082223960965411473296473,
        "e": 3961365081960959178294197133768419551060435043430437330799371731939550352626564261219865471710058480523874787120718634318364066605378505537556570049131337,
        "hashN": 2662304617,
    }

    aes_key = b"\xff\xdd\xee\xcc\xbb\xaa\x99\x88\x77\x66\x55\x44\x33\x22\x11\x00"
    cipher = AES.new(aes_key, AES.MODE_ECB)

    def __init__(self, request, client_address, server, cfg: Config, game_cfg: IDZConfig) -> None:
        self.core_config = cfg
        self.game_config = game_cfg
        self.logger = logging.getLogger("idz")
        self.data = Data(cfg)
        super().__init__(request, client_address, server)
    
    def handle(self):
        self.logger.debug(f"Userdb TCP connection {self.client_address[0]}:{self.client_address[1]} -> {self.server.server_address[0]}:{self.server.server_address[1]}")

        base = slide_to_the_left(self.aes_key)
        key_enc = pow(base, self.rsa_key["e"], self.rsa_key["N"])
        result = key_enc.to_bytes(0x40, "little") + struct.pack("<I", 0x01020304) + self.rsa_key["hashN"].to_bytes(4, "little")

        self.logger.debug(f"Userdb send hello {result.hex()}")

        try:
            self.request.sendall(result)

        except Exception as e:
            self.logger.error(f"Failed to send handshake - {e}")
            return 
        
        handshake_data = self.request.recv(1024).strip()
        req_data = self.request.recv(1024)
        try:
            handshake_decrypt = self.cipher.decrypt(handshake_data)
        except:
            self.logger.error(f"Recieved un-decryptable data {handshake_data}")
            self.request.shutdown(socket.SHUT_WR)
            return

        req_decrypt = self.cipher.decrypt(req_data)
        
        self.logger.debug(f"Userdb receive handshake {handshake_decrypt.hex()}")

        magic = struct.unpack_from("<I", handshake_decrypt, 0)[0]

        if magic == 0xFE78571D:
            self.logger.info(f"Userdb serverbox request {req_decrypt.hex()}")

            self.request.sendall(b"0")

        elif magic != 0x01020304:
            self.logger.error(f"Bad magic, ignoring {handshake_decrypt.hex()}")

        else:
            version = handshake_decrypt[16:19].decode()
            cmd = struct.unpack_from("<H", req_decrypt, 0)[0].to_bytes(2, "big")
            self.logger.info(f"Userdb receive v{version} request {req_decrypt.hex()} len {len(req_decrypt)} from {self.client_address[0]}:{self.client_address[1]}")

            ret = self.dispatch(cmd, version, req_decrypt)
            self.logger.info(f"Userdb send {ret[0]} response {ret[1].hex()} len {len(ret[1])}")

            ret_enc = self.cipher.encrypt(ret[1])
            self.request.sendall(ret_enc)

        
        self.request.shutdown(socket.SHUT_WR)
    
    def dispatch(self, cmd_code: bytes, version: int, data: bytes) -> Tuple[str, bytes]:
        # It may be cleaner if all the versions are seperate folders
        if version == "110":
            for cls in v110:
                if cmd_code in cls.cmd_code:
                    handler = cls(self.core_config, self.game_config, IDZConstants.VER_IDZ_V110)
                    return (cls.name, bytes(handler.handle(data)))

            self.logger.warn(f"Unhandled v{version} command! {cmd_code.hex()}")

        elif version == "130":
            for cls in v130:
                if cmd_code in cls.cmd_code:
                    handler = cls(self.core_config, self.game_config, IDZConstants.VER_IDZ_V130)
                    return (cls.name, bytes(handler.handle(data)))

            self.logger.warn(f"Unhandled v{version} command! {cmd_code.hex()}")

        elif version == "210":
            for cls in v210:
                if cmd_code in cls.cmd_code:
                    handler = cls(self.core_config, self.game_config, IDZConstants.VER_IDZ_V210)
                    return (cls.name, bytes(handler.handle(data)))

            self.logger.warn(f"Unhandled v{version} command! {cmd_code.hex()}")

        elif version == "230":
            for cls in v230:
                if cmd_code in cls.cmd_code:
                    handler = cls(self.core_config, self.game_config, IDZConstants.VER_IDZ_V230)
                    return (cls.name, bytes(handler.handle(data)))

            self.logger.warn(f"Unhandled v{version} command! {cmd_code.hex()}")

        else:
            self.logger.warn(f"Unhandled protocol version! {version}")

        handler = IDZHandlerBase(self.core_config, self.game_config, 0)
        return (IDZHandlerBase.name, bytes(handler.handle(data)))

class IDZUserdbTCPFactory(TCPServer):
    def __init__(self, server_address: Tuple[str, int], RequestHandlerClass, cfg: Config, game_cfg: IDZConfig, bind_and_activate: bool = ...) -> None:
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)
        self.core_config = cfg
        self.game_config = game_cfg

    def finish_request(self, request, client_address):
        """Finish one request by instantiating RequestHandlerClass."""
        self.RequestHandlerClass(request, client_address, self, self.core_config, self.game_config)
        
