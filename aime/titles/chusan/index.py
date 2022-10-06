from twisted.web import server
from twisted.internet import reactor, endpoints
import yaml
import logging, coloredlogs

from aime.data import Config, Data
from aime.titles.chusan.config import ChusanConfig
from aime.titles.chusan.dispatch import ChusanDispatch

class ChusanServlet():
    def __init__(self, core_cfg: Config, cfg_dir: str) -> None:
        self.core_cfg = core_cfg
        self.game_cfg = ChusanConfig()
        self.game_cfg.update(yaml.safe_load(open(f"{cfg_dir}/chusan.yaml")))

        self.logger = logging.getLogger("chusan")
        log_fmt_str = "[%(asctime)s] Chunithm New | %(levelname)s | %(message)s"
        log_fmt = logging.Formatter(log_fmt_str)
        fileHandler = logging.FileHandler("{0}/{1}.log".format(self.core_cfg.server.logs, "chusan"), encoding='utf8')

        fileHandler.setFormatter(log_fmt)
        
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(log_fmt)

        self.logger.addHandler(fileHandler)
        self.logger.addHandler(consoleHandler)
        
        self.logger.setLevel(self.game_cfg.server.loglevel)
        coloredlogs.install(level=self.game_cfg.server.loglevel, logger=self.logger, fmt=log_fmt_str)
        self.logger.info("Chunithm New title server loaded")
    
    def setup(self):
        endpoints.serverFromString(reactor, f"tcp:{self.game_cfg.server.port}:interface={self.core_cfg.server.hostname}") \
            .listen(server.Site(ChusanDispatch(self.core_cfg, self.game_cfg)))
        self.logger.info(f"Chunithm New title server ready on port {self.game_cfg.server.port}")

        