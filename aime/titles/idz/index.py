from turtle import back
from twisted.web import server
from twisted.internet import reactor, endpoints
import yaml
import logging, coloredlogs
from logging.handlers import RotatingFileHandler
from socketserver import TCPServer
from threading import Thread

from aime.data import Config, Data
from aime.titles.idz.config import IDZConfig
from aime.titles.idz.news import IDZNews
from aime.titles.idz.userdb import IDZUserdbTCPFactory, IDZUserdbTCP
from aime.titles.idz.ping import IDZPing
from aime.titles.idz.const import IDZConstants

class IDZServlet():
    def __init__(self, core_cfg: Config, cfg_dir: str) -> None:
        self.core_cfg = core_cfg
        self.game_cfg = IDZConfig()
        self.game_cfg.update(yaml.safe_load(open(f"{cfg_dir}/{IDZConstants.CONFIG_NAME}")))

        self.logger = logging.getLogger("idz")
        log_fmt_str = "[%(asctime)s] IDZ | %(levelname)s | %(message)s"
        log_fmt = logging.Formatter(log_fmt_str)
        fileHandler = RotatingFileHandler("{0}/{1}.log".format(self.core_cfg.server.logs, "idz"), encoding='utf8',
            maxBytes=150000000, backupCount=10)

        fileHandler.setFormatter(log_fmt)
        
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(log_fmt)

        self.logger.addHandler(fileHandler)
        self.logger.addHandler(consoleHandler)
        
        self.logger.setLevel(self.game_cfg.server.loglevel)
        coloredlogs.install(level=self.game_cfg.server.loglevel, logger=self.logger, fmt=log_fmt_str)
        self.logger.info("IDZ title server loaded")
    
    def setup(self):
        if self.game_cfg.server.enable:
            userdb = IDZUserdbTCPFactory((self.core_cfg.server.hostname, self.game_cfg.server.port), IDZUserdbTCP, self.core_cfg, self.game_cfg)
            Thread(target=userdb.serve_forever, daemon=True).start()

            endpoints.serverFromString(reactor, f"tcp:{self.game_cfg.ports.news_tcp}:interface={self.core_cfg.server.hostname}") \
                .listen(server.Site(IDZNews(self.core_cfg, self.game_cfg)))
            
            reactor.listenUDP(self.game_cfg.server.port + 1, IDZPing(self.core_cfg, self.game_cfg, self.game_cfg.server.port + 1))
            reactor.listenUDP(self.game_cfg.ports.match_udp_snd, IDZPing(self.core_cfg, self.game_cfg, self.game_cfg.ports.match_udp_snd))
            reactor.listenUDP(self.game_cfg.ports.echo1_udp, IDZPing(self.core_cfg, self.game_cfg, self.game_cfg.ports.echo1_udp))
            reactor.listenUDP(self.game_cfg.ports.echo2_udp, IDZPing(self.core_cfg, self.game_cfg, self.game_cfg.ports.echo2_udp))

            self.logger.info(f"IDZ Userdb ready on port {self.game_cfg.server.port} and {self.game_cfg.server.port + 1}")