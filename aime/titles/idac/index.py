from twisted.web import server
from twisted.internet import reactor, endpoints
import yaml
import logging, coloredlogs
from logging.handlers import TimedRotatingFileHandler
from threading import Thread

from aime.data import Config
from aime.titles.idac.config import IDACConfig
from aime.titles.idac.dispatch import IDACDispatch
from aime.titles.idac.const import IDACConstants
from aime.titles.idac.echo import IDACEchoUDP
from aime.titles.idac.matching import IDACMatching

class IDACServlet():
    def __init__(self, core_cfg: Config, cfg_dir: str) -> None:
        self.core_cfg = core_cfg
        self.game_cfg = IDACConfig()
        self.game_cfg.update(yaml.safe_load(open(f"{cfg_dir}/{IDACConstants.CONFIG_NAME}")))

        self.logger = logging.getLogger("idac")
        log_fmt_str = "[%(asctime)s] IDAC | %(levelname)s | %(message)s"
        log_fmt = logging.Formatter(log_fmt_str)
        fileHandler = TimedRotatingFileHandler("{0}/{1}.log".format(self.core_cfg.server.logs, "idac"), encoding='utf8',
            when="d", backupCount=10)

        fileHandler.setFormatter(log_fmt)
        
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(log_fmt)

        self.logger.addHandler(fileHandler)
        self.logger.addHandler(consoleHandler)
        
        self.logger.setLevel(self.game_cfg.server.loglevel)
        coloredlogs.install(level=self.game_cfg.server.loglevel, logger=self.logger, fmt=log_fmt_str)
        self.logger.info("IDAC title server initialized")
    
    def setup(self):
        if self.game_cfg.server.enable:
            if self.game_cfg.server.ssl:
                endpoints.serverFromString(reactor, f"ssl:{self.game_cfg.ports.main}:interface={self.core_cfg.server.hostname}") \
                    .listen(server.Site(IDACDispatch(self.core_cfg, self.game_cfg)))
            else:
                endpoints.serverFromString(reactor, f"tcp:{self.game_cfg.ports.main}:interface={self.core_cfg.server.hostname}") \
                    .listen(server.Site(IDACDispatch(self.core_cfg, self.game_cfg)))
            
            endpoints.serverFromString(reactor, f"tcp:{self.game_cfg.ports.matching}:interface={self.core_cfg.server.hostname}") \
                    .listen(server.Site(IDACMatching(self.core_cfg, self.game_cfg)))
            
            reactor.listenUDP(self.game_cfg.ports.echo1, IDACEchoUDP(self.core_cfg, self.game_cfg, self.game_cfg.ports.echo1))
            reactor.listenUDP(self.game_cfg.ports.echo2, IDACEchoUDP(self.core_cfg, self.game_cfg, self.game_cfg.ports.echo2))
            self.logger.info(f"IDAC title server ready on port {self.game_cfg.ports.main}")