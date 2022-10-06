import importlib
import os
import logging, coloredlogs
from logging.handlers import TimedRotatingFileHandler

from aime.data import Config

class Title():
    def __init__(self, cfg: Config, cfg_folder: str) -> None:
        self.core_config = cfg
        self.config_folder = cfg_folder

        log_fmt_str = "[%(asctime)s] Title | %(levelname)s | %(message)s"
        log_fmt = logging.Formatter(log_fmt_str)
        self.logger = logging.getLogger("title")

        fileHandler = TimedRotatingFileHandler("{0}/{1}.log".format(self.core_config.server.logs, "title"), when="d", backupCount=10)
        fileHandler.setFormatter(log_fmt)
        
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(log_fmt)

        self.logger.addHandler(fileHandler)
        self.logger.addHandler(consoleHandler)
        
        self.logger.setLevel(cfg.billing.loglevel)
        coloredlogs.install(level=cfg.billing.loglevel, logger=self.logger, fmt=log_fmt_str)

    def loadAndRun(self):
        classes = []
        
        for root, dirs, files in os.walk("./aime/titles"):
            for dir in dirs: 
                if not dir.startswith("__"):
                    try:
                        mod = importlib.import_module(f"aime.titles.{dir}")
                        classes.append(mod.main(self.core_config, self.config_folder))
                    except Exception as e:
                        self.logger.warning(f"Could not load title server from dir {dir} - {e}")
            break
        
        self.logger.info(f"Loaded {len(classes)} title servers")
        for game in classes:
            game.setup()