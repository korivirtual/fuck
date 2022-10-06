import logging, coloredlogs
import os
from typing import Any, Dict
from twisted.web import resource
import importlib
from logging.handlers import TimedRotatingFileHandler

from aime.data import Config

class Frontend(resource.Resource):
    children: Dict[str, Any] = {}
    def getChild(self, name, request):
        if name == '':
            return self            
        return resource.Resource.getChild(self, name, request)

    def __init__(self, cfg: Config, config_dir: str) -> None:
        self.config = cfg
        log_fmt_str = "[%(asctime)s] Frontend | %(levelname)s | %(message)s"
        log_fmt = logging.Formatter(log_fmt_str)
        self.logger = logging.getLogger("frontend")

        fileHandler = TimedRotatingFileHandler("{0}/{1}.log".format(self.config.server.logs, "frontend"), when="d", backupCount=10)
        fileHandler.setFormatter(log_fmt)
        
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(log_fmt)

        self.logger.addHandler(fileHandler)
        self.logger.addHandler(consoleHandler)
        
        self.logger.setLevel(cfg.frontend.loglevel)
        coloredlogs.install(level=cfg.frontend.loglevel, logger=self.logger, fmt=log_fmt_str)
        
        self.logger.info("Frontend started")

        for root, dirs, files in os.walk("./aime/titles"):
            for dir in dirs: 
                if not dir.startswith("__"):
                    try:
                        mod = importlib.import_module(f"aime.titles.{dir}")
                        self.putChild(dir.encode(), mod.frontend(cfg))
                    except ImportError as e:
                        self.logger.warning(f"Failed to import from {dir} - {e}")
                    except AttributeError as e:
                        self.logger.warning(f"Frontend not configured for {dir} - {e}")
            break
        
        self.putChild(b"", FE_Index(cfg))

        if len(self.children) < 1:
            self.isLeaf = True

class FE_Index(resource.Resource):
    isLeaf = True    

    def render_GET(self, request):
        self.logger.info("%s %s", request.getClientIP(), request.uri.decode())
        return f"<html><head><title>{self.config.server.name}</title></head><body>こんにちは世界！ I am located at {request.postpath}</body></html>".encode("utf-16")

    def __init__(self, cfg: Config) -> None:
        self.config = cfg
        self.logger = logging.getLogger('frontend')