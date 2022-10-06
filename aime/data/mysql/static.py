from decimal import Decimal
from typing import Any, Dict, List, Optional
from sqlalchemy import Table, Column
from sqlalchemy.types import Integer, Text, String, JSON, DECIMAL
from sqlalchemy.sql.schema import UniqueConstraint
import json

from aime.data.mysql.base import BaseData, metadata

"""
Table that holds chart information from each game
"""
game_music = Table(
    "game_music",
    metadata,
    Column('id', Integer, nullable=False, primary_key=True, autoincrement=True),
    Column('game', String(4), nullable=False),
    Column('version', Integer, nullable=False),
    Column('song_id', Integer, nullable=False),
    Column('chart_id', Integer, nullable=False),
    Column('title', String(255), nullable=False),
    Column('artist', String(255), nullable=False),    
    Column('level', DECIMAL, nullable=False),
    Column('chart_designer', Text),
    Column('data', JSON),
    UniqueConstraint('game', 'version', 'song_id', 'chart_id', name="game_music_uk"),
    mysql_charset='utf8mb4'
)

"""
Table that holds item information from each game
"""
game_item = Table(
    "game_item",
    metadata,
    Column('id', Integer, nullable=False, primary_key=True, autoincrement=True),
    Column('game', String(4), nullable=False),
    Column('version', Integer, nullable=False),
    Column('type', Integer, nullable=False),
    Column('item_id', Integer, nullable=False),
    Column('data', JSON),
    UniqueConstraint('game', 'version', 'type', 'item_id', name="game_item_uk"),
    mysql_charset='utf8mb4'
)

"""
Table that holds event information from each game
"""
game_event = Table(
    "game_event",
    metadata,
    Column('id', Integer, nullable=False, primary_key=True, autoincrement=True),
    Column('game', String(4), nullable=False),
    Column('version', Integer, nullable=False),
    Column('type', Integer, nullable=False),
    Column('event_id', Integer, nullable=False),
    Column('name', String(255), nullable=False),
    Column('data', JSON),
    UniqueConstraint('game', 'version', 'type', 'event_id', name="game_event_uk"),
    mysql_charset='utf8mb4'
)

class StaticData(BaseData):
    def put_game_music(self, game: str, ver: int, song_id: int, chart_id: int, title: str, artist: str,
        level: Decimal, chart_designer: str = "", data: Dict = {}) -> Optional[int]:
        """
        Insert a single chart into the database and retuns the id, or None on failure.
        """
        sql = "INSERT INTO game_music VALUES (DEFAULT, :game, :ver, :song_id, :chart_id, :title, :artist, :level, :chart_designer, :data)"
        sql += " ON DUPLICATE KEY UPDATE data = VALUES(data)"

        result = self.execute(sql, {"game": game, "ver": ver, "song_id": song_id, "chart_id": chart_id, "title": title, "artist": artist,
        "level": level, "chart_designer": chart_designer, "data": json.dumps(data)})

        if result is None: return None
        return result.lastrowid

    def put_game_item(self, game: str, ver: int, item_type: int, item_id: int, data: Dict = {}) -> Optional[int]:
        """
        Inserts a single item into the database and retuns the id, or None on failure.
        """
        sql = "INSERT INTO game_item VALUES (DEFAULT, :game, :ver, :type, :id, :data)"
        sql += " ON DUPLICATE KEY UPDATE data = VALUES(data)"

        result = self.execute(sql, {"game": game, "ver": ver, "type": item_type, "id": item_id, "data": json.dumps(data)})

        if result is None: return None
        return result.lastrowid

    def put_game_event(self, game: str, ver: int, event_type: int, event_id: int, name: str = "", data: Dict = {}) -> Optional[int]:
        """
        Inserts a single event into the database and retuns the id, or None on failure.
        """
        sql = "INSERT INTO game_event VALUES (DEFAULT, :game, :ver, :type, :id, :name, :data)"
        sql += " ON DUPLICATE KEY UPDATE data = VALUES(data)"
        
        result = self.execute(sql, {"game": game, "ver": ver, "type": event_type, "id": event_id, "name": name, "data": json.dumps(data)})
        
        if result is None: return None
        return result.lastrowid

    def get_game_music(self, game: str, ver: int, song_id: int = None, chart_id: int = None) -> Optional[List[List[Any]]]:
        """
        Gets information on all music from game version, or None if it does not exist.
        """
        sql = "SELECT id, song_id, chart_id, title, artist, level, chart_designer, data FROM game_music WHERE game = :game AND version = :ver"
        if song_id is not None:
            " AND song_id = :song_id"
        if chart_id is not None:
            " AND chart_id = :chart_id"
        
        result = self.execute(sql, {"game": game, "ver": ver, "song_id": song_id, "chart_id": chart_id})

        if result is None: return None
        return result.fetchall()

    def get_game_items(self, game: str, ver: int, item_type: int = None, item_id: int = None) -> Optional[List[List[Any]]]:
        """
        Gets information on all items from a game version, or None if it doesn't exist.
        """
        sql = "SELECT * FROM game_item WHERE game = :game AND version = :ver"
        if item_type is not None:
            " AND type = :type"
        if item_id is not None:
            " AND item_id = :id"
        
        result = self.execute(sql, {"game": game, "ver": ver, "type": item_type, "id": item_id})
        
        if result is None: return None
        return result.fetchall()
    
    def get_game_events(self, game: str, ver: int, event_type: int = None, event_id: int = None) -> Optional[List[List[Any]]]:
        """
        Gets information on all events ofrom a game version, or None if it doesn't exist.
        """
        sql = "SELECT * FROM game_event WHERE game = :game AND version = :ver"
        if event_type is not None:
            " AND type = :type"
        if event_id is not None:
            " AND event_id = :id"
        
        result = self.execute(sql, {"game": game, "ver": ver, "type": event_type, "id": event_id})
        
        if result is None: return None
        return result.fetchall()