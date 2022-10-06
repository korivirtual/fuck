from decimal import Decimal
import logging
import os
import re
import xml.etree.ElementTree as ET
from typing import Any, Dict, List

from aime.data import Config, Data
from aime.titles.mai2.const import Mai2Constants

class Mai2Importer():
    def __init__(self, cfg: Config, config_dir: str) -> None:
        self.config = cfg
        self.data = Data(cfg)
        self.logger = logging.getLogger("importer")
    
    def importer(self, ver: int, bin: str, opt: str):
        base_events = self.get_events(bin)
        opt_events = []
        base_music = self.get_music(bin)
        opt_music = []
        base_items = self.get_items(bin)
        opt_items = []

        if opt is not None: opt_events = self.get_events(opt)
        if opt is not None: opt_music = self.get_music(opt)
        if opt is not None: opt_items = self.get_items(opt)

        for event in base_events:
            self.data.static.put_game_event(Mai2Constants.GAME_CODE, ver, event["type"], event["id"], event["name"])
        for event in opt_events:
            self.data.static.put_game_event(Mai2Constants.GAME_CODE, ver, event["type"], event["id"], event["name"])

        for music in base_music:
            self.data.static.put_game_music(Mai2Constants.GAME_CODE, ver, music["song_id"], music["chart_id"], music["title"], music["artist"],
            music["level_decimal"], music["chart_designer"], music["data"])
        for music in opt_music:
            self.data.static.put_game_music(Mai2Constants.GAME_CODE, ver, music["song_id"], music["chart_id"], music["title"], music["artist"],
            music["level_decimal"], music["chart_designer"], music["data"])

        for item in base_items:
            self.data.static.put_game_item(Mai2Constants.GAME_CODE, ver, item["type"], item["id"], item["data"])
        for item in opt_items:
            self.data.static.put_game_item(Mai2Constants.GAME_CODE, ver, item["type"], item["id"], item["data"])

    def get_events(self, base_dir: str) -> List[Dict[str, Any]]:
        events = []
        for root, dirs, files in os.walk(f"{base_dir}"):
            for dir in dirs:
                if re.match("[A-Z]\d\d\d", dir):
                    next = f"{root}/{dir}/event"
                    self.logger.info(f"Importing events from {dir}...")

                    for root2, dirs2, files2 in os.walk(next):
                        for dir2 in dirs2:
                            info = f"{next}/{dir2}/Event.xml"

                            tree = ET.parse(info)
                            troot = tree.getroot()

                            events.append({"name":troot[1][1].text, "id":int(troot[1][0].text), "type": int(troot[2].text)})

        self.logger.info(f"Found {len(events)} events")
        return events
    
    def get_music(self, base_dir: str) -> List[Dict[str, Any]]:
        music = []
        for root, dirs, files in os.walk(f"{base_dir}"):
            for dir in dirs:
                if re.match("[A-Z]\d\d\d", dir):
                    next = f"{root}/{dir}/music"
                    self.logger.info(f"Importing charts from {dir}...")

                    for root2, dirs2, files2 in os.walk(next):
                        for dir2 in dirs2:
                            try:
                                info = f"{next}/{dir2}/Music.xml"

                                tree = ET.parse(info)
                                troot = tree.getroot()

                                for chart in troot[20]:
                                    file = f"{next}/{dir2}/{chart[0][0].text}"
                                    chart_id = int(chart[0][0].text.split("_")[1][:-4])

                                    if not chart[1].text == "0":
                                        
                                            with open(file, "r") as f:
                                                lines = f.readlines()
                                                bpm = lines[2].replace("\n","").split("	")

                                                music.append({"title":troot[4][1].text, "artist":troot[7][1].text, "level": int(chart[1].text),
                                                "song_id": int(troot[4][0].text), "chart_id": chart_id, "chart_designer": chart[3][1].text,
                                                "level_decimal": Decimal(f"{chart[1].text}.{chart[2].text}"), 
                                                "data": { "max_notes": int(chart[6].text), "bpm": int(troot[9].text), "bpm_start": bpm[1], 
                                                "bpm_mode": bpm[2], "bpm_max": bpm[3], "bpm_min": bpm[4], "added_ver": troot[11][1].text, 
                                                "title_katakana": troot[6].text, "genre": troot[8][1].text}})

                            except FileNotFoundError as e:
                                self.logger.warning(f"Could not load Music.xml for {dir2}")


        self.logger.info(f"Found {len(music)} charts")
        return music
    
    def get_items(self, base_dir: str) -> List[Dict[str, Any]]:
        """
        chara, course (if exists), frame, loginBonus, map, partner, plate, ticket, title, udeme (if exists)
        """
        items = []
        for root, dirs, files in os.walk(f"{base_dir}"):
            for dir in dirs:
                if re.match("A\d\d\d", dir):
                    next = f"{root}/{dir}/chara"
                    self.logger.info(f"Importing characters from {dir}...")
                    try:
                        tree = ET.parse(next)
                        troot = tree.getroot()
                    except:
                        self.logger.warning(f"Could not load characters from {dir} due to error")

                    next = f"{root}/{dir}/course"
                    self.logger.info(f"Importing courses from {dir}...")
                    try:
                        tree = ET.parse(next)
                        troot = tree.getroot()
                    except:
                        self.logger.warning(f"Could not load courses from {dir} due to error")

                    next = f"{root}/{dir}/ticket"
                    self.logger.info(f"Importing tickets from {dir}...")
                    try:
                        for root2, dirs2, files2 in os.walk(f"{next}"):
                            for dir2 in dirs2:
                                tree = ET.parse(f"{root2}/{dir2}/Ticket.xml")
                                troot = tree.getroot()

                                items.append({"type": 0})
                    except:
                        self.logger.warning(f"Could not load tickets from {dir} due to error")


        self.logger.info(f"Found {len(items)} items")
        return items
