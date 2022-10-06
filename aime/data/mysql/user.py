from typing import Dict, Optional, Tuple
import json
from sqlalchemy import Table, Column
from sqlalchemy.types import Integer, String, JSON, TIMESTAMP, Boolean
from sqlalchemy.sql.schema import ForeignKey

from aime.data.mysql.base import BaseData, metadata

user = Table(
    "user",
    metadata,
    Column("id", Integer, nullable=False, primary_key=True, autoincrement=True),
    Column("username", String(25), unique=True),
    Column("email", String(255), unique=True),
    Column("password", String(255)),
    Column("permissions", Integer),    
    Column("created_date", TIMESTAMP),
    Column("accessed_date", TIMESTAMP),
    Column("data", JSON),
    mysql_charset='utf8mb4'
)

card = Table(
    "card",
    metadata,
    Column("id", Integer, nullable=False, primary_key=True, autoincrement=True),
    Column("user", Integer, ForeignKey("user.id", ondelete="cascade"), nullable=False),
    Column("access_code", String(20), unique=True),
    Column("created_date", TIMESTAMP),
    Column("accessed_date", TIMESTAMP),
    Column("is_locked", Boolean),
    Column("is_banned", Boolean),
    Column("data", JSON),
    mysql_charset='utf8mb4'
)

session = Table(
    "session",
    metadata,
    Column("id", Integer, primary_key=True, unique=True),
    Column("user", ForeignKey("user.id", ondelete="cascade"), nullable=False),    
    Column('type', String(32), nullable=False),
    Column('session', String(32), nullable=False, unique=True),
    Column("expires", TIMESTAMP, nullable=False),
    mysql_charset='utf8mb4'
)

class UserData(BaseData):
    def create_user(self, username: str = None, email: str = None, password: str = None, data: Dict = {}) -> Optional[int]:
        if not username and not email and not password:
            sql = 'INSERT INTO user VALUES (DEFAULT, NULL, NULL, NULL, 0, NOW(), NOW(), :data)'
        else: 
            sql = 'INSERT INTO user VALUES (DEFAULT, :username, :email, :password, 0, NOW(), NOW(), :data)'
        
        result = self.execute(sql, {"username": username, "email": email, "password": password, "data": json.dumps(data)})
        if result is None: return None
        return result.lastrowid

    def create_card(self, user_id: int, access_code: int) -> Optional[int]:
        sql = 'INSERT INTO card VALUES (DEFAULT, :user_id, :access_code, NOW(), NOW(), FALSE, FALSE, "{}")'
        result = self.execute(sql, {"user_id": user_id, "access_code": access_code})
        if result is None: return None
        return result.lastrowid
    
    def reset_user_password(self, user_id: int, newpass: str) -> bool:
        pass

    def update_user_info(self, new_username: str = None, new_email: str = None, new_perms: int = None,
        new_access_date: int = None, new_data: Dict = None) -> bool:
        pass

    def remove_hanging_users(self) -> Tuple[int, int]:
        """
        Removes any empty user accounts that are left behind when somebody registeres a card but attaches
        it to a different account.
        """
        sql = "SELECT u.id FROM user u LEFT JOIN card c on u.id = c.user WHERE c.user = NULL and u.username = NULL"
        result = self.execute(sql)
        hanging_users = result.fetchall()
        failed = []
        success = []

        for id in hanging_users:
            sql = "DELETE FROM user WHERE id = :id"
            result = self.execute(sql, {"id": id})

            if result.rowcount < 1:
                failed.append(id)
            else:
                success.append(id)
        return failed, success

    def get_user_id_from_card(self, card_id: int = None, access_code: str = None) -> Optional[int]:
        if card_id is not None:
            stmt = card.select(card.c.id == card_id)
        elif access_code is not None:
            stmt = card.select(card.c.access_code == access_code)
        else:
            return None
        
        result = self.execute(stmt).fetchone()
        if result is None:
            return None
        return result.user

    def to_access_code(self, luid: str) -> str:
        return f"{int(luid, base=16):0{20}}"

    def to_idm(self, access_code: str) -> str:
        return f'{int(access_code):0{16}x}'
