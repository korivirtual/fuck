from datetime import date, datetime, timedelta
from typing import Any, Dict
import pytz
import json

from aime.data import Config
from aime.titles.ongeki.base import OngekiBase
from aime.titles.ongeki.const import OngekiConstants

from aime.titles.ongeki.data.events import events_bright

class OngekiBright(OngekiBase):

    def __init__(self, core_cfg: Config, game_cfg: Config) -> None:
        super().__init__(core_cfg, game_cfg)
        self.version = OngekiConstants.VER_ONGEKI_BRIGHT

    def handle_get_game_setting_api_request(self, data: Dict) -> Dict:
        ret = super().handle_get_game_setting_api_request(data)
        ret["gameSetting"]["dataVersion"] = "1.30.00"
        ret["gameSetting"]["onlineDataVersion"] = "1.30.00"
        ret["gameSetting"]["maxCountCharacter"] = 50
        ret["gameSetting"]["maxCountCard"] = 300
        ret["gameSetting"]["maxCountItem"] = 300
        ret["gameSetting"]["maxCountMusic"] = 50
        ret["gameSetting"]["maxCountMusicItem"] = 300
        ret["gameSetting"]["macCountRivalMusic"] = 300
        return ret

    def handle_get_game_event_api_request(self, data: Dict) -> Dict:
        game_events: list[str, Any] = []
        for event in events_bright:
                game_events.append({
                "type": event["type"], 
                "id": event["id"], 
                "startDate": "2017-12-05 07:00:00.0", 
                "endDate": "2099-12-31 00:00:00.0"})
        return {
            "type": data["type"], 
            "length": len(game_events), 
            "gameEventList": game_events
        }
        
    def handle_get_user_rival_api_request(self, data: Dict) -> Dict:
        p = self.data.game.get_profile(self.game, self.version, user_id = data["userId"])
        if p is None: return {}
        profile = json.loads(p["data"])
        return {
            "userId": data["userId"],
            "length": len(profile["userRivalList"]),
            "userRivalList": profile["userRivalList"],
        }

    def handle_get_user_rival_music_api_request(self, data: Dict) -> Dict:
        p = self.data.game.get_profile(self.game, self.version, user_id = data["userId"])
        if p is None: return {}
        profile = json.loads(p["data"])
        return {
            "userId": data["userId"],
            "rivalUserId": data["rivalUserId"],
            "length": len(profile["userRivalList"]),
            "nextIndex": -1,
            "userRivalMusicList": profile["userRivalMusicList"],
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
            "userRatingBaseNextNewList": upsert["userRatingBaseNextNewList"] if "userRatingBaseNextNewList" in upsert else [],
            "userRatingBaseNextList": upsert["userRatingBaseNextList"] if "userRatingBaseNextList" in upsert else [],
            "userRatingBaseHotNextList": upsert["userRatingBaseHotNextList"] if "userRatingBaseHotNextList" in upsert else [],
            "userRivalList": upsert["userRivalList"] if "userRivalList" in upsert else [],
            "userRivalMusicList": upsert["userRivalMusicList"] if "userRivalMusicList" in upsert else [],
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
