# vim: set fileencoding=utf-8
import csv  # type: ignore
import argparse
import re
import copy
import io
import json
import os
import struct
import yaml  # type: ignore
import xml.etree.ElementTree as ET
import urllib

from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError  # type: ignore
from typing import Any, Dict, List, Optional, Tuple

from aime.titles.diva.const import DivaConstants
from aime.titles.chusan.const import ChusanConstants
from aime.titles.chuni.const import ChuniConstants
from aime.titles.mai2.const import Mai2Constants
from aime.titles.ongeki.const import OngekiConstants
from aime.data.config import Config

class ImportBase:
    
    def execute(self, sql: str, params: Optional[Dict[str, Any]]=None) -> Optional[CursorResult]:
    
        url = f"mysql://{config['database']['username']}:{config['database']['password']}@{config['database']['host']}/{config['database']['name']}?charset=utf8mb4"

        engine = create_engine(url)
        
        with engine.connect() as connection:
            if params is not None:
                connection.execute(sql, params)
            else:
                connection.execute(sql)
        return None
        
    def insert_music(
        self,
        game: str,
        version: int,
        song_id: int,
        chart_id: int,
        title: str,
        artist: str,
        level: str,
        chart_designer: str,
        data: Dict = {},
    ) -> Optional[int]:
        count = 0
        for chart in chart_id:
            try:
                sql = ("INSERT INTO game_music (game, version, song_id, chart_id, title, artist, level, chart_designer, data) " +
                      "VALUES ('" + game + "', " + str(version) + ", " + str(song_id) + ", " + str(chart_id[count]) + ",'" + title.replace("'", "''") + "', '" + artist.replace("'", "''") + "', '" + str(level[count]) + "', '" + str(chart_designer[count]).replace("'", "''") + "' ,'" + str(data).replace("'", '"') + "');"
                )
                if float(level[count]) > 0.0:
                    self.execute(sql)
                    print("Importing " + game + " Music ID: " + str(song_id) + " Chart " + str(count) + " for Version " + str(version))
                else:
                    print("Skipping " + game + " Music ID: " + str(song_id) + " Chart " + str(count) + " for Version " + str(version) + " because chart level is zero.")
            except IntegrityError:
                print("Skipping " + game + " Music ID: " + str(song_id) + " Chart " + str(count) + " for Version " + str(version) + " because entry already exists!")
            count += 1
        
        return None
        
    def insert_item(
        self,
        game: str,
        version: int,
        item_type: int,
        id: str,
        data: Dict = {},
    ) -> Optional[int]:
        try:
            sql = ("INSERT INTO game_item (game, version, type, item_id, data) " +
                  "VALUES ('" + game + "', " + str(version) + ", " + str(item_type) + ", " + id + ", '" + str(data).replace("'", '"') + "');"
            )
            self.execute(sql)

            print("Importing " + game + " Item ID: " + id + " for Version " + str(version))
        except IntegrityError:
            print("Skipping " + game + " Item ID: " + id + " for Version " + str(version) + " because it already exists!")
        return None
        
    def insert_event(
        self,
        game: str,
        version: int,
        event_type: int,
        id: str,
        name: str,
        data: Dict = {},
    ) -> Optional[int]:
        try:
            sql = ("INSERT INTO game_event (game, version, type, event_id, name, data) " +
                  "VALUES ('" + game + "', " + str(version) + ", " + str(event_type) + ", " + id + ", '" + name.replace("'", "''") + "', '" + str(data).replace("'", '"') + "');"
            )
            self.execute(sql)

            print("Importing " + game + " Event ID: " + id + " for Version " + str(version))
        except IntegrityError:
            print("Skipping " + game + " Event ID: " + id + " for Version " + str(version) + " because it already exists!")
        return None
        
class ImportSBZV(ImportBase):
    def __init__(
        self,
        config: Dict[str, Any],
        series: str,
        version: str,
        ) -> None:
        if version in ['0', '1']:
            actual_version = {
                '0': DivaConstants.VER_PROJECT_DIVA_ARCADE,
                '1': DivaConstants.VER_PROJECT_DIVA_ARCADE_FUTURE_TONE
            }[version]
        else:
            raise Exception("Unsupported Diva version, please select: 0 or 1")
            
    def import_diva(self, game: str, version: int, rootdir: str) -> None:
        found = False
        if "ram" in rootdir.lower():
            for subdir, dirs, files in os.walk(rootdir):
                for file in files:
                    if "ShopCatalog_" in file or "CustomizeItemCatalog_" in file:
                        found = True
                        with open(subdir + "/" + file, 'rb') as fp:
                            if "ShopCatalog_" in file:
                                item_type = 1
                            else:
                                item_type = 2
                            bytedata = fp.read()
                            strdata = bytedata.decode('UTF-8')
                            # we have to do decode twice.................................
                            strdata = urllib.parse.unquote(strdata)
                            strdata = urllib.parse.unquote(strdata).split(",")
                            for i in range(len(strdata))[::7]:
                                id = strdata[i]
                                data = {
                                    "name": strdata[i+2],
                                    "unknown_0": strdata[i+1],
                                    "points": strdata[i+3],
                                    "start_date": strdata[i+4],
                                    "end_date": strdata[i+5],
                                    "type": strdata[i+6],
                                }
                                self.insert_item(game, int(version), item_type, id, data)

                    elif "QuestInfo" in file and "QuestInfoTm" not in file:
                        found = True
                        with open(subdir + "/" + file, 'rb') as fp:
                            bytedata = fp.read()
                            strdata = bytedata.decode('UTF-8')
                            strdata = urllib.parse.unquote(strdata).replace("\n", '').split (",")
                            if strdata[0] != "***":
                                id = strdata[0]
                                name = strdata[6]
                                #idk what the unknown values are...including anyway
                                data = {
                                    "quest_order": strdata[1],
                                    "kind": strdata[2],
                                    "unknown_0" : strdata[3],
                                    "start_datetime": strdata[4],
                                    "end_datetime": strdata[5],
                                    "unknown_1": strdata[7],
                                    "unknown_2": strdata[8],
                                    "quest_enable": strdata[9],
                                }
                                event_type = 1
                                self.insert_event(game, int(version), event_type, id, name, data)

        elif "pv_db.txt" in rootdir.lower() or "mdata_pv_db.txt" in rootdir.lower():
            found = True
            difficulties = ["easy.0", "normal.0", "hard.0", "extreme.0", "extreme.1"]
            music_info = open(rootdir , mode = 'r', encoding = 'UTF-8')
            lines = str(music_info.readlines())
            lines = re.sub(r"#pv_...", "", lines)
            lines = re.sub(r"# pv_...", "", lines)
            music_info.close()
            for number in range(1000):
                title = ""
                artist = ""
                bpm = ""
                date = ""
                chart_id = [0, 1, 2, 3, 4]
                level = [-1, -1, -1, -1, -1, -1]
                chart_designer = ["", "", "", "", ""]
                if number < 10:
                    song_id = "00" + str(number)
                elif number < 100:
                    song_id = "0" + str(number)
                else:
                    song_id = str(number)
                for i in range(5):
                    temp = re.compile(song_id + ".difficulty." + difficulties[i] + ".level=PV_LV_.._.")
                    result = temp.search(lines)
                    if result is not None:
                        value = result.group().split("PV_LV_", 6)
                        level[i] = value[1].replace("_", ".")
                temp = re.search(r"(" + song_id + ".song_name=(.*?)pv_)", lines)
                if temp is not None:
                    value = temp.group()
                    result = str(value).replace("\\n', 'pv_", "").split("song_name=")
                    title = result[1]
                temp = re.search(r"(" + song_id + ".songinfo.arranger=(.*?)pv_)", lines)
                if temp is not None:
                    value = temp.group()
                    result = str(value).replace("\\n', 'pv_", "").split("arranger=")
                    artist = result[1]
                temp = re.search(r"(" + song_id + ".bpm=(.*?)pv_)", lines)
                if temp is not None:
                    value = temp.group()
                    result = str(value).replace("\\n', 'pv_", "").split("bpm=")
                    bpm = result[1]
                temp = re.search(r"(" + song_id + ".date=(.*?)pv_)", lines)
                if temp is not None:
                    value = temp.group()
                    result = str(value).replace("\\n', 'pv_", "").split("date=")
                    date = result[1]
                data = {
                    "bpm": bpm,
                    "date": date,
                }
                if title != "":
                    self.insert_music(game, int(version), song_id, chart_id, title, artist, level, chart_designer, data)
        
        if found is False:
            raise Exception('Did you type the right file? Try pv_db.txt, mdata_pv_db.txt or the ram folder.')        

class ImportSDDT(ImportBase):
    def __init__(
        self,
        config: Dict[str, Any],
        series: str,
        version: str,
        ) -> None:
        if version in ['0', '1', '2', '3', '4', '5', '6', '6', '7']:
            actual_version = {
                '0': OngekiConstants.VER_ONGEKI,
                '1': OngekiConstants.VER_ONGEKI_PLUS,
                '2': OngekiConstants.VER_ONGEKI_SUMMER,
                '3': OngekiConstants.VER_ONGEKI_SUMMER_PLUS,
                '4': OngekiConstants.VER_ONGEKI_RED,
                '5': OngekiConstants.VER_ONGEKI_RED_PLUS,
                '6': OngekiConstants.VER_ONGEKI_BRIGHT,
                '7': OngekiConstants.VER_ONGEKI_BRIGHT_MEMORY,
            }[version]
        else:
            raise Exception("Unsupported Ongeki version, please select: 0, 1, 2, 3, 4, 5, 6, or 7")
            
        
    def import_ongeki(self, game: str, version: int, rootdir: str) -> None:
        found = False
        if "event" in rootdir.lower() or "music" in rootdir.lower() or "option" in rootdir.lower() or "a000" in rootdir.lower():
            for subdir, dirs, files in os.walk(rootdir):
                for file in files:
                    if file == "Music.xml":
                        found = True
                        chart_id = [-1,-1,-1,-1,-1]
                        level = [-1,-1,-1,-1,-1]
                        chart_designer = ["", "", "", "", ""]
                        with open(subdir + "/" + file, 'rb') as fp:
                            bytedata = fp.read()
                            strdata = bytedata.decode('UTF-8')
                        root = ET.fromstring(strdata)
                        for name in root.findall('Name'):
                            song_id = name.find('id').text
                            title = name.find('str').text
                        for artistName in root.findall('ArtistName'):
                            artist = artistName.find('str').text
                        for genre_ in root.findall('Genre'):
                            genre = genre_.find('str').text
                        for fumens in root.findall('FumenData'):
                            count = 0
                            for fumens_data in fumens.findall('FumenData'):
                                chart_id[count] = count
                                level[count] = fumens_data.find('FumenConstIntegerPart').text
                                count += 1
                        data = {
                            'genre': genre,
                        }
                        self.insert_music(game, int(version), song_id, chart_id, title, artist, level, chart_designer, data)
                    
                    elif file == "Event.xml":
                        found = True
                        with open(subdir + "/" + file, 'rb') as fp:
                            bytedata = fp.read()
                            strdata = bytedata.decode('UTF-8')
                        root = ET.fromstring(strdata)
                        for name in root.findall('Name'):
                            id = name.find('id').text
                            name = name.find('str').text
                        event_type = 1
                        data = {}
                        self.insert_event(game, int(version), event_type, id, name, data)      

        if found is False:
            raise Exception('Did you type the folder path correctly? Try the event, music, A000, or option folder.')

class ImportSDBT(ImportBase):
    def __init__(
        self,
        config: Dict[str, Any],
        series: str,
        version: str,
        ) -> None:
        if version in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']:
            actual_version = {
                '0': ChuniConstants.VER_CHUNITHM,
                '1': ChuniConstants.VER_CHUNITHM_PLUS,
                '2': ChuniConstants.VER_CHUNITHM_AIR,
                '3': ChuniConstants.VER_CHUNITHM_AIR_PLUS,
                '4': ChuniConstants.VER_CHUNITHM_STAR,
                '5': ChuniConstants.VER_CHUNITHM_STAR_PLUS,
                '6': ChuniConstants.VER_CHUNITHM_AMAZON,
                '7': ChuniConstants.VER_CHUNITHM_AMAZON_PLUS,
                '8': ChuniConstants.VER_CHUNITHM_CRYSTAL,
                '9': ChuniConstants.VER_CHUNITHM_CRYSTAL_PLUS,
                '10': ChuniConstants.VER_CHUNITHM_PARADISE,
            }[version]
        else:
            raise Exception("Unsupported Chuni version, please select: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, or 10")
            
        
    def import_chuni(self, game: str, version: int, rootdir: str) -> None:
        found = False
        if "event" in rootdir.lower() or "music" in rootdir.lower() or "option" in rootdir.lower() or "a000" in rootdir.lower():
            for subdir, dirs, files in os.walk(rootdir):
                for file in files:
                    if file == "Music.xml":
                        found = True
                        chart_id = [-1,-1,-1,-1,-1,-1]
                        level = [-1,-1,-1,-1,-1,-1]
                        chart_designer = ["", "", "", "", "", ""]
                        with open(subdir + "/" + file, 'rb') as fp:
                            bytedata = fp.read()
                            strdata = bytedata.decode('UTF-8')
                        root = ET.fromstring(strdata)
                        for name in root.findall('name'):
                            song_id = name.find('id').text
                            title = name.find('str').text
                        for artistName in root.findall('artistName'):
                            artist = artistName.find('str').text
                        for genreNames in root.findall('genreNames'):
                            for list_ in genreNames.findall('list'):
                                for StringID in list_.findall('StringID'):
                                    genre = StringID.find('str').text
                        for jaketFile in root.findall('jaketFile'): #nice typo, SEGA
                            jacket_path = jaketFile.find('path').text
                        for fumens in root.findall('fumens'):
                            count = 0
                            for MusicFumenData in fumens.findall('MusicFumenData'):
                                for fumen_type in MusicFumenData.findall('type'):
                                    chart_id[count] = fumen_type.find('id').text
                                level[count] = MusicFumenData.find('level').text
                                count += 1
                        data = {
                            'genre': genre,
                            'jacket_path': jacket_path,
                        }
                        self.insert_music(game, int(version), song_id, chart_id, title, artist, level, chart_designer, data)
                    
                    elif file == "Event.xml":
                        found = True
                        with open(subdir + "/" + file, 'rb') as fp:
                            bytedata = fp.read()
                            strdata = bytedata.decode('UTF-8')
                        root = ET.fromstring(strdata)
                        for name in root.findall('name'):
                            id = name.find('id').text
                            name = name.find('str').text
                        for substances in root.findall('substances'):
                            event_type = substances.find('type').text
                        data = {}
                        self.insert_event(game, int(version), event_type, id, name, data)
                        
        if found is False:
            raise Exception('Did you type the folder path correctly? Try the event, music, A000, or option folder.')
 
    
class ImportSDHD(ImportBase):
    def __init__(
        self,
        config: Dict[str, Any],
        series: str,
        version: str,
        ) -> None:
        if version in ['0', '1', '2']:
            actual_version = {
                '0': ChusanConstants.VER_CHUNITHM,
                '1': ChusanConstants.VER_CHUNITHM_NEW,
                '2': ChusanConstants.VER_CHUNITHM_NEW_PLUS,
            }[version]
        else:
            raise Exception("Unsupported Chusan version, please select: 0, 1, or 2")
            
        
    def import_chusan(self, game: str, version: int, rootdir: str) -> None:
        found = False
        if "event" in rootdir.lower() or "avatarAccessory" in rootdir.lower() or "music" in rootdir.lower() or "option" in rootdir.lower() or "a000" in rootdir.lower():
            for subdir, dirs, files in os.walk(rootdir):
                for file in files:
                    if file == "Music.xml":
                        found = True
                        chart_id = [-1,-1,-1,-1,-1,-1]
                        level = [-1,-1,-1,-1,-1,-1]
                        chart_designer = ["", "", "", "", "", ""]
                        with open(subdir + "/" + file, 'rb') as fp:
                            bytedata = fp.read()
                            strdata = bytedata.decode('UTF-8')
                        root = ET.fromstring(strdata)
                        for name in root.findall('name'):
                            song_id = name.find('id').text
                            title = name.find('str').text
                        for artistName in root.findall('artistName'):
                            artist = artistName.find('str').text
                        for genreNames in root.findall('genreNames'):
                            for list_ in genreNames.findall('list'):
                                for StringID in list_.findall('StringID'):
                                    genre = StringID.find('str').text
                        for jaketFile in root.findall('jaketFile'): #nice typo, SEGA
                            jacket_path = jaketFile.find('path').text
                        for fumens in root.findall('fumens'):
                            count = 0
                            for MusicFumenData in fumens.findall('MusicFumenData'):
                                for fumen_type in MusicFumenData.findall('type'):
                                    chart_id[count] = fumen_type.find('id').text
                                level[count] = MusicFumenData.find('level').text
                                count += 1
                        data = {
                            'genre': genre,
                            'jacket_path': jacket_path,
                        }
                        self.insert_music(game, int(version), song_id, chart_id, title, artist, level, chart_designer, data)
                    
                    elif file == "Event.xml":
                        found = True
                        with open(subdir + "/" + file, 'rb') as fp:
                            bytedata = fp.read()
                            strdata = bytedata.decode('UTF-8')
                        root = ET.fromstring(strdata)
                        for name in root.findall('name'):
                            id = name.find('id').text
                            name = name.find('str').text
                        for substances in root.findall('substances'):
                            event_type = substances.find('type').text
                        data = {}
                        self.insert_event(game, int(version), event_type, id, name, data)
                    
                    elif file == "AvatarAccessory.xml":
                        found = True
                        with open(subdir + "/" + file, 'rb') as fp:
                            bytedata = fp.read()
                            strdata = bytedata.decode('UTF-8')
                        root = ET.fromstring(strdata)
                        for name in root.findall('name'):
                            id = name.find('id').text
                            name = name.find('str').text
                        category = root.find('category').text
                        for image in root.findall('image'):
                            icon_path = image.find('path').text
                        for texture in root.findall('texture'):
                            texture_path = texture.find('path').text
                        explain_text = root.find('explainText').text
                        data = {
                            'name': name,
                            'category': category,
                            'icon_path': icon_path,
                            'texture_path': texture_path,
                            'explain_text': explain_text,
                        }
                        self.insert_item(game, int(version), item_type, id, data)
                    
        if found is False:
            raise Exception('Did you type the folder path correctly? Try the avatarAccessory, event, music, A000, or option folder.')

class ImportSDEZ(ImportBase):
    def __init__(
        self,
        config: Dict[str, Any],
        series: str,
        version: str,
        ) -> None:
        if version in ['0', '1', '2', '3', '4']:
            actual_version = {
                '0': Mai2Constants.VER_MAIMAI_DX,
                '1': Mai2Constants.VER_MAIMAI_DX_PLUS,
                '2': Mai2Constants.VER_MAIMAI_DX_SPLASH,
                '3': Mai2Constants.VER_MAIMAI_DX_SPLASH_PLUS,
                '4': Mai2Constants.VER_MAIMAI_DX_UNIVERSE,
            }[version]
        else:
            raise Exception("Unsupported Mai2 version, please select: 0, 1, 2, 3, or 4")
            
        
    def import_mai2(self, game: str, version: int, rootdir: str) -> None:
        found = False
        if "event" in rootdir.lower() or "music" in rootdir.lower() or "option" in rootdir.lower() or "a000" in rootdir.lower():
            chart_designer = ""
            for subdir, dirs, files in os.walk(rootdir):
                for file in files:
                    if file == "Music.xml":
                        found = True
                        chart_id = [-1,-1,-1,-1,-1,-1]
                        level = [-1,-1,-1,-1,-1,-1]
                        chart_designer = ["", "", "", "", "", ""]
                        with open(subdir + "/" + file, 'rb') as fp:
                            bytedata = fp.read()
                            strdata = bytedata.decode('UTF-8')
                        root = ET.fromstring(strdata)
                        for name in root.findall('name'):
                            song_id = name.find('id').text
                            title = name.find('str').text
                        for artistName in root.findall('artistName'):
                            artist = artistName.find('str').text
                        for genreName in root.findall('genreName'):
                            genre = genreName.find('str').text
                        bpm = root.find('bpm').text
                        for notesData in root.findall('notesData'):
                            count = 0
                            for Notes in notesData.findall('Notes'):
                                chart_id[count] = count
                                level[count] = float(Notes.find('level').text + '.' + Notes.find('levelDecimal').text)
                                for notesDesigner in Notes.findall('notesDesigner'):
                                    if notesDesigner.find('id').text != 999:
                                        chart_designer[count] = notesDesigner.find('str').text
                                count += 1
                                
                        data = {
                            'genre': genre,
                            'bpm': bpm,
                        }
                        self.insert_music(game, int(version), song_id, chart_id, title, artist, level, chart_designer, data)
                    
                    elif file == "Event.xml":
                        found = True
                        with open(subdir + "/" + file, 'rb') as fp:
                            bytedata = fp.read()
                            strdata = bytedata.decode('UTF-8')
                        root = ET.fromstring(strdata)
                        for name in root.findall('name'):
                            id = name.find('id').text
                            name = name.find('str').text
                        event_type = root.find('infoType').text
                        data = {}
                        self.insert_event(game, int(version), event_type, id, name, data)
                    
        if found is False:
            raise Exception('Did you type the folder path correctly? Try the avatarAccessory, event, music, A000, or option folder.')
                                  
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Import Game Information')
    parser.add_argument(
        '--series',
        action='store',
        type=str,
        required=True,
        help='The game series we are importing.',
    )
    parser.add_argument(
        '--version',
        dest='version',
        action='store',
        type=str,
        required=True,
        help='The game version we are importing.',
    )
    parser.add_argument(
        '--folder',
        dest='folder',
        action='store',
        type=str,
        help='The base folder you are trying to read.',
    )
    parser.add_argument(
        '--txt',
        dest='txt',
        action='store',
        type=str,
        help='A text file we want to read from.',
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config/core.yaml",
        help="Core configuration for importing to DB. Defaults to 'config/core.yaml'.",
    )

    # Parse args, validate invariants.
    args = parser.parse_args()

    config = yaml.safe_load(open(args.config))  # type: ignore
 
    if args.series.upper() == ChusanConstants.GAME_CODE:
        game = ImportSDHD(config, args.series.upper(), args.version)
        if args.folder is not None:
            game.import_chusan(args.series.upper(), args.version, args.folder)
        else:
            raise Exception(
                'No folder path provided specified! ' +
                'Please provide a --folder!'
            )
            
    elif args.series.upper() == OngekiConstants.GAME_CODE:
        game = ImportSDDT(config, args.series.upper(), args.version)
        if args.folder is not None:
            game.import_ongeki(args.series.upper(), args.version, args.folder)
        else:
            raise Exception(
                'No folder path provided specified! ' +
                'Please provide a --folder!'
            )
    
    elif args.series.upper() == ChuniConstants.GAME_CODE:
        game = ImportSDBT(config, args.series.upper(), args.version)
        if args.folder is not None:
            game.import_chuni(args.series.upper(), args.version, args.folder)
        else:
            raise Exception(
                'No folder path provided specified! ' +
                'Please provide a --folder!'
            )
    
    elif args.series.upper() == Mai2Constants.GAME_CODE:
        game = ImportSDEZ(config, args.series.upper(), args.version)
        if args.folder is not None:
            game.import_mai2(args.series.upper(), args.version, args.folder)
        else:
            raise Exception(
                'No folder path provided specified! ' +
                'Please provide a --folder!'
            )
            
    elif args.series.upper() == DivaConstants.GAME_CODE:
        game = ImportSBZV(config, args.series.upper(), args.version)
        if args.txt is not None:
            game.import_diva(args.series.upper(), args.version, args.txt)
        elif args.folder is not None:
            game.import_diva(args.series.upper(), args.version, args.folder)
        else:
            raise Exception(
                'No txt file specified! ' +
                'Please provide a --txt or --folder!'
            )
    
    else:
        raise Exception('Unsupported game series!')
