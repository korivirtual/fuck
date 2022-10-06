from random import choice, randint
from typing import Any, Dict, List, Optional
import json
from sqlalchemy import Table, Column
from sqlalchemy.types import Integer, String, JSON, Text, TIMESTAMP
from sqlalchemy.sql.schema import ForeignKey, PrimaryKeyConstraint

from aime.data.mysql.base import BaseData, metadata

arcade = Table(
    "arcade",
    metadata,
    Column("id", Integer, nullable=False, primary_key=True, autoincrement=True),
    Column("name", String(255), nullable=False),
    Column("description", Text),
    Column("type", Integer, nullable=False, default=0), # private owner, public arcade, data
    Column("data", JSON),
    mysql_charset='utf8mb4'
)

machine = Table(
    "machine",
    metadata,
    Column("id", Integer, nullable=False, primary_key=True, autoincrement=True),
    Column("arcade", ForeignKey("arcade.id", ondelete="cascade"), nullable=False),
    Column("keychip", String(16), unique=True, nullable=False),
    Column("game", String(4)),    
    Column("data", JSON),
    mysql_charset='utf8mb4'
)

arcade_owner = Table(
    'arcade_owner',
    metadata,
    Column('user', Integer, ForeignKey("user.id", ondelete="cascade"), nullable=False),
    Column('arcade', Integer, ForeignKey("arcade.id", ondelete="cascade"), nullable=False),
    Column('permissions', Integer, nullable=False),
    PrimaryKeyConstraint('user', 'arcade', name='arcade_owner_pk'),
    mysql_charset='utf8mb4'
)

log = Table(
    'log',
    metadata,
    Column('id', Integer, nullable=False),
    Column('machine', Integer, ForeignKey("machine.id", ondelete="cascade"), nullable=False),
    Column('time', TIMESTAMP, nullable=False),
    Column('type', Integer, nullable=False),
    Column('data', JSON),
    mysql_charset='utf8mb4'
)

class ArcadeData(BaseData):
    def get_machine(self, keychip: str) -> Optional[Dict[str, Any]]:
        sql = "SELECT * FROM machine WHERE keychip LIKE :keychip"

        result = self.execute(sql, {"keychip": f"{keychip}%"})

        if result is None: return None
        return result.fetchone()
    
    def get_arcade(self, arcade_id: int) -> Optional[Dict[str, Any]]:
        sql = "SELECT * FROM arcade WHERE id = :id"

        result = self.execute(sql, {"id": arcade_id})

        if result is None: return None
        return result.fetchone()

    def get_arcade_owners(self, arcade_id: int) -> Optional[List[int]]:
        pass

    def create_arcade(self, name: str, ac_type: int, owner: int, description: str = "", data: Dict = {}) -> Optional[int]:
        sql = "INSERT INTO arcade VALUES (DEFAULT, :name, :description, :type, :data)"
        result = self.execute(sql, {"name": name, "description": description, "type": ac_type, "data": json.dumps(data)})

        if result is not None:
            arcade = result.lastrowid
            result = self.add_owner_to_arcade(arcade, owner, 1)

            if not result:
                result = self.execute("DELETE FROM arcade WHERE id = :arcade", {"arcade": arcade})
                self.logger.error(f"Failed to create arcade {name} with owner {owner}")
                return None

            return arcade

        else:
            self.logger.error(f"Failed to create arcade {name} with owner {owner}")
            return None
     
    def create_machine(self, arcade: int, keychip: str, game: str = "", data: Dict = {}) -> Optional[int]:
        sql = "INSERT INTO machine VALUES (DEFAULT, :arcade, :keychip, :game, :data)"
        result = self.execute(sql, {"arcade": arcade, "keychip": keychip, "game": game, "data": json.dumps(data)})
        if result is None: return None
        return result.lastrowid

    def update_arcade(self, arcade_id: int, name: str = None, arcade_type: int = None, description: str = None, data: Dict = {}) -> Optional[int]:
        sql = "UPDATE arcade SET "
        if not name or arcade_type or description or data:
            self.logger.warn("No data provided to update!")
            return None

        if name:
            sql += "name = :name, "

        if description:
            sql += "description = :description, "

        if arcade_type:
            sql += "type = :type, "

        if not data == {}:
            sql += "data = :data"
        else:
            sql = sql[:-2] # chop off the trailing comma and space
        
        sql += " WHERE id = :id"
        result = self.execute(sql, {"id": arcade_id, "name": name, "description": description, "type": arcade_type, "data": json.dumps(data)})
        if result is None: return None
        return result.lastrowid        
    
    def update_machine(self, machine_id: int, keychip: str = None, game: str = None, data: Dict = {}) -> Optional[int]:
        sql = "UPDATE machine SET "

        if keychip:
            sql += "keychip = :keychip, "

        if game:
            sql += "game = :game, "

        if not data == {}:
            sql += "data = :data"
        else:
            sql = sql[:-2] # chop off the trailing comma and space

        sql += " WHERE id = :id"
        result = self.execute(sql, {"id": machine_id, "keychip": keychip, "game": game, "data": json.dumps(data)})
        if result is None: return None
        return result.lastrowid

    def add_owner_to_arcade(self, arcade: int, owner: int, permissions: int) -> bool:
        sql = "INSERT INTO arcade_owner VALUES (:user, :arcade, :perms)"
        result = self.execute(sql, {"user": owner, "arcade": arcade, "perms": permissions})
        if result is None: return False
        return True
    
    def generate_keychip_serial(self, platform: str):
        """
        Generates a unique keychip ID
        """
        match = True
        keychip = ""

        while match:
            id = f"{randint(1, 9999):0{4}}"
            id2 = f"{randint(1, 9999):0{4}}"
            center = "20A" if platform[3] == "X" else f'01{choice(["A","B","C","D","U"])}'

            keychip = platform + center + id

            old = self.get_machine(keychip)

            if not old or old is None:
                keychip += id2
                match = False
        
        return keychip

        