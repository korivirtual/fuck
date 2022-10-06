from typing import Any, Dict, List, Optional, Tuple
import json
from sqlalchemy import Table, Column, text
from sqlalchemy.types import Integer, String, JSON
from sqlalchemy.sql.schema import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.mysql import insert

from aime.data.cache import cached
from aime.data.mysql.base import BaseData, metadata

profile = Table(
    'profile',
    metadata,
    Column('id', Integer, nullable=False, primary_key=True, autoincrement=True ),
    Column('user', Integer, ForeignKey("user.id", ondelete="cascade"), nullable=False),    
    Column('game', String(4), nullable=False),
    Column('version', Integer, nullable=False),
    Column('name', String(20)),
    Column('use_count', Integer, nullable=False),
    Column('game_id', Integer),
    Column('mods', JSON),
    Column('data', JSON),
    UniqueConstraint('user', 'game', 'version', name="profile_user_uk"),
    UniqueConstraint('game_id', 'game', 'version', name="profile_game_id_uk"),
    mysql_charset='utf8mb4'
)

score = Table(
    "score",
    metadata,
    Column('id', Integer, nullable=False, primary_key=True, autoincrement=True),
    Column('user', Integer, ForeignKey("user.id", ondelete="cascade"), nullable=False),
    Column('game', String(4), nullable=False),
    Column('version', Integer, nullable=False),
    Column('song_id', String(255), nullable=False), # Some games store song ids as strings for some reason
    Column('chart_id', Integer, nullable=False),
    Column('score1', Integer, nullable=False),
    Column('score2', Integer, nullable=False),
    Column('fc1', Integer, nullable=False),
    Column('fc2', Integer, nullable=False),
    Column('cleared', Integer, nullable=False),
    Column('grade', Integer, nullable=False),
    Column('data', JSON),
    UniqueConstraint('user', 'game', 'song_id', 'chart_id', name="score_uk"),
    mysql_charset='utf8mb4'
)

score_history = Table(
    "score_history",
    metadata,
    Column('id', Integer, nullable=False, primary_key=True, autoincrement=True),
    Column('user', Integer, ForeignKey("user.id", ondelete="cascade"), nullable=False),
    Column('game', String(4), nullable=False),
    Column('version', Integer, nullable=False),    
    Column('song_id', String(255), nullable=False), # Some games store song ids as strings for some reason
    Column('chart_id', Integer, nullable=False),
    Column('score1', Integer, nullable=False),
    Column('score2', Integer, nullable=False),
    Column('fc1', Integer, nullable=False),
    Column('fc2', Integer, nullable=False),
    Column('cleared', Integer, nullable=False),
    Column('grade', Integer, nullable=False),
    Column('data', JSON),
    mysql_charset='utf8mb4'
)

achievement = Table(
    "achievement",
    metadata,
    Column('id', Integer, nullable=False, primary_key=True, autoincrement=True ),
    Column('user', Integer, ForeignKey("user.id", ondelete="cascade"), nullable=False),
    Column('game', String(4), nullable=False),
    Column('version', Integer, nullable=False),
    Column('type', Integer, nullable=False),
    Column('achievement_id', Integer, nullable=False),
    Column('data', JSON),
    UniqueConstraint('user', 'game', 'version', 'type', 'achievement_id', name="achievement_uk"),
    mysql_charset='utf8mb4'
)

item = Table(
    "item",
    metadata,
    Column('id', Integer, nullable=False, primary_key=True, autoincrement=True ),
    Column('user', Integer, ForeignKey("user.id", ondelete="cascade"), nullable=False),
    Column('game', String(4), nullable=False),
    Column('version', Integer, nullable=False),
    Column('type', Integer, nullable=False),
    Column('item_id', Integer, nullable=False),
    Column('data', JSON),
    UniqueConstraint('user', 'game', 'version', 'type', 'item_id', name="item_uk"),
    mysql_charset='utf8mb4'
)

class GameData(BaseData):
    def put_profile(self, user_id: int, game: str, version: int, game_id: int = None, name: str = None,
        mods: Dict = {}, data: Dict = {}, should_inc_use: bool = False) -> Optional[int]:
        """
        Given a user, game, version, and dicts containing mods and data, create a game profile.
        """
        sql = "INSERT INTO profile (id, user, game, version, use_count, name, game_id, mods, data) "
        sql += "VALUES (DEFAULT, :user_id, :game, :version, 0"

        if name is not None:
            sql += ", :name"
        else:
            sql += ", NULL"

        if game_id is not None:
            sql += ", :game_id"
        else:
            sql += ", NULL"

        if mods:
            sql += ", :mods"
        else:
            sql += ", '{}'"

        if data:
            sql += ", :data"
        else:
            sql += ", '{}'"
        sql += ") " 

        sql += "ON DUPLICATE KEY UPDATE mods = VALUES(mods), data = VALUES(data)"

        if should_inc_use:
            sql += ", use_count = use_count + 1"

        result = self.execute(sql, {"user_id": user_id, "game": game, "version": version, "name": name, "game_id": game_id, 
            "mods": json.dumps(mods), "data": json.dumps(data)})
        if result is None: return None
        return result.lastrowid

    #@cached(lifetime=30)
    def get_profile(self, game: str, version: int, profile_id: int = None, user_id: int = None, game_id: int = None) -> Optional[Dict[str, Any]]:
        sql = "SELECT * FROM profile WHERE game = :game AND version = :version AND "

        if not profile_id and not user_id and not game_id:
            self.logger.warn(f"No profile search parameters provided!")
            return None
        if profile_id:
            sql += "id = :profileid"
        if user_id:
            sql += "user = :user_id"
        if game_id:
            sql += "game_id = :game_id"        
        
        result = self.execute(sql, {"game": game, "version": version, "profileid": profile_id, "user_id": user_id, "game_id": game_id})
        
        if result is None:
            self.logger.warn(f"No profile found for id {profile_id} user_id {user_id} game_id {game_id}")
            return None
            
        return result.fetchone()
    
    def update_profile_name(self, user_id: int, game: str, version: int, new_name: str) -> None:
        """
        Update a user's username for a given game and version.
        """

        self.execute("UPDATE profile SET name = :name WHERE user = :user AND game = :game AND version = :version", 
        {"name": new_name, "user": user_id, "game": game, "version": version})

    def put_score(self, user_id: int, game: str, version: int, song_id: str, chart_id: int, score1: int, score2: int, 
        fc1: int, fc2: int, cleared: int, grade: int, data: Dict) -> Optional[int]:
        """
        Put a score attempt
        """
        sql = "INSERT INTO score_history VALUES (DEFAULT, :user_id, :game, :version, :song_id, :chart_id, :score1, :score2, :fc1, :fc2, :cleared, :grade, :data)"
        result = self.execute(sql, {"user_id": user_id, "game": game, "version": version, "song_id": song_id, "chart_id": chart_id, 
        "score1": score1, "score2": score2, "fc1": fc1, "fc2": fc2, "cleared": cleared, "grade": grade, "data": json.dumps(data)})
        if result is None:
            self.logger.warn("Failed to insert score!")
            return None
        return result.lastrowid

    @cached(lifetime=10)
    def get_scores(self, user_id: int, game: str, version: int = None, song_id: str = None, chart_id: int = None) -> Optional[List[Dict]]:
        """
        Gets all score attempts for a user from a specific game, optionally of a specific song or chart.
        """
        sql = "SELECT * FROM score WHERE user = :user_id AND game = :game "
        if song_id and chart_id:
            sql += "AND song_id = :song_id AND chart_id = :chart_id"
        elif song_id:
            sql += "AND song_id = :song_id"
        elif chart_id: 
            sql += "AND chart_id = :chart_id"
        
        result = self.execute(sql, {"user_id": user_id, "game": game, "song_id": song_id, "chart_id": chart_id})
        if result is None: return None
        return result.fetchall()

    def put_best_score(self, user_id: int, game: str, version: int, song_id: str, chart_id: int, score1: int, score2: int, 
        fc1: int, fc2: int, cleared: int, grade: int, data: Dict) -> Optional[int]:
        """
        Put a best score
        """
        sql = "INSERT INTO score VALUES (DEFAULT, :user_id, :game, :version, :song_id, :chart_id, :score1, :score2, :fc1, " + \
        ":fc2, :cleared, :grade, :data) ON DUPLICATE KEY UPDATE version=VALUES(version), score1=VALUES(score1), " + \
        "score2=VALUES(score2), fc1=VALUES(fc1), fc2=VALUES(fc2), cleared=VALUES(cleared), grade=VALUES(grade), data=VALUES(data)"

        result = self.execute(sql, {"user_id": user_id, "game": game, "version": version, "song_id": song_id, "chart_id": chart_id, 
        "score1": score1, "score2": score2, "fc1": fc1, "fc2": fc2, "cleared": cleared, "grade": grade, "data": json.dumps(data)})
        
        if result is None:
            self.logger.warn("Failed to insert score!")
            return None
        return result.lastrowid

    @cached(lifetime=10)
    def get_best_scores(self, user_id: int, game: str, song_id: str = None, chart_id: int = None) -> Optional[List[Dict]]:
        """
        Gets all best scores for a user from a specific game, or the best score of a specific chart
        """
        sql = "SELECT * FROM score WHERE user = :user_id AND game = :game "
        if song_id and chart_id:
            sql += "AND song_id = :song_id AND chart_id = :chart_id"
        elif song_id:
            sql += "AND song_id = :song_id"
        elif chart_id: 
            sql += "AND chart_id = :chart_id"
        
        result = self.execute(sql, {"user_id": user_id, "game": game, "song_id": song_id, "chart_id": chart_id})
        if result is None: return None
        return result.fetchall()
    
    def game_id_to_user_id(self, game_id: int, game: str, version: int) -> Optional[int]:
        sql = "SELECT user FROM profile WHERE game_id = :game_id AND game = :game AND version = :version"
        result = self.execute(sql, {"game_id": game_id, "game": game, "version": version})
        user = result.fetchone()
        if user is None: return None
        return user["user"]

    def put_achievement(self, user_id: int, game: str, version: int, ach_type: int, ach_id: int, data: Dict = {}) -> Optional[int]:
        sql = "INSERT INTO achievement VALUES (DEFAULT, :user_id, :game, :version, :type, :achievement_id, :data) "
        sql += "ON DUPLICATE KEY UPDATE data = VALUES(data)"
        
        result = self.execute(sql, {"user_id": user_id, "game": game, "version": version, "type": ach_type,"achievement_id": ach_id, 
        "data": json.dumps(data)})

        if result is None: return None
        return result.lastrowid

    @cached(lifetime=10)
    def get_achievements(self, user_id: int, game: str, version: int, ach_type: int = None, ach_id: int = None) -> Optional[List[Dict]]:
        sql = "SELECT * FROM achievement WHERE user = :user_id AND game = :game AND version = :version "
        if ach_type is not None and ach_id is not None:
            sql += "AND type = :type AND achievement_id = :achievement_id"
        elif ach_type is not None:
            sql += "AND type = :type"
        elif ach_id is not None: 
            sql += "AND achevement_id = :achievement_id"

        result = self.execute(sql, {"user_id": user_id, "game": game, "version": version, "type": ach_type,"achievement_id": ach_id})
        if result is None: return None
        return result.fetchall()

    def put_item(self, user_id: int, game: str, version: int, item_type: int, item_id: int, data: Dict = {}) -> Optional[int]:
        sql = "INSERT INTO item VALUES (DEFAULT, :user_id, :game, :version, :type, :item_id, :data) ON DUPLICATE KEY UPDATE data = VALUES(data)"
        result = self.execute(sql, {"user_id": user_id, "game": game, "version": version, "type": item_type,"item_id": item_id,
        "data": json.dumps(data)})
        if result is None:
            self.logger.warn(f"Failed to insert item: {user_id} {game} {item_type} {item_id}")
            return None
        return result.lastrowid

    @cached(lifetime=10)
    def get_items(self, user_id: int, game: str, version: int = None, item_type: int = None, item_id: int = None) -> Optional[List[Tuple]]:
        sql = "SELECT * FROM item WHERE user = :user_id AND game = :game "
        if version is not None:
            sql += "AND version = :version "
        if item_type is not None and item_id is not None:
            sql += "AND type = :type AND item_id = :item_id"
        elif item_type is not None:
            sql += "AND type = :type"
        elif item_id is not None: 
            sql += "AND item_id = :id"

        result = self.execute(sql, {"user_id": user_id, "game": game, "version": version, "type": item_type,"item_id": item_id})
        if result is None: return None
        return result.fetchall()
