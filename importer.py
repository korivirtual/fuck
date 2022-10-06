import argparse
from typing import Dict
import yaml
import os
import importlib
import logging
import coloredlogs
from logging.handlers import TimedRotatingFileHandler

from aime.data import Config

parser = argparse.ArgumentParser(description="Aime service provider")
parser.add_argument("--config", "-c", type=str, help="Config folder to use", default="config")
parser.add_argument("--game", "-g", type=str, help="4 letter game code", default=None)
parser.add_argument("--version", "-v", type=str, help="game version to import, as defined in game constants", default=None)
parser.add_argument("--bin", "-b", type=str, help="Directory containing A000", default=None)
parser.add_argument("--opt", "-o", type=str, help="Directory containing AXXX option files", default=None)
args = parser.parse_args()

cfg = Config()
cfg.update(yaml.safe_load(open(f"{args.config}/core.yaml")))

importer = None

logger = logging.getLogger("importer")
log_fmt_str = "[%(asctime)s] ImportData | %(levelname)s | %(message)s"
log_fmt = logging.Formatter(log_fmt_str)

fileHandler = TimedRotatingFileHandler("{0}/{1}.log".format("log", "import"), encoding='utf8', when="d", backupCount=10)
fileHandler.setFormatter(log_fmt)
        
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(log_fmt)

logger.addHandler(fileHandler)
logger.addHandler(consoleHandler)

logger.setLevel(cfg.title.loglevel)
coloredlogs.install(level=cfg.title.loglevel, logger=logger, fmt=log_fmt_str)

for root, dirs, files in os.walk("./aime/titles"):
    for dir in dirs: 
        if not dir.startswith("__") and root == "./aime/titles":
            try:
                mod = importlib.import_module(f"aime.titles.{dir}")
                if mod.game_code == args.game:
                    importer = mod.importer(cfg, args.config)
                    break
            except ImportError as e:
                logger.warning(f"Failed to import from dir {dir} - {e}")

if importer is None:
    logger.error(f"No importer for {args.game} found!")

importer.importer(args.version, args.bin, args.opt)
