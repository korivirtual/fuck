from twisted.web import server
from twisted.internet import reactor, endpoints
import yaml
import logging, coloredlogs
from logging.handlers import TimedRotatingFileHandler

from aime.data import Config
from aime.titles.chuni.config import ChuniConfig
from aime.titles.chuni.dispatch import ChuniDispatch

class ChuniServlet():
    def __init__(self, core_cfg: Config, cfg_dir: str) -> None:
        self.core_cfg = core_cfg
        self.game_cfg = ChuniConfig()
        self.game_cfg.update(yaml.safe_load(open(f"{cfg_dir}/chuni.yaml")))

        self.logger = logging.getLogger("chuni")
        log_fmt_str = "[%(asctime)s] Chunithm | %(levelname)s | %(message)s"
        log_fmt = logging.Formatter(log_fmt_str)
        fileHandler = TimedRotatingFileHandler("{0}/{1}.log".format(self.core_cfg.server.logs, "chuni"), encoding='utf8', 
            when="d", backupCount=10)

        fileHandler.setFormatter(log_fmt)
        
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(log_fmt)

        self.logger.addHandler(fileHandler)
        self.logger.addHandler(consoleHandler)
        
        self.logger.setLevel(self.game_cfg.server.loglevel)
        coloredlogs.install(level=self.game_cfg.server.loglevel, logger=self.logger, fmt=log_fmt_str)
        self.logger.info("Chunithm title server initialized")
    
    def setup(self):
        if self.game_cfg.server.enable:
            endpoints.serverFromString(reactor, f"tcp:{self.game_cfg.server.port}:interface={self.core_cfg.server.hostname}") \
                .listen(server.Site(ChuniDispatch(self.core_cfg, self.game_cfg)))
            self.logger.info(f"Chunithm title server ready on port {self.game_cfg.server.port}")

        