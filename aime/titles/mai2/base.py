from datetime import datetime, date, timedelta
from multiprocessing import Event
from typing import Any, List, Dict
import logging
import pytz
import json

from aime.data import Data, Config
from aime.titles.mai2.const import Mai2Constants
from aime.titles.mai2.config import Mai2Config

class Mai2Base():
    ITEM_TYPE = {
        "character": 0,
        "map": 1,
        "login_bonus": 2,
        "ticket": 3,
    }
    GRADE = {
        "D": 0,
        "C": 1,
        "B": 2,
        "BB": 3,
        "BBB": 4,
        "A": 5,
        "AA": 6,
        "AAA": 7,
        "S": 8,
        "S+": 9,
        "SS": 10,
        "SS+": 11,
        "SSS": 12,
        "SSS+": 13
    }
    FC = {
        "None": 0,
        "FC": 1,
        "FC+": 2,
        "AP": 3,
        "AP+": 4
    }
    SYNC = {
        "None": 0,
        "FS": 1,
        "FS+": 2,
        "FDX": 3,
        "FDX+": 4
    }

    def __init__(self, cfg: Config, game_cfg: Mai2Config) -> None:
        self.core_config = cfg
        self.game_config = game_cfg
        self.game = Mai2Constants.GAME_CODE
        self.version = Mai2Constants.VER_MAIMAI_DX
        self.data = Data(cfg)
        self.logger = logging.getLogger("mai2")
        self.date_time_format = "%Y-%m-%d %H:%M:%S"

    def handle_get_game_setting_api_request(self, data: Dict):
        reboot_start = date.strftime(datetime.now() - timedelta(hours=3), self.date_time_format)
        reboot_end = date.strftime(datetime.now() - timedelta(hours=2), self.date_time_format)
        return {
        "gameSetting": {
            "isMaintenance": "false",
            "requestInterval": 10,
            "rebootStartTime": reboot_start,
            "rebootEndTime": reboot_end,
            "movieUploadLimit": 10000,
            "movieStatus": 0,
            "movieServerUri": "",
            "deliverServerUri": "",
            "oldServerUri": "",
            "usbDlServerUri": "",
            "rebootInterval": 0        
            },
        "isAouAccession": "true",
        }

    def handle_get_game_ranking_api_request(self, data: Dict) -> Dict:
        return {"length": 0, "gameRankingList": []}

    def handle_get_game_tournament_info_api_request(self, data: Dict) -> Dict:
        # TODO: Tournament support
        return {"length": 0, "gameTournamentInfoList": []}

    def handle_get_game_event_api_request(self, data: Dict) -> Dict:
        events = self.data.static.get_game_events(self.game, self.version)
        events_lst = []

        for event in events:
            if event[4] == 0: # event id 0 should never be sent
                continue
            events_lst.append({"type": event[3], 
                "id": event[4], 
                "startDate": "2017-12-05 07:00:00.0", 
                "endDate": "2099-12-31 00:00:00.0"})

        return {"type": data["type"], "length": len(events_lst), "gameEventList": events_lst}

    def handle_get_game_ng_music_id_api_request(self, data: Dict) -> Dict:
        return {"length": 0, "musicIdList": []}

    def handle_get_game_charge_api_request(self, data: Dict) -> Dict:
        return {"length": 0, "gameChargeList": []}

    def handle_upsert_client_setting_api_request(self, data: Dict) -> Dict:
        pass

    def handle_upsert_client_upload_api_request(self, data: Dict) -> Dict:
        pass

    def handle_upsert_client_bookkeeping_api_request(self, data: Dict) -> Dict:
        pass

    def handle_upsert_client_testmode_api_request(self, data: Dict) -> Dict:
        pass

    def handle_get_user_preview_api_request(self, data: Dict) -> Dict:
        p = self.data.game.get_profile(self.game, self.version, user_id = data["userId"])
        if p is None: return {} # Register
        profile = json.loads(p["data"])

        return {
            "userId": data["userId"],            
            "userName": profile["userData"]["userName"],
            "isLogin": False,
            "lastGameId": profile["userData"]["lastGameId"],
            "lastDataVersion": profile["userData"]["lastDataVersion"],
            "lastRomVersion": profile["userData"]["lastRomVersion"],
            "lastLoginDate": profile["userData"]["lastLoginDate"],
            "lastPlayDate": profile["userData"]["lastPlayDate"],            
            "playerRating": profile["userData"]["playerRating"],
            "nameplateId": 0, # Unused            
            "iconId": profile["userData"]["iconId"],
            "trophyId": 0, # Unused
            "partnerId": profile["userData"]["partnerId"],
            "frameId": profile["userData"]["frameId"],
            "dispRate": profile["userOption"]["dispRate"], # 0: all/begin, 1: disprate, 2: dispDan, 3: hide, 4: end
            "totalAwake": profile["userData"]["totalAwake"],
            "isNetMember": profile["userData"]["isNetMember"],
            "dailyBonusDate": profile["userData"]["dailyBonusDate"],
            "headPhoneVolume": profile["userOption"]["headPhoneVolume"],
            "isInherit": False # Not sure what this is or does??
        }
    
    def handle_user_login_api_request(self, data: Dict) -> Dict:
        p = self.data.game.get_profile(self.game, self.version, user_id = data["userId"])
        if p is not None:
            profile = json.loads(p["data"])
            loginCt = p["use_count"]
        else:
            loginCt = 0

        return {
            "returnCode": 1,
            "lastLoginDate": profile["userData"]["lastLoginDate"] if p is not None else "2017-12-05 07:00:00.0",
            "loginCount": loginCt,
            "consecutiveLoginCount": 0, # We don't really have a way to track this...
            "loginId": loginCt # Used with the playlog!
        }
    
    def handle_upload_user_playlog_api_request(self, data: Dict) -> Dict:
        user_id = data["userId"]
        playlog = data["userPlaylog"]

        self.data.game.put_score(user_id, self.game, self.version, playlog["musicId"], playlog["level"], playlog["achievement"],
        playlog["deluxscore"], playlog["comboStatus"], playlog["syncStatus"], int(playlog["isClear"]), playlog["scoreRank"], playlog)

        old_bests = self.data.game.get_best_scores(user_id, self.game, playlog["musicId"], playlog["level"])
        if old_bests:
            best = old_bests[0]

            self.data.game.put_best_score(user_id, self.game, self.version, playlog["musicId"], playlog["level"], 
            max(playlog["achievement"], best[6]), max(playlog["deluxscore"], best[7]), max(playlog["comboStatus"], best[8]), 
            max(playlog["syncStatus"], best[9]), max(int(playlog["isClear"]), best[10]), max(playlog["scoreRank"], best[11]), {})

        else:
            self.data.game.put_best_score(user_id, self.game, self.version, playlog["musicId"], playlog["level"], playlog["achievement"],
            playlog["deluxscore"], playlog["comboStatus"], playlog["syncStatus"], int(playlog["isClear"]), playlog["scoreRank"], {})

        pass

    def handle_upsert_user_all_api_request(self, data: Dict) -> Dict:
        user_id = data["userId"]
        upsert = data["upsertUserAll"]

        profile = {
            "userData": upsert["userData"][0],
            "userOption": upsert["userOption"][0],
            "userExtend": upsert["userExtend"][0],            
            "userRating": upsert["userRatingList"][0],
            "userGhost": upsert["userGhost"],
            "userFavoriteList": upsert["userFavoriteList"],
            "userActivityList": upsert["userActivityList"],
            "userFriendSeasonRankingList": [] if "userFriendSeasonRankingList" not in upsert else upsert["userFriendSeasonRankingList"],
        }

        # TODO: A more sophisticated way of figuring out if we need to save stuff
        if upsert["isNewCharacterList"] and int(upsert["isNewCharacterList"]) > 0:
            for char in upsert["userCharacterList"]:
                self.data.game.put_item(user_id, self.game, self.version, self.ITEM_TYPE["character"],char["characterId"], char)

        if upsert["isNewItemList"] and int(upsert["isNewItemList"]) > 0:
            for item in upsert["userItemList"]:
                self.data.game.put_item(user_id, self.game, self.version, int(item["itemKind"]) + 100, item["itemId"], item)

        if upsert["isNewLoginBonusList"] and int(upsert["isNewLoginBonusList"]) > 0:
            for login_bonus in upsert["userLoginBonusList"]:
                self.data.game.put_item(user_id, self.game, self.version, self.ITEM_TYPE["login_bonus"], login_bonus["bonusId"],
                login_bonus)

        if upsert["isNewMapList"] and int(upsert["isNewMapList"]) > 0:
            for map in upsert["userMapList"]:
                self.data.game.put_item(user_id, self.game, self.version, self.ITEM_TYPE["map"], map["mapId"], map)

        self.data.game.put_profile(user_id, self.game, self.version, data = profile, should_inc_use=True)

    def handle_user_logout_api_request(self, data: Dict) -> Dict:
        pass

    def handle_get_user_data_api_request(self, data: Dict) -> Dict:
        profile = self.data.game.get_profile(self.game, self.version, user_id=data["userId"])
        if profile is None: return
        pdata = json.loads(profile["data"])

        return {
            "userId": data["userId"],
            "userData": pdata["userData"]
        }

    def handle_get_user_extend_api_request(self, data: Dict) -> Dict:
        profile = self.data.game.get_profile(self.game, self.version, user_id=data["userId"])
        if profile is None: return
        pdata = json.loads(profile["data"])

        return {
            "userId": data["userId"],
            "userExtend": pdata["userExtend"]
        }

    def handle_get_user_option_api_request(self, data: Dict) -> Dict:
        profile = self.data.game.get_profile(self.game, self.version, user_id=data["userId"])
        if profile is None: return
        pdata = json.loads(profile["data"])

        return {
            "userId": data["userId"],
            "userOption": pdata["userOption"]
        }

    def handle_get_user_card_api_request(self, data: Dict) -> Dict:
        return {"userId": data["userId"], "nextIndex": 0, "userCardList": []}

    def handle_get_user_charge_api_request(self, data: Dict) -> Dict:
        return {"userId": data["userId"], "length": 0, "userChargeList": []}

    def handle_get_user_item_api_request(self, data: Dict) -> Dict:
        kind = int(data["nextIndex"] / 10000000000)
        user_items = self.data.game.get_items(data["userId"], self.game)
        user_item_list = []
        next_idx = 0

        for item in user_items:
            itemd = json.loads(item["data"])

            if "itemKind" in itemd and itemd["itemKind"] == kind:
                user_item_list.append({"itemKind": kind, "itemId": item["item_id"], "stock": itemd["stock"], "isValid": True})
            
            if len(user_item_list) == data["maxCount"]:
                next_idx = data["nextIndex"] + data["maxCount"] + 1
                break

        return {"userId": data["userId"], "nextIndex": next_idx, "itemKind": kind, "userItemList": user_item_list}

    def handle_get_user_character_api_request(self, data: Dict) -> Dict:
        return {"userId": data["userId"], "nextIndex": 0, "userCharacterList": []}
    
    def handle_get_user_favorite_api_request(self, data: Dict) -> Dict:
        profile = self.data.game.get_profile(self.game, self.version, user_id=data["userId"])
        if profile is None: return
        pdata = json.loads(profile["data"])

        userFavs = []
        for fav in pdata["userFavoriteList"]:
            if fav["itemKind"] == data["itemKind"]:
                userFavs.append(fav)

        return {
            "userId": data["userId"],
            "userFavoriteData": userFavs
        }

    def handle_get_user_ghost_api_request(self, data: Dict) -> Dict:
        profile = self.data.game.get_profile(self.game, self.version, user_id=data["userId"])
        if profile is None: return
        pdata = json.loads(profile["data"])

        return {
            "userId": data["userId"],
            "userGhost": pdata["userGhost"]
        }

    def handle_get_user_rating_api_request(self, data: Dict) -> Dict:
        profile = self.data.game.get_profile(self.game, self.version, user_id=data["userId"])
        if profile is None: return
        pdata = json.loads(profile["data"])

        return {
            "userId": data["userId"],
            "userRating": pdata["userRating"]
        }

    def handle_get_user_activity_api_request(self, data: Dict) -> Dict:
        profile = self.data.game.get_profile(self.game, self.version, user_id=data["userId"])
        if profile is None: return
        pdata = json.loads(profile["data"])

        return { "userActivity": pdata["userActivityList"] }

    def handle_get_user_course_api_request(self, data: Dict) -> Dict:
        return {"userId": data["userId"], "nextIndex": 0, "userCourseList": []}

    def handle_get_user_portrait_api_request(self, data: Dict) -> Dict:
        return {"length": 0, "userPortraitList": []}

    def handle_get_user_friend_season_ranking_api_request(self, data: Dict) -> Dict:
        return {"userId": data["userId"], "nextIndex": 0, "userFriendSeasonRankingList": []}

    def handle_get_user_map_api_request(self, data: Dict) -> Dict:
        return {"userId": data["userId"], "nextIndex": 0, "userMapList": []}

    def handle_get_user_login_bonus_api_request(self, data: Dict) -> Dict:
        return {"userId": data["userId"], "nextIndex": 0, "userLoginBonusList": []}

    def handle_get_user_region_api_request(self, data: Dict) -> Dict:
        return {"userId": data["userId"], "length": 0, "userRegionList": []}

    def handle_get_user_music_api_request(self, data: Dict) -> Dict:
        songs = self.data.game.get_best_scores(data["userId"], self.game)
        music_detail_list = []
        next_index = 0

        for song in songs:
            sdata = json.loads(song[12])
            music_detail_list.append({
                "musicId": song[4],
                "level": song[5],
                "playCount": 1 if not "playCount" in sdata else sdata["playCount"],
                "achievement": song[6],
                "comboStatus": song[8],
                "syncStatus": song[9],
                "deluxscoreMax": song[7],
                "scoreRank": song[11],
                })
            if len(music_detail_list) == data["maxCount"]:
                next_index = data["maxCount"] + data["nextIndex"]
                break

        return {"userId": data["userId"], "nextIndex": next_index, "userMusicList": [{"userMusicDetailList": music_detail_list}]}