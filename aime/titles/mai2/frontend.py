import logging
from twisted.web import resource

from aime.data import Data, Config

class Mai2Frontend(resource.Resource):
    isLeaf = True
    def getChild(self, name, request):
        if name == '':
            return self
        return resource.Resource.getChild(self, name, request)
    # TODO: yes
    def __init__(self, cfg: Config) -> None:
        self.config = cfg
        self.logger = logging.getLogger('frontend')
    
    def render_GET(self, request):
        self.logger.info("%s %s", request.getClientIP(), request.uri.decode())
        return b"<html><head><title>maimai DX</title></head><body>Hello, world! I am located at %r and I am maimai DX</body></html>" % (request.postpath)