import logging
import json
from datetime import datetime, timedelta

import pytz
from typing import Dict, Any

from aime.data import Config, Data
from aime.titles.chusan.const import ChusanConstants

class ChusanBase():

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
        self.logger = logging.getLogger("chusan")
        self.game = ChusanConstants.GAME_CODE
        self.version = ChusanConstants.VER_CHUNITHM
    
    def handle_game_login_api_request(self, data: Dict) -> Dict:
        return { "returnCode": 1 }
    def handle_game_logout_api_request(self, data: Dict) -> Dict:
        return { "returnCode": 1 }

    def handle_get_game_charge_api_request(self, data: Dict) -> Dict:
        game_charge: list[str, Any] = [
            {"orderId": 1, "chargeId": 701, "price": 1, "startDate": datetime.strftime((datetime.now() - timedelta(days=1)), self.date_time_format),
            "endDate": datetime.strftime((datetime.now() + timedelta(days=1)), self.date_time_format), "salePrice": 1,
            "saleStartDate": datetime.strftime((datetime.now() - timedelta(days=1)), self.date_time_format),
            "saleEndDate": datetime.strftime((datetime.now() + timedelta(days=1)), self.date_time_format)},
            
            {"orderId": 2, "chargeId": 601, "price": 1, "startDate": datetime.strftime((datetime.now() - timedelta(days=1)), self.date_time_format),
            "endDate": datetime.strftime((datetime.now() + timedelta(days=1)), self.date_time_format), "salePrice": 1,
            "saleStartDate": datetime.strftime((datetime.now() - timedelta(days=1)), self.date_time_format),
            "saleEndDate": datetime.strftime((datetime.now() + timedelta(days=1)), self.date_time_format)},
            
            {"orderId": 3, "chargeId": 2080, "price": 2, "startDate": datetime.strftime((datetime.now() - timedelta(days=1)), self.date_time_format),
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
        match_start = datetime.strftime(datetime.now() - timedelta(hours=10), self.date_time_format)
        match_end = datetime.strftime(datetime.now() + timedelta(hours=10), self.date_time_format)
        reboot_start = datetime.strftime(datetime.now() - timedelta(hours=11), self.date_time_format)
        reboot_end = datetime.strftime(datetime.now() - timedelta(hours=10), self.date_time_format)
        return {
            "gameSetting": {
                "isMaintenance": "false",
                "requestInterval": 10,
                "rebootStartTime": reboot_start,
                "rebootEndTime": reboot_end,
                "isBackgroundDistribute": "false",
                "maxCountCharacter": 300,
                "maxCountItem": 300,
                "maxCountMusic": 300,
                "matchStartTime": match_start,
                "matchEndTime": match_end,
                "matchTimeLimit": 99,
                "matchErrorLimit": 9999,
            },
                "isDumpUpload": "false",
                "isAou": "false",
        }
        
    def handle_delete_token_api_request(self, data: Dict) -> Dict:
        return { "returnCode": "1" }
    
    def handle_create_token_api_request(self, data: Dict) -> Dict:
        return { "returnCode": "1" }
        
    def handle_get_user_map_area_api_request(self, data: Dict) -> Dict:
        p = self.data.game.get_profile(self.game, self.version, user_id = data["userId"])
        if p is None: return {}
        profile = json.loads(p["data"])

        return {
            "userId": data["userId"], 
            "userMapAreaList": profile["userMapAreaList"]
        }
    
    def handle_get_user_symbol_chat_setting_api_request(self, data: Dict) -> Dict:
        return {
            "userId": data["userId"], 
            "symbolCharInfoList": []
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
        characters = self.data.game.get_items(user_id = data["userId"], game = self.game, version = self.version, item_type = self.ITEM_TYPE["character"])
        if characters is None: return {}
        characterList = []
        indexChar = 0
        
        #ID 13360 is the last character released
        for character in range(1360):
            characterList.append({"level": 50, "exMaxLv": 0, "assignIllust": 0, "param1": "50","param2": "50", "isValid": True,"isNewMark": False,
            "playCount": 99,"characterId": str(int(character)*10) ,"friendshipExp": "50" })
        
        if int(data["nextIndex"]) < 1:
            return {
                "userId": data["userId"], 
                "length": 300,
                "nextIndex": 1,
                "userCharacterList": characterList[0:300]
            }
        elif int(data["nextIndex"]) == 1:
            return {
                "userId": data["userId"], 
                "length": 300,
                "nextIndex": 2,
                "userCharacterList": characterList[301:601]
            }
        elif int(data["nextIndex"]) == 2:
            return {
                "userId": data["userId"], 
                "length": 300,
                "nextIndex": 3,
                "userCharacterList": characterList[601:901]
            }
        elif int(data["nextIndex"]) == 3:
            return {
                "userId": data["userId"], 
                "length": 300,
                "nextIndex": 4,
                "userCharacterList": characterList[901:1201]
            }
        elif int(data["nextIndex"]) == 4:
            return {
                "userId": data["userId"], 
                "length": len(characterList[1201:1360]),
                "nextIndex": -1,
                "userCharacterList": characterList[1201:1360]
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
        
        if len(profile["userCourseList"]) > 50:
            if int(data["nextIndex"])== 0:
                return {
                    "userId": data["userId"], 
                    "length": len(profile["userCourseList"][0:49]),
                    "nextIndex": 1,
                    "userCourseList": profile["userCourseList"][0:49]
                }
            elif int(data["nextIndex"]) == 1:
                return {
                    "userId": data["userId"], 
                    "length": len(profile["userCourseList"][50:101]),
                    "nextIndex": 2,
                    "userCourseList": profile["userCourseList"][50:101]
                }
            elif int(data["nextIndex"]) == 2:
                return {
                    "userId": data["userId"], 
                    "length": len(profile["userCourseList"][101:152]),
                    "nextIndex": 3,
                    "userCourseList": profile["userCourseList"][101:152]
                }
            else:
                return {
                    "userId": data["userId"], 
                    "length": len(profile["userCourseList"][152:203]),
                    "nextIndex": -1, 
                    "userCourseList": profile["userCourseList"][152:203]
                }
        return {
            "userId": data["userId"], 
            "length": len(profile["userCourseList"]),
            "nextIndex": -1,
            "userCourseList": profile["userCourseList"]
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
        p = self.data.game.get_items(user_id = data["userId"], game = self.game, version = self.version, item_type = kind)

        if p is None: 
            return {"userId": data["userId"], "nextIndex": -1, "itemKind": kind, "userItemList": []}

        items: list[Dict[str, Any]] = []
        for i in range(int(data["nextIndex"]) % 10000000000, len(p)):
            if len(items) > int(data["maxCount"]):
                break
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
            difficulties = self.data.game.get_best_scores(user_id = data["userId"], game = self.game, song_id = song["song_id"])
            songDifficultyList = []
            
            for difficulty in difficulties:
                songDifficultyList.append(json.loads(difficulty["data"]))
            
            songList.append({"length": len(difficulties), "userMusicDetailList": songDifficultyList })

        if len(songList) > 300:
            if data["nextIndex"] == 0:
                return {
                    "userId": data["userId"], 
                    "length": len(songList[0:300]), 
                    "nextIndex": 1,
                    "userMusicList": songList[0:300]
                }
            elif data["nextIndex"] == 1:
                return {
                    "userId": data["userId"], 
                    "length": len(songList[300:599]), 
                    "nextIndex": -1,
                    "userMusicList": songList[300:599]
                }
        return {
            "userId": data["userId"], 
            "length": len(songList), 
            "nextIndex": -1,
            "userMusicList": songList
        }

    def handle_get_user_option_api_request(self, data: Dict) -> Dict:
        p = self.data.game.get_profile(self.game, self.version, user_id = data["userId"])
        if p is None: return {}
        profile = json.loads(p["data"])

        return {
            "userId": data["userId"], 
            "userGameOption": profile["userGameOption"]
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
                "emoneyBrandId": 0,
                "trophyId": 0,
                # Current Selected Character (Default is penguin)
                "userCharacter": 0, #  
                # User Game Options
                "playerLevel": 0, 
                "rating": 0, 
                "headphone": 0,
                
                "chargeState": 0,
                "userNameEx": "0",
                "classEmblemMedal": "0",
                "classEmblemBase": "0",
                "battleRankId": "0"
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
            "emoneyBrandId": 0,
            "trophyId": profile["userData"]["trophyId"],
            
            # Current Selected Character
            "userCharacter": {
                "characterId": profile["userData"]["characterId"], 
                "level": "1",
                "friendshipExp": "1",
                "isValid": "true", 
                "isNewMark": "false", 
                "exMaxLv": "0", 
                "assignIllust": "0", 
                "param1": "0", 
                "param2": "0"
            },

            # User Game Options
            "playerLevel": profile["userGameOption"]["playerLevel"], 
            "rating": profile["userGameOption"]["rating"], 
            "headphone": profile["userGameOption"]["headphone"],
            "chargeState": 0,
            "userNameEx": "0",
            "banState": 0,
            "classEmblemMedal": profile["userData"]["classEmblemMedal"],
            "classEmblemBase": profile["userData"]["classEmblemBase"],
            "battleRankId": profile["userData"]["battleRankId"],
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
            "userActivityList": upsert["userActivityList"] if "userActivityList" in upsert else [],
            "userRecentRatingList": upsert["userRecentRatingList"] if "userRecentRatingList" in upsert else [],
            "userCourseList": upsert["userCourseList"] if "userCourseList" in upsert else [],
            "userChargeList": upsert["userChargeList"] if "userChargeList" in upsert else [],
            "userPlaylogList": upsert["userPlaylogList"] if "userPlaylogList" in upsert else [],
            "userDuelList": upsert["userDuelList"] if "userDuelList" in upsert else [],
            "userTeamPoint": upsert["userTeamPoint"] if "userTeamPoint" in upsert else [],
            "userRatingBaseHotList": upsert["userRatingBaseHotList"] if "userRatingBaseHotList" in upsert else [],
            "userRatingBaseList": upsert["userRatingBaseList"] if "userRatingBaseList" in upsert else [],
            "userMapAreaList": upsert["userMapAreaList"] if "userMapAreaList" in upsert else [],
            "userOverPowerList": upsert["userOverPowerList"] if "userOverPowerList" in upsert else [],
            "userEmoneyList": upsert["userEmoneyList"] if "userEmoneyList" in upsert else [],
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
