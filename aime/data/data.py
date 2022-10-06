import logging, coloredlogs
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine, text
from logging.handlers import TimedRotatingFileHandler
from hashlib import sha256

from aime.data.config import Config
from aime.data.mysql import BaseData, UserData, ArcadeData, GameData, StaticData, metadata

class Data():
    def __init__(self, cfg: Config) -> None:
        self.__config = cfg

        if self.__config.database.sha2_password:
            passwd = sha256(self.__config.database.password.encode()).digest()
            self.__url = f"{self.__config.database.type}://{self.__config.database.username}:{passwd.hex()}@{self.__config.database.host}/{self.__config.database.name}?charset=utf8mb4"
        else:
            self.__url = f"{self.__config.database.type}://{self.__config.database.username}:{self.__config.database.password}@{self.__config.database.host}/{self.__config.database.name}?charset=utf8mb4"
        
        self.__engine = create_engine(self.__url, pool_recycle=3600)
        session = sessionmaker(bind=self.__engine, autoflush=True, autocommit=True)
        self.__session = scoped_session(session)

        self.static = StaticData(self.__config, self.__session)
        self.user = UserData(self.__config, self.__session)
        self.arcade = ArcadeData(self.__config, self.__session)
        self.game = GameData(self.__config, self.__session)
        self.base = BaseData(self.__config, self.__session)
        self.schema_ver_latest = 3

        log_fmt_str = "[%(asctime)s] %(levelname)s | Database | %(message)s"
        log_fmt = logging.Formatter(log_fmt_str)
        self.logger = logging.getLogger("database")
        # Prevent the logger from adding handlers multiple times
        if not getattr(self.logger, 'handler_set', None):
            fileHandler = TimedRotatingFileHandler("{0}/{1}.log".format(self.__config.server.logs, "db"), encoding="utf-8",
                when="d", backupCount=10)
            fileHandler.setFormatter(log_fmt)
            
            consoleHandler = logging.StreamHandler()
            consoleHandler.setFormatter(log_fmt)

            self.logger.addHandler(fileHandler)
            self.logger.addHandler(consoleHandler)
            
            self.logger.setLevel(self.__config.database.loglevel)
            coloredlogs.install(cfg.database.loglevel, logger=self.logger, fmt=log_fmt_str)
            self.logger.handler_set = True
    
    def create_database(self):
        self.logger.info("Creating databases...")
        try:
            metadata.create_all(self.__engine.connect())
        except SQLAlchemyError as e:
            self.logger.error(f"Failed to create databases! {e}")
            return

        self.logger.info("Resetting user auto_incrememnt to 100000...")
        self.base.execute("ALTER TABLE user AUTO_INCREMENT = 100000")
        
        self.logger.info(f"Setting schema_ver to {self.schema_ver_latest}")
        self.base.execute("DELETE FROM schema_ver")
        self.base.execute(f"INSERT INTO schema_ver VALUES ({self.schema_ver_latest})")
    
    def recreate_database(self):
        self.logger.info("Dropping all databases...")
        try:
            metadata.drop_all(self.__engine.connect())
        except SQLAlchemyError as e:
            self.logger.error(f"Failed to drop databases! {e}")
            return
        self.create_database()
    
    def migrate_database(self, version: int):
        current = self.base.get_schema_ver()
        action = ""

        if not current:
            self.logger.error(f"Could not get database version, did you create it?")

        if current == version:
            self.logger.info(f"Database is already version {version}, no change.")
            return
        
        elif current > version:
            action = "down"
        
        elif current < version:
            action = "up"
        
        else:
            self.logger.error(f"Something went wrong. ({current} -> {version}) {action}")
            return

        self.logger.info(f"Migrating database ({current} -> {version}) {action}")

        for x in range(current, version, -1 if action == "down" else 1):
            file = f"./aime/data/mysql/versions/{x}-{action}.sql"
            try:
                escaped_sql = text(open(file).read())
                self.base.execute(escaped_sql)

            except:
                self.logger.error(f"Failed to read file {file}")
                return

        self.logger.info(f"Successfully migrated to version {version}")

