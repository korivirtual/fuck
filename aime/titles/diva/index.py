from twisted.web import server
from twisted.internet import reactor, endpoints
import yaml
import logging, coloredlogs
from logging.handlers import TimedRotatingFileHandler

from aime.data import Config, Data
from aime.titles.diva.config import DivaConfig
from aime.titles.diva.dispatch import DivaDispatch

class DivaServlet():
    def __init__(self, core_cfg: Config, cfg_dir: str) -> None:
        self.core_cfg = core_cfg
        self.game_cfg = DivaConfig()
        self.game_cfg.update(yaml.safe_load(open(f"{cfg_dir}/diva.yaml")))

        self.logger = logging.getLogger("diva")
        log_fmt_str = "[%(asctime)s] Diva | %(levelname)s | %(message)s"
        log_fmt = logging.Formatter(log_fmt_str)
        fileHandler = TimedRotatingFileHandler("{0}/{1}.log".format(self.core_cfg.server.logs, "diva"), encoding='utf8',
            when="d", backupCount=10)

        fileHandler.setFormatter(log_fmt)
        
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(log_fmt)

        self.logger.addHandler(fileHandler)
        self.logger.addHandler(consoleHandler)
        
        self.logger.setLevel(self.game_cfg.server.loglevel)
        coloredlogs.install(level=self.game_cfg.server.loglevel, logger=self.logger, fmt=log_fmt_str)
        self.logger.info("Diva title server initialized")
    
    def setup(self):
        if self.game_cfg.server.enable:
            endpoints.serverFromString(reactor, f"tcp:{self.game_cfg.server.port}:interface={self.core_cfg.server.hostname}") \
                .listen(server.Site(DivaDispatch(self.core_cfg, self.game_cfg)))
            self.logger.info(f"Diva title server ready on port {self.game_cfg.server.port}")

        
