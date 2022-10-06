from twisted.internet.protocol import Factory, Protocol
import logging, coloredlogs
from Crypto.Cipher import AES
import struct
from logging.handlers import TimedRotatingFileHandler

from aime.data import Config, Data

class Aimedb(Protocol):
    AIMEDB_REQUEST_CODES = {
        "felica_lookup": 0x01,
        "lookup": 0x04,
        "register": 0x05,
        "log": 0x09,
        "campaign": 0x0b,
        "touch": 0x0d,
        "lookup2": 0x0f,
        "felica_lookup2": 0x11,
        "log2": 0x13,
        "hello": 0x64,
        "goodbye": 0x66
    }

    AIMEDB_RESPONSE_CODES = {
        "felica_lookup": 0x03,
        "lookup": 0x06,
        "log": 0x0a,
        "campaign": 0x0c,
        "touch": 0x0e,
        "lookup2": 0x10,
        "felica_lookup2": 0x12,
        "log2": 0x14,
        "hello": 0x65
    }

    def __init__(self, cfg: Config) -> None:
        super().__init__()
        self.config = cfg
        self.logger = logging.getLogger("aimedb")
        self.data = Data(cfg)

    def dataReceived(self, data):
        req = self.aimedb_preprocessing(data)
        cmd = req[4]
        resp = None

        if cmd == self.AIMEDB_REQUEST_CODES["goodbye"]:
            # Explicitly handle goodbye as it's a special case where no data is send
            self.logger.info("Goodbye")
            self.transport.loseConnection()
            return

        for k,v in self.AIMEDB_REQUEST_CODES.items():
            if cmd == v:
                #try: 
                    handler = getattr(self, f"handle_{k}_request")
                    self.logger.info(f"Received {k}")
                    resp = handler(req)
                #except:
                    #self.logger.error(f"Error handling {k} command")
                    #self.transport.write(b"0")
                    #return

        if resp is None:
            self.logger.warn(f"Unhandled command: {hex(cmd)}")
            self.transport.write(b"0")
            return

        self.transport.write(self.aimedb_postprocessing(resp))
    
    def aimedb_preprocessing(self, data: bytes) -> bytes:
        key = self.config.aimedb.key.encode("utf-8")
        self.cipher = AES.new(key, AES.MODE_ECB)

        try:
            decrypted = self.cipher.decrypt(data)
        except:
            self.logger.error(f"Failed to decrypt {data.hex()}")
            return b''

        self.logger.info(f"Request: {decrypted.hex()}")
        return decrypted
    
    def aimedb_postprocessing(self, data: bytes) -> bytes:
        self.logger.info(f"Response: {data.hex()}")

        try:
            encrypted = self.cipher.encrypt(data)
        except ValueError as e:
            print(f"Failed to encrypt {data.hex()} because {e}")
            return b"0"

        return encrypted

    def append_padding(self, data: bytes):
        """Appends 0s to the end of the data until it's at the correct size"""
        length = struct.unpack_from("<H", data, 6)
        padding_size = length[0] - len(data)
        data += bytes(padding_size)
        return data

    def handle_campaign_request(self, data: bytes) -> bytes: 
        ret = struct.pack("<5H", 0xa13e, 0x3087, self.AIMEDB_RESPONSE_CODES["campaign"], 0x0200, 0x0001)
        return self.append_padding(ret)
    
    def handle_hello_request(self, data: bytes) -> bytes:
        ret = struct.pack("<5H", 0xa13e, 0x3087, self.AIMEDB_RESPONSE_CODES["hello"], 0x0020, 0x0001)
        return self.append_padding(ret)

    def handle_lookup_request(self, data: bytes) -> bytes:
        luid = data[0x20: 0x2a].hex()
        user_id = self.data.user.get_user_id_from_card(access_code=luid)

        if user_id is None: user_id = -1

        ret = struct.pack("<5H", 0xa13e, 0x3087, self.AIMEDB_RESPONSE_CODES["lookup"], 0x0130, 0x0001)
        ret += bytes(0x20 - len(ret))

        if user_id is None: ret += struct.pack("<iH", -1, 0)
        else: ret += struct.pack("<l", user_id)
        return self.append_padding(ret)

    def handle_lookup2_request(self, data: bytes) -> bytes:
        ret = bytearray(self.handle_lookup_request(data))
        ret[4] = self.AIMEDB_RESPONSE_CODES["lookup2"]
        return bytes(ret)

    def handle_felica_lookup_request(self, data: bytes) -> bytes:
        idm = data[0x20: 0x28].hex()
        pmm = data[0x28: 0x30].hex()
        access_code = self.data.user.to_access_code(idm)

        ret = struct.pack("<5H", 0xa13e, 0x3087, self.AIMEDB_RESPONSE_CODES["felica_lookup"], 0x0030, 0x0001)
        ret += bytes(26)
        ret += bytes.fromhex(access_code)

        return self.append_padding(ret)

    def handle_felica_lookup2_request(self, data: bytes) -> bytes:
        idm = data[0x30: 0x38].hex()
        pmm = data[0x38: 0x40].hex()
        access_code = self.data.user.to_access_code(idm)
        user_id = self.data.user.get_user_id_from_card(access_code=access_code)

        if user_id is None: user_id = -1

        ret = struct.pack("<5H", 0xa13e, 0x3087, self.AIMEDB_RESPONSE_CODES["felica_lookup2"], 0x0140, 0x0001)
        ret += bytes(22)
        ret += struct.pack("<lq", user_id, -1) # first -1 is ext_id, 3rd is access code
        ret += bytes.fromhex(access_code)
        ret += struct.pack("<l", 1)
        
        return self.append_padding(ret)
    
    def handle_touch_request(self, data: bytes) -> bytes:
        ret = struct.pack("<5H", 0xa13e, 0x3087, self.AIMEDB_RESPONSE_CODES["touch"], 0x0050, 0x0001)
        ret += bytes(5)
        ret += struct.pack("<3H", 0x6f, 0, 1)

        return self.append_padding(ret)

    def handle_register_request(self, data: bytes) -> bytes:
        user_id = self.data.user.create_user()

        if user_id is None: 
            user_id = -1
            self.logger.error("Failed to register user!")

        else:
            luid = data[0x20: 0x2a].hex()
            card_id = self.data.user.create_card(user_id, luid)

            if card_id is None: 
                user_id = -1
                self.logger.error("Failed to register card!")

        ret = struct.pack("<5H", 0xa13e, 0x3087, self.AIMEDB_RESPONSE_CODES["lookup"], 0x0030, 0x0001 if user_id > -1 else 0)
        ret += bytes(0x20 - len(ret))
        ret += struct.pack("<l", user_id)

        return self.append_padding(ret)

    def handle_log_request(self, data: bytes) -> bytes:
        # TODO: Save aimedb logs
        ret = struct.pack("<5H", 0xa13e, 0x3087, self.AIMEDB_RESPONSE_CODES["log"], 0x0020, 0x0001)
        return self.append_padding(ret)

    def handle_log2_request(self, data: bytes) -> bytes:
        ret = struct.pack("<5H", 0xa13e, 0x3087, self.AIMEDB_RESPONSE_CODES["log2"], 0x0040, 0x0001)
        ret += bytes(22)
        ret += struct.pack("H", 1)

        return self.append_padding(ret)

class AimedbFactory(Factory):
    protocol = Aimedb
    def __init__(self, cfg: Config) -> None:
        self.config = cfg
        log_fmt_str = "[%(asctime)s] Aimedb | %(levelname)s | %(message)s"
        log_fmt = logging.Formatter(log_fmt_str)
        self.logger = logging.getLogger("aimedb")

        fileHandler = TimedRotatingFileHandler("{0}/{1}.log".format(self.config.server.logs, "aimedb"), when="d", backupCount=10)
        fileHandler.setFormatter(log_fmt)
        
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(log_fmt)

        self.logger.addHandler(fileHandler)
        self.logger.addHandler(consoleHandler)
        
        self.logger.setLevel(self.config.aimedb.loglevel)
        coloredlogs.install(level=cfg.aimedb.loglevel, logger=self.logger, fmt=log_fmt_str)
        if self.config.aimedb.key == "":
            self.logger.error("Please set 'key' field in your config file.")
            exit(1)
        self.logger.info("Aimedb started")
    
    def buildProtocol(self, addr):
        return Aimedb(self.config)
