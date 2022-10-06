import logging, coloredlogs
import struct
from typing import Dict
from twisted.web import resource
import zlib
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto.Signature import PKCS1_v1_5
from logging.handlers import TimedRotatingFileHandler

from aime.data import Config, Data

class Billing(resource.Resource):
    isLeaf = True
    def __init__(self, cfg: Config) -> None:
        self.config = cfg
        self.data = Data(cfg)
        log_fmt_str = "[%(asctime)s] Billing | %(levelname)s | %(message)s"
        log_fmt = logging.Formatter(log_fmt_str)
        self.logger = logging.getLogger("billing")

        fileHandler = TimedRotatingFileHandler("{0}/{1}.log".format(self.config.server.logs, "billing"), when="d", backupCount=10)
        fileHandler.setFormatter(log_fmt)
        
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(log_fmt)

        self.logger.addHandler(fileHandler)
        self.logger.addHandler(consoleHandler)
        
        self.logger.setLevel(cfg.billing.loglevel)
        coloredlogs.install(level=cfg.billing.loglevel, logger=self.logger, fmt=log_fmt_str)
        self.logger.info("Billing started")
    
    def render_POST(self, request):
        request.responseHeaders.addRawHeader(b"content-type", b"text/plain")
        url = request.uri.decode()
        urlSplit = url.split("/")
        req_raw = request.content.getvalue()

        try:
            req_data = self.billing_req_preprocessing(req_raw)
            if req_data:
                self.logger.info(f"Billing request from {request.getClientIP()}: {req_data}")
                handler = getattr(self, f"handle_{urlSplit[1]}_request")
                return self.billing_req_postprocessing(handler(req_data)).encode("utf-8")
            else:
                return b""

        except Exception as e:
            self.logger.error(f"Error processing billing request from {request.getClientIP()}: {request.uri.decode()} || {req_raw} || {e}")
            return b""
    
    def render_GET(self, request):
        self.logger.debug(f"Billing GET request, ip: {request.getClientIP()} url: {request.uri.decode()} body: {request.content.getvalue()}")
        return b""

    def billing_req_preprocessing(self, data: bytes) -> Dict:
        decomp = zlib.decompressobj(-zlib.MAX_WBITS)
        try:
            req_bytes = decomp.decompress(data)
            req_str = req_bytes.decode('ascii')
        except:
            self.logger.error(f"Error decompressing {data}")
            return []

        req_kvp_full = []
        for i in req_str.split("\r\n"):
            tmp = {}
            for j in i.split("&"):
                k = j.split("=")
                if not k[0] == '':
                    tmp[k[0]] = k[1]
            req_kvp_full.append(tmp)
        return req_kvp_full

    def billing_req_postprocessing(self, data: Dict) -> str:
        res_str = ""
        for key, val in data.items():
            res_str += f"{key}={val}&"
        res_str = res_str[:-1] + '\r\n'
        return res_str
    
    def handle_request_request(self, data: Dict) -> Dict:
        rsa = RSA.import_key(open(self.config.billing.sign_key, 'rb').read())
        signer = PKCS1_v1_5.new(rsa)
        digest = SHA.new()
        playlimit = int(data[0]["playlimit"])
        nearfull = int(data[0]["nearfull"]) + (int(data[0]["billingtype"]) * 0x00010000)
        keychip_bytes = data[0]["keychipid"].encode()
        playlimit_bytes = playlimit.to_bytes(4, 'little')
        nearfull_bytes = nearfull.to_bytes(4, 'little')

        digest.update(playlimit_bytes + keychip_bytes)
        playlimit_sig = signer.sign(digest).hex()

        digest = SHA.new()
        digest.update(nearfull_bytes + keychip_bytes)
        nearfull_sig = signer.sign(digest).hex()

        playhistory_dict = {}
        playhistory = ""

        if playhistory_dict: #TODO: Real playhistory
            for k,v in playhistory_dict.items():
                playhistory += f"{k}/{v}:"                

            if playhistory.endswith(":"):
                playhistory = playhistory[:-1]
                
        else:
            playhistory = "000000/0:000000/0:000000/0"

        resp =  {
            "result": "0",
            "waitime": "100",
            "linelimit": "1",
            "message": "",
            "playlimit": str(playlimit),
            "playlimitsig": playlimit_sig,
            "protocolver": "1.000",
            "nearfull": str(nearfull),
            "nearfullsig": nearfull_sig,
            "fixlogincnt": "0",
            "fixinterval": "5",
            "playhistory": playhistory 
        }

        self.logger.info(f"Billing response: {resp}")
        return resp