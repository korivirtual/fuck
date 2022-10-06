import zlib
import json
import logging
import inflection
import urllib.parse
import base64

from twisted.web import resource

from aime.titles.diva.base import DivaBase
from aime.data import Config, Data

class DivaDispatch(resource.Resource):
    isLeaf = True

    def __init__(self, core_cfg: Config, game_cfg: Config):
        self.core_cfg = core_cfg
        self.game_cfg = game_cfg
        self.data = Data(core_cfg)
        self.logger = logging.getLogger("diva")

        self.base = DivaBase(core_cfg, game_cfg)
    
    def render_POST(self, req) -> bytes:
        url = req.uri.decode()
        req_raw = req.content.getvalue()
        url_header = req.getAllHeaders()

        #Ping Dispatch
        if "THIS_STRING_SEPARATES"in str(url_header):
            binary_request = req_raw.splitlines()
            binary_cmd_decoded = binary_request[3].decode("utf-8")
            binary_array = binary_cmd_decoded.split('&')

            bin_req_data = {}

            for kvp in binary_array:
                split_bin = kvp.split("=")
                bin_req_data[split_bin[0]] = split_bin[1]

            handler = getattr(self.base, "handle_ping_request")
            resp = handler(bin_req_data)

            self.logger.info(f"Binary Request {binary_cmd_decoded}")
            self.logger.info(f"Response cmd={bin_req_data['cmd']}&req_id={bin_req_data['req_id']}&stat=ok{resp}")
            return f"cmd={bin_req_data['cmd']}&req_id={bin_req_data['req_id']}&stat=ok{resp}".encode('utf-8')

        #Main Dispatch
        json_string = json.dumps(req_raw.decode("utf-8")) #Take the response and decode as UTF-8 and dump
        b64string = json_string.replace(r'\n', '\n') # Remove all \n and separate them as new lines
        gz_string = base64.b64decode(b64string) # Decompressing the base64 string
        try:
            url_data = zlib.decompress( gz_string ).decode("utf-8") # Decompressing the gzip
        except zlib.error as e:
            if b'\xa6z' in gz_string:
                return b''
            print(f"Diva: could not deflate: {gz_string}")
            return "stat=0"

        req_kvp = urllib.parse.unquote(url_data)
        req_data = {}
        
        # We then need to split each parts with & so we can reuse them to fill out the requests
        splitted_request = str.split(req_kvp, "&")
        for kvp in splitted_request:
            split = kvp.split("=")
            req_data[split[0]] = split[1]

        self.logger.info(f"Request {req_data}", extra={"game": "Diva"})

        func_to_find = "handle_"
        for s in req_data["cmd"]:
            func_to_find += f"{s}"
        func_to_find += "_request"

        # Load the requests
        try:
            handler = getattr(self.base, func_to_find)
            resp = handler(req_data)

        except AttributeError as e: 
            self.logger.warning(f"Unhandled request {url} {e}", extra={"game": "Diva"})
            return f"cmd={req_data['cmd']}&req_id={req_data['req_id']}&stat=ok".encode('utf-8')

        except Exception as e:
            self.logger.error(f"Error handling method {url} {e}", extra={"game": "Diva"})
            return f"cmd={req_data['cmd']}&req_id={req_data['req_id']}&stat=ok".encode('utf-8')

        req.responseHeaders.addRawHeader(b"content-type", b"text/plain")
        self.logger.info(f"Response cmd={req_data['cmd']}&req_id={req_data['req_id']}&stat=ok{resp}", extra={"game": "Diva"})

        return f"cmd={req_data['cmd']}&req_id={req_data['req_id']}&stat=ok{resp}".encode('utf-8')

    def render_GET(self, request):
        return b""