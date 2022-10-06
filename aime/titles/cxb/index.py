from twisted.web import server
from twisted.internet import reactor, endpoints
import yaml
import logging, coloredlogs
from logging.handlers import TimedRotatingFileHandler

from aime.data import Config
from aime.titles.cxb.config import CxbConfig
from aime.titles.cxb.dispatch import CxbDispatch

class CxbServlet():
    def __init__(self, core_cfg: Config, cfg_dir: str) -> None:
        self.core_cfg = core_cfg
        self.game_cfg = CxbConfig()
        self.game_cfg.update(yaml.safe_load(open(f"{cfg_dir}/cxb.yaml")))

        self.logger = logging.getLogger("cxb")
        log_fmt_str = "[%(asctime)s] Crossbeats | %(levelname)s | %(message)s"
        log_fmt = logging.Formatter(log_fmt_str)
        fileHandler = TimedRotatingFileHandler("{0}/{1}.log".format(self.core_cfg.server.logs, "cxb"), encoding='utf8',
            when="d", backupCount=10)

        fileHandler.setFormatter(log_fmt)
        
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(log_fmt)

        self.logger.addHandler(fileHandler)
        self.logger.addHandler(consoleHandler)
        
        self.logger.setLevel(self.game_cfg.server.loglevel)
        coloredlogs.install(level=self.game_cfg.server.loglevel, logger=self.logger, fmt=log_fmt_str)
        self.logger.info("Crossbeats title server initialized")

    def setup(self):
        if self.game_cfg.server.enable:
            endpoints.serverFromString(reactor, f"ssl:{self.game_cfg.server.port}:interface={self.game_cfg.server.hostname}:privateKey={self.game_cfg.server.ssl_key}:certKey={self.game_cfg.server.ssl_cert}").listen(server.Site(CxbDispatch(self.core_cfg, self.game_cfg)))
            self.logger.info(f"Crossbeats title server ready on port {self.game_cfg.server.port}")
