import logging
import json
from datetime import datetime, timedelta
from time import strftime

import pytz
from typing import Dict, Any

from aime.data import Config, Data
from aime.titles.chuni.const import ChuniConstants

class ChuniBase():
    
    ITEM_TYPE = {
        "character": 20,
        "story": 21,
        "card": 22
    }

    def __init__(self, core_cfg: Config, game_cfg: Config) -> None:
        self.core_cfg = core_cfg
        self.game_cfg = game_cfg
        self.data = Data(core_cfg)
        self.date_time_format = "%Y-%m-%d %H:%M:%S"
        self.logger = logging.getLogger("chuni")
        self.game = ChuniConstants.GAME_CODE
        self.version = ChuniConstants.VER_CHUNITHM
    
    def handle_game_login_api_request(self, data: Dict) -> Dict:
        return { "returnCode": 1 }
    
    def handle_game_logout_api_request(self, data: Dict) -> Dict:
        return { "returnCode": 1 }

    def handle_get_game_charge_api_request(self, data: Dict) -> Dict:
        game_charge: list[str, Any] = [
            {"orderId": 1, "chargeId": 2060, "price": 1, "startDate": datetime.strftime((datetime.now() - timedelta(days=1)), self.date_time_format),
            "endDate": datetime.strftime((datetime.now() + timedelta(days=1)), self.date_time_format), "salePrice": 1,
            "saleStartDate": datetime.strftime((datetime.now() - timedelta(days=1)), self.date_time_format),
            "saleEndDate": datetime.strftime((datetime.now() + timedelta(days=1)), self.date_time_format)},
            
            {"orderId": 2, "chargeId": 2310, "price": 1, "startDate": datetime.strftime((datetime.now() - timedelta(days=1)), self.date_time_format),
            "endDate": datetime.strftime((datetime.now() + timedelta(days=1)), self.date_time_format), "salePrice": 1,
            "saleStartDate": datetime.strftime((datetime.now() - timedelta(days=1)), self.date_time_format),
            "saleEndDate": datetime.strftime((datetime.now() + timedelta(days=1)), self.date_time_format)},
            
            {"orderId": 3, "chargeId": 2230, "price": 2, "startDate": datetime.strftime((datetime.now() - timedelta(days=1)), self.date_time_format),
            "endDate": datetime.strftime((datetime.now() + timedelta(days=1)), self.date_time_format), "salePrice": 2,
            "saleStartDate": datetime.strftime((datetime.now() - timedelta(days=1)), self.date_time_format),
            "saleEndDate": datetime.strftime((datetime.now() + timedelta(days=1)), self.date_time_format)},
        ]
        return {
            "length": len(game_charge), 
            "gameChargeList": game_charge
        }

    def handle_get_game_event_api_request(self, data: Dict) -> Dict:
        game_events: list[str, Any] = []
        return {
            "type": data["type"], 
            "length": len(game_events), 
            "gameEventList": game_events
        }

    def handle_get_game_idlist_api_request(self, data: Dict) -> Dict:
        return { "type": data["type"], "length": 0, "gameIdlistList": [] }

    def handle_get_game_message_api_request(self, data: Dict) -> Dict:
        return { "type": data["type"], "length": "0", "gameMessageList": [] }

    def handle_get_game_ranking_api_request(self, data: Dict) -> Dict:
        return { "type": data["type"], "gameRankingList": [] }

    def handle_get_game_sale_api_request(self, data: Dict) -> Dict:
        return { "type": data["type"], "length": 0, "gameSaleList": [] }

    def handle_get_game_setting_api_request(self, data: Dict) -> Dict:
        reboot_start = datetime.strftime(datetime.now() - timedelta(hours=4), self.date_time_format)
        reboot_end = datetime.strftime(datetime.now() - timedelta(hours=3), self.date_time_format)
        return {
            "gameSetting": {
                "dataVersion": "1.00.00",
                "isMaintenance": "false",
                "requestInterval": 10,
                "rebootStartTime": reboot_start,
                "rebootEndTime": reboot_end,
                "isBackgroundDistribute": "false",
                "maxCountCharacter": 300,
                "maxCountItem": 300,
                "maxCountMusic": 300,
            },
                "isDumpUpload": "false",
                "isAou": "false",
        }

    def handle_get_user_activity_api_request(self, data: Dict) -> Dict:
        p = self.data.game.get_profile(self.game, self.version, user_id = data["userId"])
        if p is None: return {}
        profile = json.loads(p["data"])
        
        user_activity = []
        
        for activity in profile["userActivityList"]:
            if activity["kind"] == data["kind"]:
                    user_activity.append(activity)
        return {
          "userId": data["userId"], 
          "length": len(profile["userActivityList"]),
          "kind": data["kind"],
          "userActivityList": user_activity
        }

    def handle_get_user_character_api_request(self, data: Dict) -> Dict:
        characters = self.data.game.get_items(user_id = data["userId"], game = self.game, version = self.version)
        if characters is None: return {}
        characterList = []
        
        for character in characters:
            if self.ITEM_TYPE["character"] == character["type"]:
                data1 = json.loads(character["data"])
                characterList.append({"level": data1["level"],"param1": data1["param1"],"param2": data1["param2"],
                "isValid": data1["isValid"],"skillId": data1["skillId"],"isNewMark": data1["isNewMark"],
                "playCount": data1["playCount"],"characterId": data1["characterId"],"friendshipExp": data1["friendshipExp"] })
        
        if int(data["nextIndex"]) <= 300:
            return {
                "userId": data["userId"], 
                "length": len(characterList[0:299]),
                "nextIndex": 301,
                "userCharacterList": characterList[0:299]
            }
        elif int(data["nextIndex"]) == 301:
            return {
                "userId": data["userId"], 
                "length": len(characterList[300:599]),
                "nextIndex": 601,
                "userCharacterList": characterList[300:599]
            }
        elif int(data["nextIndex"]) == 601:
            return {
                "userId": data["userId"], 
                "length": len(characterList[600:899]),
                "nextIndex": 901,
                "userCharacterList": characterList[600:899]
            }
        else:
            return {
                "userId": data["userId"], 
                "length": len(characterList[900:1199]),
                "nextIndex": -1, 
                "userCharacterList": characterList[900:1199]
            }

    def handle_get_user_charge_api_request(self, data: Dict) -> Dict:
        p = self.data.game.get_profile(self.game, self.version, user_id = data["userId"])
        if p is None: return {}
        profile = json.loads(p["data"])

        return {
            "userId": data["userId"], 
            "length": len(profile["userChargeList"]),
            "userChargeList": profile["userChargeList"]
        }

    def handle_get_user_course_api_request(self, data: Dict) -> Dict:
        p = self.data.game.get_profile(self.game, self.version, user_id = data["userId"])
        if p is None: return {}
        profile = json.loads(p["data"])
                
        if int(data["nextIndex"]) <= 300:
            return {
                "userId": data["userId"], 
                "length": len(profile["userCourseList"][0:300]),
                "nextIndex": 301,
                "userCourseList": profile["userCourseList"][0:300]
            }
        elif int(data["nextIndex"]) == 301:
            return {
                "userId": data["userId"], 
                "length": len(profile["userCourseList"][301:601]),
                "nextIndex": 602,
                "userCourseList": profile["userCourseList"][301:601]
            }
        elif int(data["nextIndex"]) == 602:
            return {
                "userId": data["userId"], 
                "length": len(profile["userCourseList"][601:901]),
                "nextIndex": 902,
                "userCourseList": profile["userCourseList"][601:901]
            }
        else:
            return {
                "userId": data["userId"], 
                "length": len(profile["userCourseList"][901:1201]),
                "nextIndex": -1, 
                "userCourseList": profile["userCourseList"][901:1201]
            }

    def handle_get_user_data_api_request(self, data: Dict) -> Dict:
        p = self.data.game.get_profile(self.game, self.version, user_id = data["userId"])
        if p is None: return {}
        profile = json.loads(p["data"])
        profile["userData"]["userName"] = self.readWtf8(profile["userData"]["userName"])
        return {
            "userId": data["userId"], 
            "userData": profile["userData"]
        }

    def handle_get_user_data_ex_api_request(self, data: Dict) -> Dict:
        p = self.data.game.get_profile(self.game, self.version, user_id = data["userId"])
        if p is None: return {}
        profile = json.loads(p["data"])

        data1 = {
            "compatibleCmVersion": "",
            "medal": profile["userDataEx"][0]["medal"],
            "mapIconId": profile["userDataEx"][0]["mapIconId"],
            "voiceId": profile["userDataEx"][0]["voiceId"],
            "ext1": profile["userDataEx"][0]["ext1"],
            "ext2": profile["userDataEx"][0]["ext2"],
            "ext3": profile["userDataEx"][0]["ext3"],
            "ext4": profile["userDataEx"][0]["ext4"],
            "ext5": profile["userDataEx"][0]["ext5"],
            "ext6": profile["userDataEx"][0]["ext6"],
            "ext7": profile["userDataEx"][0]["ext7"],
            "ext8": profile["userDataEx"][0]["ext8"],            
            "ext9": profile["userDataEx"][0]["ext9"],  
            "ext10": profile["userDataEx"][0]["ext10"],
            "ext11": profile["userDataEx"][0]["ext11"],
            "ext12": profile["userDataEx"][0]["ext12"],
            "ext13": profile["userDataEx"][0]["ext13"],
            "ext14": profile["userDataEx"][0]["ext14"],
            "ext15": profile["userDataEx"][0]["ext15"],
            "ext16": profile["userDataEx"][0]["ext16"],
            "ext17": profile["userDataEx"][0]["ext17"],
            "ext18": profile["userDataEx"][0]["ext18"],
            "ext19": profile["userDataEx"][0]["ext19"],
            "ext20": profile["userDataEx"][0]["ext20"],
            "extStr1": profile["userDataEx"][0]["extStr1"],
            "extStr2": profile["userDataEx"][0]["extStr2"],
            "extStr3": profile["userDataEx"][0]["extStr3"],
            "extStr4": profile["userDataEx"][0]["extStr4"],
            "extStr5": profile["userDataEx"][0]["extStr5"],
            "extLong1": profile["userDataEx"][0]["extLong1"],
            "extLong2": profile["userDataEx"][0]["extLong2"],
            "extLong3": profile["userDataEx"][0]["extLong3"],
            "extLong4": profile["userDataEx"][0]["extLong4"],
            "extLong5": profile["userDataEx"][0]["extLong5"],
        }
        
        return {
            "userId": data["userId"], 
            "userDataEx": data1
        }

    def handle_get_user_duel_api_request(self, data: Dict) -> Dict:
        p = self.data.game.get_profile(self.game, self.version, user_id = data["userId"])
        if p is None: return {}
        profile = json.loads(p["data"])

        return {
            "userId": data["userId"], 
            "length": len(profile["userDuelList"]),
            "userDuelList": profile["userDuelList"]
        }

    def handle_get_user_favorite_item_api_request(self, data: Dict) -> Dict:
        p = self.data.game.get_profile(self.game, self.version, user_id = data["userId"])
        if p is None: return {}
        profile = json.loads(p["data"])

        return {
            "userId": data["userId"], 
            "length": 0,
            "kind": data["kind"], 
            "nextIndex": -1, 
            "userFavoriteItemList": []
        }

    def handle_get_user_favorite_music_api_request(self, data: Dict) -> Dict:
        p = self.data.game.get_profile(self.game, self.version, user_id = data["userId"])
        if p is None: return {}
        profile = json.loads(p["data"])

        return {
            "userId": data["userId"], 
            "length": 0,
            "userFavoriteMusicList": []
        }

    def handle_get_user_item_api_request(self, data: Dict) -> Dict:
        kind = int(int(data["nextIndex"]) / 10000000000)
        p = self.data.game.get_items(user_id = data["userId"], game = self.game, version = self.version)

        if p is None: 
            return {"userId": data["userId"], "nextIndex": -1, "itemKind": kind, "userItemList": []}

        items: list[Dict[str, Any]] = []
        for i in range(int(data["nextIndex"]) % 10000000000, len(p)):
            if len(items) > int(data["maxCount"]):
                break
            if int(kind) == int(p[i][4]):
                items.append(json.loads(p[i][6]))

        xout = kind * 10000000000 + int(data["nextIndex"]) % 10000000000 + len(items)

        if len(items) < int(data["maxCount"]): nextIndex = 0
        else: nextIndex = xout

        return {"userId": data["userId"], "nextIndex": nextIndex, "itemKind": kind, "length": len(items), "userItemList": items}

    def handle_get_user_login_bonus_api_request(self, data: Dict) -> Dict:
        p = self.data.game.get_profile(self.game, self.version, user_id = data["userId"])
        if p is None: return {}
        profile = json.loads(p["data"])

        return {
            "userId": data["userId"], 
            "length": 0,
            "userLoginBonusList": []
        }

    def handle_get_user_map_api_request(self, data: Dict) -> Dict:
        p = self.data.game.get_profile(self.game, self.version, user_id = data["userId"])
        if p is None: return {}
        profile = json.loads(p["data"])

        return {
            "userId": data["userId"], 
            "length": len(profile["userMapList"]),
            "userMapList": profile["userMapList"]
        }

    def handle_get_user_music_api_request(self, data: Dict) -> Dict:
        songs = self.data.game.get_best_scores(user_id = data["userId"], game = self.game)
        if songs is None: return {}
        songList = []
            
        for song in songs:
            # Put a cap at 2083 as songs with an ID higher than this will cause profile corruption due to A033 and A034
            if int(song["song_id"]) < 2083:
                difficulties = self.data.game.get_best_scores(user_id = data["userId"], game = self.game, song_id = song["song_id"])
                songDifficultyList = []
            
                for difficulty in difficulties:
                    songDifficultyList.append(json.loads(difficulty["data"]))
            
                songList.append({"length": len(difficulties), "userMusicDetailList": songDifficultyList })
            elif int(song["song_id"]) > 8000:
                difficulties = self.data.game.get_best_scores(user_id = data["userId"], game = self.game, song_id = song["song_id"])
                songDifficultyList = []
            
                for difficulty in difficulties:
                    songDifficultyList.append(json.loads(difficulty["data"]))
            
                songList.append({"length": len(difficulties), "userMusicDetailList": songDifficultyList })

        return {
            "userId": data["userId"], 
            "length": len(songList[0:300]), 
            "nextIndex": -1,
            "userMusicList": songList[0:300] #240
        }

    def handle_get_user_option_api_request(self, data: Dict) -> Dict:
        p = self.data.game.get_profile(self.game, self.version, user_id = data["userId"])
        if p is None: return {}
        profile = json.loads(p["data"])

        return {
            "userId": data["userId"], 
            "userGameOption": profile["userGameOption"]
        }

    def handle_get_user_option_ex_api_request(self, data: Dict) -> Dict:
        p = self.data.game.get_profile(self.game, self.version, user_id = data["userId"])
        if p is None: return {}
        profile = json.loads(p["data"])

        return {
            "userId": data["userId"], 
            "userGameOptionEx": profile["userGameOptionEx"]
        }

    def readWtf8(self, src):
        return bytes([ord(c) for c in src]).decode("utf-8")

    def handle_get_user_preview_api_request(self, data: Dict) -> Dict:
        p = self.data.game.get_profile(self.game, self.version, user_id = data["userId"])
        if p is None: 
            return {
                "userId": 1, 
                # Current Login State
                "isLogin": False,
                "lastLoginDate": "1970-01-01 09:00:00",
                # User Profile
                "userName": "",
                "reincarnationNum": 0,
                "level": 0,
                "exp": 0,
                "playerRating": 0,
                "lastGameId": "",
                "lastRomVersion": "",
                "lastDataVersion": "",
                "lastPlayDate": "",     
                "trophyId": 0,  
                # Current Selected Character (Default is penguin)
                "userCharacter": 0,     
                # User Game Options
                "playerLevel": 0, 
                "rating": 0, 
                "headphone": 0,
            }
        profile = json.loads(p["data"])
        name = b''
        for c in profile["userData"]["userName"]:
            name += c.encode('utf-8')
        print(name.decode('utf-8'))
        
        data1 = {
            "userId": data["userId"],    
            # Current Login State            
            "isLogin": False,
            "lastLoginDate": profile["userData"]["lastPlayDate"],
            # User Profile
            "userName": self.readWtf8(profile["userData"]["userName"]),
            "reincarnationNum": profile["userData"]["reincarnationNum"],
            "level": profile["userData"]["level"],
            "exp": profile["userData"]["exp"],
            "playerRating": profile["userData"]["playerRating"],
            "lastGameId": profile["userData"]["lastGameId"],
            "lastRomVersion": profile["userData"]["lastRomVersion"],
            "lastDataVersion": profile["userData"]["lastDataVersion"],
            "lastPlayDate": profile["userData"]["lastPlayDate"],            
            "trophyId": profile["userData"]["trophyId"],  
            "nameplateId": profile["userData"]["nameplateId"],
            # Current Selected Character
            "userCharacter": {"level": "1", "param1": "0", "param2": "0", "isValid": "true", "skillId": "1", "isNewMark": "false", "playCount": "1", "characterId": profile["userData"]["characterId"], "friendshipExp": "1"},
            # User Game Options
            "playerLevel": profile["userGameOption"]["playerLevel"], 
            "rating": profile["userGameOption"]["rating"], 
            "headphone": profile["userGameOption"]["headphone"],
            "chargeState": "1",
            "userNameEx": self.readWtf8(profile["userData"]["userName"]),
        }
        return data1

    def handle_get_user_recent_rating_api_request(self, data: Dict) -> Dict:
        p = self.data.game.get_profile(self.game, self.version, user_id = data["userId"])
        if p is None: return {}
        profile = json.loads(p["data"])
        return {
            "userId": data["userId"],
            "length": len(profile["userRecentRatingList"]),
            "userRecentRatingList": profile["userRecentRatingList"],
        }

    def handle_get_user_region_api_request(self, data: Dict) -> Dict:
        return {
            "userId": data["userId"],
            "length": 0,
            "userRegionList": [],
        }

    def handle_get_user_team_api_request(self, data: Dict) -> Dict:
        # TODO: Team
        return {
            "userId": data["userId"],
            "teamId": 0
        }
    
    def handle_get_team_course_setting_api_request(self, data: Dict) -> Dict:
        return {
            "userId": data["userId"],
            "length": 0,
            "nextIndex": 0,
            "teamCourseSettingList": [],
        }

    def handle_get_team_course_rule_api_request(self, data: Dict) -> Dict:
        return {
            "userId": data["userId"],
            "length": 0,
            "nextIndex": 0,
            "teamCourseRuleList": [],
        }

    def handle_upsert_user_all_api_request(self, data: Dict) -> Dict:
        upsert = data["upsertUserAll"]
        user_id = data["userId"]
        
        profile = {
            "userData": upsert["userData"][0],
            "userGameOption": upsert["userGameOption"][0],
            "userGameOptionEx": upsert["userGameOptionEx"],
            "userMapList": upsert["userMapList"] if "userMapList" in upsert else [],
            "userActivityList": upsert["userActivityList"] if "userActivityList" in upsert else [],
            "userPlaylogList": upsert["userPlaylogList"] if "userPlaylogList" in upsert else [],
            "userChargeList": upsert["userChargeList"] if "userChargeList" in upsert else [],
            "userCourseList": upsert["userCourseList"] if "userCourseList" in upsert else [],
            "userDataEx": upsert["userDataEx"] if "userDataEx" in upsert else [],
            "userDuelList": upsert["userDuelList"] if "userDuelList" in upsert else [],
            "userRecentRatingList": upsert["userRecentRatingList"] if "userRecentRatingList" in upsert else [],
        }

        c1 = 0
        
        #Score system
        for song in upsert["userMusicDetailList"]:
            #put the score attempt into history
            self.data.game.put_score(user_id, self.game, self.version, song["musicId"], song["level"], song["scoreMax"], 0, 0, 0, 0, 0, song)

            #load the current highest score from the songs table
            songsdatabase = self.data.game.get_scores(user_id = user_id, game = self.game, song_id = song["musicId"], chart_id = song["level"])
            
            if not songsdatabase:
                self.data.game.put_best_score(user_id, self.game, self.version, song["musicId"], song["level"], song["scoreMax"], 0, 0, 0, 0, 0, song)
            for score in songsdatabase:
                data1 = json.loads(score["data"])
                if not data1 or int(song["scoreMax"]) > int(data1["scoreMax"]):
                    self.data.game.put_best_score(user_id, self.game, self.version, song["musicId"], song["level"], song["scoreMax"], 0, 0, 0, 0, 0, song)
                else:
                    pass

        for character in upsert["userCharacterList"]:
            c1 += 1
            self.data.game.put_item(user_id, self.game, self.version, self.ITEM_TYPE["character"], c1 + self.ITEM_TYPE["character"] * 100000, character)
        
        if "userItemList" in upsert:
            for item in upsert["userItemList"]:
                self.data.game.put_item(user_id, self.game, self.version, item["itemKind"], item["itemId"], item)
            
        self.data.game.put_profile(game=self.game, version=self.version, user_id=user_id, data=profile)
        return { "returnCode": "1" }

    def handle_upsert_user_chargelog_api_request(self, data: Dict) -> Dict:
        return { "returnCode": "1" }

    def handle_upsert_client_bookkeeping_api_request(self, data: Dict) -> Dict:
        return { "returnCode": "1" }

    def handle_upsert_client_develop_api_request(self, data: Dict) -> Dict:
        return { "returnCode": "1" }

    def handle_upsert_client_error_api_request(self, data: Dict) -> Dict:
        return { "returnCode": "1" }

    def handle_upsert_client_setting_api_request(self, data: Dict) -> Dict:
        return { "returnCode": "1" }

    def handle_upsert_client_testmode_api_request(self, data: Dict) -> Dict:
        return { "returnCode": "1" }
