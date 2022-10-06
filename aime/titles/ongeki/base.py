from datetime import date, datetime, timedelta
from typing import Any, Dict
import pytz
import json
import logging

from aime.data import Config, Data
from aime.titles.ongeki.const import OngekiConstants

class OngekiBase():

    ITEM_TYPE = {
        "character": 20,
        "story": 21,
        "card": 22,
        "deck": 23,
        "login": 24,
        "chapter": 25
    }

    def __init__(self, core_cfg: Config, game_cfg: Config) -> None:
        self.core_cfg = core_cfg
        self.game_cfg = game_cfg
        self.data = Data(core_cfg)
        self.date_time_format = "%Y-%m-%d %H:%M:%S"
        self.logger = logging.getLogger("ongeki")
        self.game = OngekiConstants.GAME_CODE
        self.version = OngekiConstants.VER_ONGEKI

    def handle_get_game_setting_api_request(self, data: Dict) -> Dict:
        reboot_start = date.strftime(datetime.now() - timedelta(hours=3), self.date_time_format)
        reboot_end = date.strftime(datetime.now() - timedelta(hours=2), self.date_time_format)
        return {
            "gameSetting": {
                "dataVersion": "1.00.00",
                "onlineDataVersion": "1.00.00",
                "isMaintenance": "false",
                "requestInterval": 10,
                "rebootStartTime": reboot_start,
                "rebootEndTime": reboot_end,
                "isBackgroundDistribute": "false",
            },
            "isDumpUpload": "false",
            "isAou": "true",
        }

    def handle_get_game_idlist_api_request(self, data: Dict) -> Dict:
        return {"type": data["type"], "length": 0, "gameIdlistList": []}

    def handle_get_game_ranking_api_request(self, data: Dict) -> Dict:
        return {"length": 0, "gameRankingList": []}
    
    def handle_get_game_point_api_request(self, data: Dict) -> Dict:
        return {"length":6,"gamePointList":[
            {"type":0,"cost":100,"startDate":"2000-01-01 05:00:00.0","endDate":"2099-01-01 05:00:00.0"},
            {"type":1,"cost":45,"startDate":"2000-01-01 05:00:00.0","endDate":"2099-01-01 05:00:00.0"},
            {"type":2,"cost":100,"startDate":"2000-01-01 05:00:00.0","endDate":"2099-01-01 05:00:00.0"},
            {"type":3,"cost":120,"startDate":"2000-01-01 05:00:00.0","endDate":"2099-01-01 05:00:00.0"},
            {"type":4,"cost":240,"startDate":"2000-01-01 05:00:00.0","endDate":"2099-01-01 05:00:00.0"},
            {"type":5,"cost":360,"startDate":"2000-01-01 05:00:00.0","endDate":"2099-01-01 05:00:00.0"}
        ]}
    
    def handle_game_login_api_request(self, data: Dict) -> Dict:
        return {"returnCode": 1, "apiName": "gameLogin"}

    def handle_game_logout_api_request(self, data: Dict) -> Dict:
        return {"returnCode": 1, "apiName": "gameLogout"}

    def handle_extend_lock_time_api_request(self, data: Dict) -> Dict:
        return {"returnCode": 1, "apiName": "ExtendLockTimeApi"}

    def handle_get_game_reward_api_request(self, data: Dict) -> Dict:
        return {"length": 0, "gameRewardList": []}

    def handle_get_game_present_api_request(self, data: Dict) -> Dict:
        return {"length": 0, "gamePresentList": []}

    def handle_get_game_message_api_request(self, data: Dict) -> Dict:
        return {"length": 0, "gameMessageList": []}

    def handle_get_game_sale_api_request(self, data: Dict) -> Dict:
        return {"length": 0, "gameSaleList": []}

    def handle_get_game_tech_music_api_request(self, data: Dict) -> Dict:
        return {"length": 0, "gameTechMusicList": []}

    def handle_extend_lock_time_request(self, data: Dict) -> Dict:
        return {"returnCode": 1, "apiName": "extendLockTime"}

    def handle_upsert_client_setting_api_request(self, data: Dict) -> Dict:
        return {"returnCode": 1, "apiName": "UpsertClientSettingApi"}

    def handle_upsert_client_testmode_api_request(self, data: Dict) -> Dict:
        return {"returnCode": 1, "apiName": "UpsertClientTestmodeApi"}

    def handle_upsert_client_bookkeeping_api_request(self, data: Dict) -> Dict:
        return {"returnCode": 1, "apiName": "upsertClientBookkeeping"}

    def handle_upsert_client_develop_api_request(self, data: Dict) -> Dict:
        return {"returnCode": 1, "apiName": "upsertClientDevelop"}

    def handle_upsert_client_error_api_request(self, data: Dict) -> Dict:
        return {"returnCode": 1, "apiName": "upsertClientError"}

    def handle_upsert_user_gplog_api_request(self, data: Dict) -> Dict:
        return {"returnCode": 1, "apiName": "UpsertUserGplogApi"}

    def handle_extend_lock_time_api_request(self, data: Dict) -> Dict:
        return {"returnCode": 1, "apiName": "ExtendLockTimeApi"}

    def handle_get_game_event_api_request(self, data: Dict) -> Dict:
        game_events: list[str, Any] = []
        return {"type": data["type"], "length": len(game_events), "gameEventList": game_events}

    def handle_get_game_id_list_api_request(self, data: Dict) -> Dict:
        game_idlist: list[str, Any] = [] #1 to 230 & 8000 to 8050
        
        if data["type"] == 1:
            for i in range(1,231):
                game_idlist.append({"type": 1, "id": i})
            return {"type": data["type"], "length": len(game_idlist), "gameIdlistList": game_idlist}
        elif data["type"] == 2:
            for i in range(8000,8051):
                game_idlist.append({"type": 2, "id": i})
            return {"type": data["type"], "length": len(game_idlist), "gameIdlistList": game_idlist}

    def handle_get_user_region_api_request(self, data: Dict) -> Dict:
        return {"userId": data["userId"], "length": 0, "userRegionList": []}

    def handle_get_user_preview_api_request(self, data: Dict) -> Dict:
        p = self.data.game.get_profile(self.game, self.version, user_id = data["userId"])
        if p is None: 
            return {
                "userId": data["userId"],            
                "isLogin": False,
                "lastLoginDate": "0000-00-00 00:00:00",
                "userName": "",
                "reincarnationNum": 0,
                "level": 0,
                "exp": 0,
                "playerRating": 0,
                "lastGameId": "",
                "lastRomVersion": "",
                "lastDataVersion": "",
                "lastPlayDate": "",     
                "nameplateId": 0,
                "trophyId": 0,  
                "cardId": 0,      
                "dispPlayerLv": 0, 
                "dispRating": 0, 
                "dispBP": 0,
                "headphone": 0,
                "banStatus": 0,
                "isWarningConfirmed": True,
            }

        profile = json.loads(p["data"])
        return {
            "userId": data["userId"],            
            "isLogin": False,
            "lastLoginDate": profile["userData"]["lastPlayDate"],
            "userName": profile["userData"]["userName"],
            "reincarnationNum": profile["userData"]["reincarnationNum"],
            "level": profile["userData"]["level"],
            "exp": profile["userData"]["exp"],
            "playerRating": profile["userData"]["playerRating"],
            "lastGameId": profile["userData"]["lastGameId"],
            "lastRomVersion": profile["userData"]["lastRomVersion"],
            "lastDataVersion": profile["userData"]["lastDataVersion"],
            "lastPlayDate": profile["userData"]["lastPlayDate"],      
            "nameplateId": profile["userData"]["nameplateId"],
            "trophyId": profile["userData"]["trophyId"],  
            "cardId": profile["userData"]["cardId"],      
            "dispPlayerLv": profile["userOption"]["dispPlayerLv"], 
            "dispRating": profile["userOption"]["dispRating"], 
            "dispBP": profile["userOption"]["dispBP"],
            "headphone": profile["userOption"]["headphone"],
            "banStatus": 0,
            "isWarningConfirmed": True,
        }

    def handle_get_user_tech_count_api_request(self, data: Dict) -> Dict:
        p = self.data.game.get_profile(self.game, self.version, user_id = data["userId"])
        if p is None: return {}
        profile = json.loads(p["data"])
        return {
            "userId": data["userId"],
            "length": len(profile["userTechCountList"]),
            "userTechCountList": profile["userTechCountList"],
        }

    def handle_get_user_tech_event_api_request(self, data: Dict) -> Dict:
        p = self.data.game.get_profile(self.game, self.version, user_id = data["userId"])
        if p is None: return {}
        profile = json.loads(p["data"])
        return {
            "userId": data["userId"],
            "length": len(profile["userTechEventList"]),
            "userTechEventList": profile["userTechEventList"],
        }

    def handle_get_user_tech_event_ranking_api_request(self, data: Dict) -> Dict:
        p = self.data.game.get_profile(self.game, self.version, user_id = data["userId"])
        if p is None: return {}
        profile = json.loads(p["data"])
        return {
            "userId": data["userId"],
            "length": 0,
            "userTechEventRankingList": [],
        }

    def handle_get_user_kop_api_request(self, data: Dict) -> Dict:
        p = self.data.game.get_profile(self.game, self.version, user_id = data["userId"])
        if p is None: return {}
        profile = json.loads(p["data"])
        return {
            "userId": data["userId"],
            "length": len(profile["userKopList"]),
            "userKopList": profile["userKopList"],
        }

    def handle_get_user_music_api_request(self, data: Dict) -> Dict:
        songs = self.data.game.get_best_scores(user_id = data["userId"], game = self.game)
        #Removed version filtering, this should allow the player to see their scores on all versions
        if songs is None: return {}
        songList = []
        
        for song in songs:
            difficulties = self.data.game.get_best_scores(user_id = data["userId"], game = self.game, song_id = song["song_id"])    
            songDifficultyList = []
            
            for difficulty in difficulties:
                songDifficultyList.append(json.loads(difficulty["data"]))
            
            songList.append({"length": len(difficulties), "userMusicDetailList": songDifficultyList })
        
        if len(songList) > 50:
            if data["nextIndex"] == 0:
                return {
                    "userId": data["userId"], 
                    "length": len(songList[0:50]),
                    "nextIndex": 1,
                    "userMusicList": songList[0:50]
                }
            elif data["nextIndex"] == 1:
                return {
                    "userId": data["userId"], 
                    "length": len(songList[50:101]), 
                    "nextIndex": 2,
                    "userMusicList": songList[50:101]
                }
            elif data["nextIndex"] == 2:
                return {
                    "userId": data["userId"], 
                    "length": len(songList[101:152]),
                    "nextIndex": 3,
                    "userMusicList": songList[101:152]
                }
            elif data["nextIndex"] == 3:
                return {
                    "userId": data["userId"], 
                    "length": len(songList[152:203]),
                    "nextIndex": 4,
                    "userMusicList": songList[152:203]
                }
            elif data["nextIndex"] == 4:
                return {
                    "userId": data["userId"], 
                    "length": len(songList[203:254]),
                    "nextIndex": 5,
                    "userMusicList": songList[203:254]
                }
            elif data["nextIndex"] == 5:
                return {
                    "userId": data["userId"], 
                    "length": len(songList[254:305]),
                    "nextIndex": 6,
                    "userMusicList": songList[254:305]
                }
            elif data["nextIndex"] == 6:
                return {
                    "userId": data["userId"], 
                    "length": len(songList[305:356]),
                    "nextIndex": -1,
                    "userMusicList": songList[305:356]
                }
        else:
            return {
                "userId": data["userId"], 
                "length": len(songList), 
                "nextIndex": -1,
                "userMusicList": songList
            }

    def handle_get_user_item_api_request(self, data: Dict) -> Dict:
        kind = data["nextIndex"] / 10000000000
        p = self.data.game.get_items(user_id = data["userId"], game = self.game, version = self.version)

        if p is None: 
            return {"userId": data["userId"], "nextIndex": -1, "itemKind": kind, "userItemList": []}

        items: list[Dict[str, Any]] = []
        for i in range(data["nextIndex"] % 10000000000, len(p)):
            if len(items) > data["maxCount"]:
                break
            if int(kind) == int(p[i][4]):
                items.append(json.loads(p[i][6]))

        xout = kind * 10000000000 + (data["nextIndex"] % 10000000000) + len(items)

        if len(items) < data["maxCount"] or data["maxCount"] == 0: nextIndex = 0
        else: nextIndex = xout

        return {"userId": data["userId"], "nextIndex": int(nextIndex), "itemKind": int(kind), "length": len(items), "userItemList": items}

    def handle_get_user_option_api_request(self, data: Dict) -> Dict:
        p = self.data.game.get_profile(self.game, self.version, user_id = data["userId"])
        if p is None: return {}
        profile = json.loads(p["data"])

        return {"userId": data["userId"], "userOption": profile["userOption"]}

    def handle_get_user_data_api_request(self, data: Dict) -> Dict:
        p = self.data.game.get_profile(self.game, self.version, user_id = data["userId"])
        if p is None: return {}
        profile = json.loads(p["data"])

        return {"userId": data["userId"], "userData": profile["userData"]}

    def handle_get_user_event_ranking_api_request(self, data: Dict) -> Dict:
        p = self.data.game.get_profile(self.game, self.version, user_id = data["userId"])
        if p is None: return {}
        profile = json.loads(p["data"])
        return {
            "userId": data["userId"],
            "length": 0,
            "userEventRankingList": [],
        }

    def handle_get_user_login_bonus_api_request(self, data: Dict) -> Dict:
        logins = self.data.game.get_items(user_id = data["userId"], game = self.game, version = self.version)
        if logins is None: return {}
        
        loginList = []
        
        for login in logins:
            if self.ITEM_TYPE["login"] == login["type"]:
                data1 = json.loads(login["data"])
                loginList.append({ "bonusId": data1["bonusId"],"bonusCount": data1["bonusCount"],"lastUpdateDate": data1["lastUpdateDate"] })
        
        return {
            "userId": data["userId"], 
            "length": len(loginList), 
            "userLoginBonusList": loginList
        }

    def handle_get_user_bp_base_request(self, data: Dict) -> Dict:
        p = self.data.game.get_profile(self.game, self.version, user_id = data["userId"])
        if p is None: return {}
        profile = json.loads(p["data"])
        return {
            "userId": data["userId"],
            "length": len(profile["userBpBaseList"]),
            "userBpBaseList": profile["userBpBaseList"],
        }

    def handle_get_user_recent_rating_api_request(self, data: Dict) -> Dict:
        p = self.data.game.get_profile(self.game, self.version, user_id = data["userId"])
        if p is None: return {}
        profile = json.loads(p["data"])
        return {
            "userId": data["userId"],
            "length": len(profile["userRecentRatingList"]),
            "userRecentRatingList": profile["userRecentRatingList"],
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

    def handle_get_user_story_api_request(self, data: Dict) -> Dict:
        stories = self.data.game.get_items(user_id = data["userId"], game = self.game, version = self.version)
        if stories is None: return {}
        
        storyList = []
        
        for story in stories:
            if self.ITEM_TYPE["story"] == story["type"]:
                data1 = json.loads(story["data"])
                storyList.append({ "storyId": data1["storyId"],"jewelCount": data1["jewelCount"],"lastChapterId": data1["lastChapterId"],
                "lastPlayMusicId": data1["lastPlayMusicId"],"lastPlayMusicLevel": data1["lastPlayMusicLevel"],"lastPlayMusicCategory": data1["lastPlayMusicCategory"] })
        
        return {
            "userId": data["userId"], 
            "length": len(storyList), 
            "userStoryList": storyList
        }

    def handle_get_user_chapter_api_request(self, data: Dict) -> Dict:
        chapters = self.data.game.get_items(user_id = data["userId"], game = self.game, version = self.version)
        if chapters is None: return {}
        chapterList = []
        
        for chapter in chapters:
            if self.ITEM_TYPE["chapter"] == chapter["type"]:
                chapterList.append(json.loads(chapter["data"]))
        
        return {
            "userId": data["userId"], 
            "length": len(chapterList), 
            "userChapterList": chapterList
        }

    def handle_get_user_training_room_by_key_api_request(self, data: Dict) -> Dict:
        p = self.data.game.get_profile(self.game, self.version, user_id = data["userId"])
        if p is None: return {}
        profile = json.loads(p["data"])
        return {
            "userId": data["userId"],
            "length": len(profile["userTrainingRoomList"]),
            "userTrainingRoomList": profile["userTrainingRoomList"],
        }

    def handle_get_user_character_api_request(self, data: Dict) -> Dict:
        characters = self.data.game.get_items(user_id = data["userId"], game = self.game, version = self.version)
        if characters is None: return {}
        characterList = []
        
        for character in characters:
            if self.ITEM_TYPE["character"] == character["type"]:
                characterList.append(json.loads(character["data"]))
        
        return {
            "userId": data["userId"], 
            "length": len(characterList), 
            "userCharacterList": characterList
        }

    def handle_get_user_card_api_request(self, data: Dict) -> Dict:
        cards = self.data.game.get_items(user_id = data["userId"], game = self.game, version = self.version)
        if cards is None: return {}
        cardList = []
        
        for card in cards:
            if self.ITEM_TYPE["card"] == card["type"]:
                data1 = json.loads(card["data"])
                cardList.append({ "exp": data1["exp"],"isNew": data1["isNew"],"level": data1["level"],
                "cardId": data1["cardId"],"created": data1["created"],"skillId": data1["skillId"],
                "maxLevel": data1["maxLevel"],"useCount": data1["useCount"],"kaikaDate": data1["kaikaDate"],
                "isAcquired": data1["isAcquired"],"printCount": data1["printCount"],"analogStock": data1["analogStock"],
                "choKaikaDate": data1["choKaikaDate"],"digitalStock": data1["digitalStock"] })
        
        return {
            "userId": data["userId"], 
            "length": len(cardList), 
            "userCardList": cardList
        }

    def handle_get_user_deck_by_key_api_request(self, data: Dict) -> Dict:
        decks = self.data.game.get_items(user_id = data["userId"], game = self.game, version = self.version)
        if decks is None: return {}
        deckList = []

        for deck in decks:
            if self.ITEM_TYPE["deck"] == deck["type"]:
                data1 = json.loads(deck["data"])
                deckList.append({ "deckId": data1["deckId"], "cardId1": data1["cardId1"], "cardId2": data1["cardId2"], "cardId3": data1["cardId3"] })

        return {
            "userId": data["userId"],
            "length": len(deckList),
            "userDeckList": deckList,
        }

    def handle_get_user_trade_item_api_request(self, data: Dict) -> Dict:
        p = self.data.game.get_profile(self.game, self.version, user_id = data["userId"])
        if p is None: return {}
        profile = json.loads(p["data"])
        return {
            "userId": data["userId"],
            "length": len(profile["userTradeItemList"]),
            "userTradeItemList": profile["userTradeItemList"],
        }

    def handle_get_user_scenario_api_request(self, data: Dict) -> Dict:
        p = self.data.game.get_profile(self.game, self.version, user_id = data["userId"])
        if p is None: return {}
        profile = json.loads(p["data"])
        return {
            "userId": data["userId"],
            "length": len(profile["userScenarioList"]),
            "userScenarioList": profile["userScenarioList"],
        }

    def handle_get_user_ratinglog_api_request(self, data: Dict) -> Dict:
        p = self.data.game.get_profile(self.game, self.version, user_id = data["userId"])
        if p is None: return {}
        profile = json.loads(p["data"])
        return {
            "userId": data["userId"],
            "length": len(profile["userRatinglogList"]),
            "userRatinglogList": profile["userRatinglogList"],
        }

    def handle_get_user_mission_point_api_request(self, data: Dict) -> Dict:
        p = self.data.game.get_profile(self.game, self.version, user_id = data["userId"])
        if p is None: return {}
        profile = json.loads(p["data"])
        return {
            "userId": data["userId"],
            "length": len(profile["userMissionPointList"]),
            "userMissionPointList": profile["userMissionPointList"],
        }

    def handle_get_user_event_point_api_request(self, data: Dict) -> Dict:
        p = self.data.game.get_profile(self.game, self.version, user_id = data["userId"])
        if p is None: return {}
        profile = json.loads(p["data"])
        return {
            "userId": data["userId"],
            "length": len(profile["userEventPointList"]),
            "userEventPointList": profile["userEventPointList"],
        }

    def handle_get_user_music_item_api_request(self, data: Dict) -> Dict:
        songs = self.data.game.get_best_scores(user_id = data["userId"], game = self.game)
        if songs is None: return {}
        
        songList = []
        
        for song in songs:
            musicid = json.loads(song["data"])
            songList.append({ "status": 2, "musicId": musicid["musicId"] })
        
        return {
            "userId": data["userId"],
            "length": len(songs),
            "userMusicItemList": songList,
        }

    def handle_get_user_event_music_api_request(self, data: Dict) -> Dict:
        p = self.data.game.get_profile(self.game, self.version, user_id = data["userId"])
        if p is None: return {}
        profile = json.loads(p["data"])
        return {
            "userId": data["userId"],
            "length": len(profile["userEventMusicList"]),
            "userEventMusicList": profile["userEventMusicList"],
        }

    def handle_get_user_boss_api_request(self, data: Dict) -> Dict:
        p = self.data.game.get_profile(self.game, self.version, user_id = data["userId"])
        if p is None: return {}
        profile = json.loads(p["data"])
        return {
            "userId": data["userId"],
            "length": len(profile["userBossList"]),
            "userBossList": profile["userBossList"],
        }

    def handle_get_user_tech_count_api_request(self, data: Dict) -> Dict:
        p = self.data.game.get_profile(self.game, self.version, user_id = data["userId"])
        if p is None: return {}
        profile = json.loads(p["data"])
        return {
            "userId": data["userId"],
            "length": len(profile["userTechCountList"]),
            "userTechCountList": profile["userTechCountList"],
        }

    def handle_upsert_user_all_api_request(self, data: Dict) -> Dict:
        upsert = data["upsertUserAll"]
        user_id = data["userId"]
        
        profile = {
            "userData": upsert["userData"][0] if "userData" in upsert else [],
            "userOption": upsert["userOption"][0] if "userOption" in upsert else [],
            "userPlaylogList": upsert["userPlaylogList"],
            "userJewelboostlogList": upsert["userJewelboostlogList"],
            "userSessionlogList": upsert["userSessionlogList"],
            "userActivityList": upsert["userActivityList"] if "userActivityList" in upsert else [],
            "userRecentRatingList": upsert["userRecentRatingList"],
            "userBpBaseList": upsert["userBpBaseList"],
            "userRatingBaseBestNewList": upsert["userRatingBaseBestNewList"] if "userRatingBaseBestNewList" in upsert else [],
            "userDeckList": upsert["userDeckList"],
            "userTrainingRoomList": upsert["userTrainingRoomList"],
            "userStoryList": upsert["userStoryList"],
            "userChapterList": upsert["userChapterList"],
            "userMusicItemList": upsert["userMusicItemList"],
            "userLoginBonusList": upsert["userLoginBonusList"],
            "userEventPointList": upsert["userEventPointList"],
            "userMissionPointList": upsert["userMissionPointList"],
            "userRatinglogList": upsert["userRatinglogList"],
            "userBossList": upsert["userBossList"],
            "userTechCountList": upsert["userTechCountList"],
            "userScenarioList": upsert["userScenarioList"],
            "userTradeItemList": upsert["userTradeItemList"],
            "userEventMusicList": upsert["userEventMusicList"],
            "userTechEventList": upsert["userTechEventList"],
            "userKopList": upsert["userKopList"],
        } 
        
        c1 = 0
        c2 = 0
        c3 = 0
        c4 = 0
        c5 = 0
        c6 = 0

        #Score system
        for song in upsert["userMusicDetailList"]:
            #put the score attempt into history
            self.data.game.put_score(user_id, self.game, self.version, song["musicId"], song["level"], song["techScoreMax"], song["battleScoreMax"], 0, 0, 0, 0, song)

            #load the current highest score from the songs table
            songsdatabase = self.data.game.get_scores(user_id = data["userId"], game = self.game, song_id = song["musicId"], chart_id = song["level"])
            if not songsdatabase:
                self.data.game.put_best_score(user_id, self.game, self.version, song["musicId"], song["level"], song["techScoreMax"], song["battleScoreMax"], 0, 0, 0, 0, song)
            for score in songsdatabase:
                data1 = json.loads(score["data"])
                if not data1 or int(song["techScoreMax"]) > int(data1["techScoreMax"]):
                    self.data.game.put_best_score(user_id, self.game, self.version, song["musicId"], song["level"], song["techScoreMax"], song["battleScoreMax"], 0, 0, 0, 0, song)
                else:
                    pass
        
        for character in upsert["userCharacterList"]:
            c1 += 1
            self.data.game.put_item(user_id, self.game, self.version, self.ITEM_TYPE["character"], c1 + self.ITEM_TYPE["character"] * 100000, character)
            
        for card in upsert["userCardList"]:
            c2 += 1
            self.data.game.put_item(user_id, self.game, self.version, self.ITEM_TYPE["card"] , c2 + self.ITEM_TYPE["card"] * 100000, card)
            
        for item in upsert["userItemList"]:          
            self.data.game.put_item(user_id, self.game, self.version, item["itemKind"], item["itemId"], item)
            
        for story in upsert["userStoryList"]:
            c3 += 1
            self.data.game.put_item(user_id, self.game, self.version, self.ITEM_TYPE["story"], c3 + self.ITEM_TYPE["story"] * 100000, story)

        for deck in upsert["userDeckList"]:
            c4 += 1
            self.data.game.put_item(user_id, self.game, self.version, self.ITEM_TYPE["deck"] , c4 + self.ITEM_TYPE["deck"] * 100000, deck)

        for login in upsert["userLoginBonusList"]:
            c5 += 1
            self.data.game.put_item(user_id, self.game, self.version, self.ITEM_TYPE["login"] , c5 + self.ITEM_TYPE["login"] * 100000, login)

        for chapter in upsert["userChapterList"]:
            c6 += 1
            self.data.game.put_item(user_id, self.game, self.version, self.ITEM_TYPE["chapter"] , c6 + self.ITEM_TYPE["chapter"] * 100000, chapter)

        self.data.game.put_profile(game=self.game, version=self.version, user_id=user_id, data=profile)

        return {'returnCode': 1, 'apiName': 'upsertUserAll'}
