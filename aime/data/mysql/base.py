import logging
from random import randrange
from typing import Any, Optional, Dict
from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.engine.base import Connection
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import MetaData, Table, Column
from sqlalchemy.types import Integer

from aime.data.config import Config

metadata = MetaData()

schema_ver = Table(
    "schema_ver",
    metadata,
    Column("version", Integer, primary_key=True, nullable=False)
)

class BaseData():
    def __init__(self, cfg: Config, conn: Connection) -> None:
        self.config = cfg
        self.conn = conn
        self.logger = logging.getLogger("database")

    def execute(self, sql: str, opts: Dict[str, Any]={}) -> Optional[CursorResult]:
        self.logger.info(f"SQL Execute: {sql} || {opts}")
        res = None

        try:
            res = self.conn.execute(text(sql), opts)

        except SQLAlchemyError as e:
            self.logger.error(f"SQLAlchemy error {e}")
            return None
        
        except UnicodeEncodeError as e:
            self.logger.error(f"UnicodeEncodeError error {e}")
            return None

        except:
            try:
                res = self.conn.execute(sql, opts)

            except SQLAlchemyError as e:
                self.logger.error(f"SQLAlchemy error {e}")
                return None

        return res
    
    def generate_id(self) -> int:
        """
        Generate a random 5-7 digit id
        """
        return randrange(10000, 9999999)
    
    def get_schema_ver(self) -> int:
        sql = schema_ver.select()
        result = self.execute(sql)
        return result.fetchone()["version"]
