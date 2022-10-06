import logging
import json
from decimal import Decimal
from base64 import b64encode
from typing import Any, Dict
from hashlib import md5
from datetime import datetime

from aime.data import Config, Data
from aime.titles.cxb.config import CxbConfig
from aime.titles.cxb.const import CxbConstants

class CxbBase():
    def __init__(self, core_cfg: Config, game_cfg: CxbConfig) -> None:
        self.core_config = core_cfg
        self.game_config = game_cfg
        self.data = Data(core_cfg)
        self.game = CxbConstants.GAME_CODE
        self.logger = logging.getLogger("cxb")
        self.version = CxbConstants.VER_CROSSBEATS_REV
        
    def handle_action_rpreq_request(self, data: Dict) -> Dict:
        return({})
    
    def handle_action_hitreq_request(self, data: Dict) -> Dict:
        return({"data":[]})

    def handle_auth_usercheck_request(self, data: Dict) -> Dict:
        profile = self.data.game.get_profile(self.game, self.version, user_id=data["usercheck"]["authid"])        
        if profile is not None:
            return({"exist": "true", "logout": "true"})
        return({"exist": "false", "logout": "true"})

    def handle_auth_entry_request(self, data: Dict) -> Dict:
        token = self.data.user.generate_id()
        return({"token": token, "uid": token})

    def handle_auth_login_request(self, data: Dict) -> Dict:     
        profile = self.data.game.get_profile(self.game, self.version, user_id=data["login"]["authid"])
            
        if profile is not None:
            return({"token": profile["game_id"], "uid": profile["game_id"]})
        return({})
    
    def handle_action_loadrange_request(self, data: Dict) -> Dict:
        range_start = data['loadrange']['range'][0]
        range_end = data['loadrange']['range'][1]
        uid = data['loadrange']['uid']
        
        extId = self.data.game.game_id_to_user_id(uid, self.game, self.version)
        profile = self.data.game.get_profile(self.game, self.version, user_id=extId)
        
        profile_data = json.loads(profile["data"])
        songs = self.data.game.get_best_scores(user_id = extId, game = self.game)
        index = []
        data1 = []
        versionindex = []

        if int(range_start) == 800000:
            return({"index":range_start, "data":[], "version":10400})
        
        for val in profile_data["index"]:
            if not ( int(range_start) <= int(val) <=  int(range_end) ):
                continue
            #Prevent loading of the coupons within the profile to use the force unlock instead
            elif 500 <= int(val) <= 510:
                continue
            #Prevent loading of songs saved in the profile
            elif 100000 <= int(val) <= 110000:
                continue
            #Prevent loading of the shop list / unlocked titles & icons saved in the profile
            elif 200000 <= int(val) <= 210000:
                continue
            else:
                offset = profile_data["index"].index(val)
                data0 = json.loads(profile_data["data"][offset])

                index.append(val)
                data1.append(b64encode(bytes(json.dumps(data0, separators=(',', ':')), 'utf-8')).decode('utf-8'))

        # Coupons
        
        for i in range(500,510):
            index.append(str(i))
            couponid = int(i) - 500
            dataValue = [{
                "couponId":str(couponid),
                "couponNum":"1",
                "couponLog":[],
            }]
            data1.append(b64encode(bytes(json.dumps(dataValue[0], separators=(',', ':')), 'utf-8')).decode('utf-8'))
        

        # ShopList_Title
        for i in range(200000,201451):
            index.append(str(i))
            shopid = int(i) - 200000
            dataValue = [{
                "shopId":shopid,
                "shopState":"2",
                "isDisable":"t",
                "isDeleted":"f",
                "isSpecialFlag":"f"
            }]
            data1.append(b64encode(bytes(json.dumps(dataValue[0], separators=(',', ':')), 'utf-8')).decode('utf-8'))

        #ShopList_Icon
        for i in range(202000,202264):
            index.append(str(i))
            shopid = int(i) - 200000
            dataValue = [{
                "shopId":shopid,
                "shopState":"2",
                "isDisable":"t",
                "isDeleted":"f",
                "isSpecialFlag":"f"
            }]
            data1.append(b64encode(bytes(json.dumps(dataValue[0], separators=(',', ':')), 'utf-8')).decode('utf-8'))

        for song in songs:
            song_data = json.loads(song["data"])
            songCode = []

            songCode.append({
                    "mcode": song_data['mcode'],
                    "musicState": song_data['musicState'],
                    "playCount": song_data['playCount'],
                    "totalScore": song_data['totalScore'],
                    "highScore": song_data['highScore'],
                    "everHighScore": song_data['everHighScore'] if 'everHighScore' in song_data else ["0","0","0","0","0"],
                    "clearRate": song_data['clearRate'],
                    "rankPoint": song_data['rankPoint'],
                    "normalCR": song_data['normalCR'] if 'normalCR' in song_data else ["0","0","0","0","0"],
                    "survivalCR": song_data['survivalCR'] if 'survivalCR' in song_data else ["0","0","0","0","0"],
                    "ultimateCR": song_data['ultimateCR'] if 'ultimateCR' in song_data else ["0","0","0","0","0"],
                    "nohopeCR": song_data['nohopeCR'] if 'nohopeCR' in song_data else ["0","0","0","0","0"],
                    "combo": song_data['combo'],
                    "coupleUserId": song_data['coupleUserId'],
                    "difficulty": song_data['difficulty'],
                    "isFullCombo": song_data['isFullCombo'],
                    "clearGaugeType": song_data['clearGaugeType'],
                    "fieldType": song_data['fieldType'],
                    "gameType": song_data['gameType'],
                    "grade": song_data['grade'],
                    "unlockState": song_data['unlockState'],
                    "extraState": song_data['extraState']
                })
            index.append(song_data['index'])
            data1.append(b64encode(bytes(json.dumps(songCode[0], separators=(',', ':')), 'utf-8')).decode('utf-8'))

        for v in index:
            profile_version = versionindex.append(profile_data["version"])

        return({"index":index, "data":data1, "version":versionindex})

    def handle_action_saveindex_request(self, data: Dict) -> Dict:
        save_data = data['saveindex']
        
        try:
            #REV Omnimix Version Fetcher
            gameversion = data['saveindex']['data'][0][2]
            self.logger.warning(f"Game Version is {gameversion}")
        except:
            pass
            
        if "10205" in gameversion:
            self.logger.warning(f"Switching to CrossBeats REV SaveIndex")
            #Alright.... time to bring the jank code
            
            dataList = []
            indexList = []
            rev_aimeId = []
            
            for value in data['saveindex']['data']:
                if 'playedUserId' in value[1]:
                    indexList.append(value[0])
                    dataList.append(value[1])
                if 'mcode' not in value[1]:
                    if "aimeId" in value[1]:
                        user_json = json.loads(value[1])
                        rev_aimeId.append(user_json["aimeId"])
                    indexList.append(value[0])
                    dataList.append(value[1])
                if 'shopId' in value:
                    continue
                if 'mcode' in value[1] and 'musicState' in value[1]:
                    song_json = json.loads(value[1])
                    
                    songCode = []
                    songCode.append({
                        "mcode": song_json['mcode'],
                        "musicState": song_json['musicState'],
                        "playCount": song_json['playCount'],
                        "totalScore": song_json['totalScore'],
                        "highScore": song_json['highScore'],
                        "clearRate": song_json['clearRate'],
                        "rankPoint": song_json['rankPoint'],
                        "combo": song_json['combo'],
                        "coupleUserId": song_json['coupleUserId'],
                        "difficulty": song_json['difficulty'],
                        "isFullCombo": song_json['isFullCombo'],
                        "clearGaugeType": song_json['clearGaugeType'],
                        "fieldType": song_json['fieldType'],
                        "gameType": song_json['gameType'],
                        "grade": song_json['grade'],
                        "unlockState": song_json['unlockState'],
                        "extraState": song_json['extraState'],
                        "index": value[0]
                    })
                    
                    self.data.game.put_best_score(rev_aimeId, self.game, self.version, song_json['mcode'], value[0], 0, 0, 0, 0, 0, 0, songCode[0])
            
            fullList = []
            i = 0
            
            fullList.append({
                "uid": data["saveindex"]["uid"], 
                "index": indexList,
                "data": dataList,
                "version": 10205
                })
                
            self.logger.warning(f"{fullList}")
            
            # Put user profile is now somewhat fixed
            self.data.game.put_profile(user_id=int(rev_aimeId[0]), game=self.game, version=self.version, game_id=data["saveindex"]["uid"], data=fullList[0])
            return({})
        else:
            self.logger.warning(f"Switching to REV Sunrise SaveIndex")

        #Sunrise
        try:
            profileIndex = save_data['index'].index('0')
        except:
            return({"data":""}) #Maybe

        profile = json.loads(save_data["data"][profileIndex])
        aimeId = profile["aimeId"]

        fullList = []
        dataList = []
        i = 0

        for index, value in enumerate(data["saveindex"]["data"]):
            if 'playedUserId' in value:
                dataList.append(value)
            if 'mcode' not in value and "normalCR" not in value:
                dataList.append(value)
            if 'shopId' in value:
                continue
        
        fullList.append({
            "uid": data["saveindex"]["uid"], 
            "index": data["saveindex"]["index"],
            "data": dataList,
            "version": 10400
            })

        # MusicList Index for the profile
        indexSongList = []
        for value in data["saveindex"]["index"]:
            if int(value) in range(100000,110000):
                indexSongList.append(value)
        
        # Put user profile is now fixed
        self.data.game.put_profile(user_id=aimeId, game=self.game, version=self.version, game_id=data["saveindex"]["uid"], data=fullList[0])
        
        for index, value in enumerate(data["saveindex"]["data"]):
            if 'mcode' not in value:
                continue
            if 'playedUserId' in value:
                continue
            
            data1 = json.loads(value)

            songCode = []
            songCode.append({
                "mcode": data1['mcode'],
                "musicState": data1['musicState'],
                "playCount": data1['playCount'],
                "totalScore": data1['totalScore'],
                "highScore": data1['highScore'],
                "everHighScore": data1['everHighScore'],
                "clearRate": data1['clearRate'],
                "rankPoint": data1['rankPoint'],
                "normalCR": data1['normalCR'],
                "survivalCR": data1['survivalCR'],
                "ultimateCR": data1['ultimateCR'],
                "nohopeCR": data1['nohopeCR'],
                "combo": data1['combo'],
                "coupleUserId": data1['coupleUserId'],
                "difficulty": data1['difficulty'],
                "isFullCombo": data1['isFullCombo'],
                "clearGaugeType": data1['clearGaugeType'],
                "fieldType": data1['fieldType'],
                "gameType": data1['gameType'],
                "grade": data1['grade'],
                "unlockState": data1['unlockState'],
                "extraState": data1['extraState'],
                "index": indexSongList[i]
            })

            self.data.game.put_best_score(aimeId, self.game, self.version, data1['mcode'], indexSongList[i], 0, 0, 0, 0, 0, 0, songCode[0])
            i += 1
        return({})
        
    def handle_action_sprankreq_request(self, data: Dict) -> Dict:
        uid = data['sprankreq']['uid']
        extId = self.data.game.game_id_to_user_id(uid, self.game, self.version)
        
        p = self.data.game.get_items(user_id = extId, game = self.game, version = self.version, item_type=2)

        rankList: list[Dict[str, Any]] = []

        for i, value in enumerate(p):
            rankList.append(json.loads(value["data"]))

        return({
            "uid": data["sprankreq"]["uid"],
            "aid": data["sprankreq"]["aid"],
            "rank": rankList ,
            "rankx":[1,1,1]
        })
    
    def handle_action_getadv_request(self, data: Dict) -> Dict:
        return({"data":[{"r":"1","i":"100300","c":"20"}]})
        
    def handle_action_getmsg_request(self, data: Dict) -> Dict:
        return({"msgs":[]})
    
    def handle_auth_logout_request(self, data: Dict) -> Dict:
        return({"auth":True})
     
    def handle_action_rankreg_request(self, data: Dict) -> Dict:
        uid = data['rankreg']['uid']
        extId = self.data.game.game_id_to_user_id(uid, self.game, self.version)

        for rid in data['rankreg']['data']:
            self.data.game.put_item(extId, self.game, self.version, 2, rid["rid"], rid)
        return({})
        
    def handle_action_addenergy_request(self, data: Dict) -> Dict:
        uid = data['addenergy']['uid']
        extId = self.data.game.game_id_to_user_id(uid, self.game, self.version)
        profile = self.data.game.get_profile(self.game, self.version, user_id=extId)
        profile_data = json.loads(profile["data"])

        data1 = json.loads(profile_data["data"][3])

        p = self.data.game.get_items(extId, self.game, self.version, item_type=3)
            
        if not p: 
            itemList = [{"total": 5}]
            self.data.game.put_item(extId, self.game, self.version, 3, 101, itemList[0])
            
            return({
                "class": data1["myClass"],
                "granted": "5",
                "total": "5",
                "threshold": "1000"
            })
        
        array = []
        for item in p:
            data0 = json.loads(item["data"])
            energy = data0["total"]

            newenergy = energy + 5
            itemList = [{"total": newenergy}]
            self.data.game.put_item(extId, self.game, self.version, 3, 101, itemList[0])

            if int(energy) <= 995:
                array.append({
                    "class": data1["myClass"],
                    "granted": "5",
                    "total": str(energy),
                    "threshold": "1000"
                })
            else:
                array.append({
                    "class": data1["myClass"],
                    "granted": "0",
                    "total": str(energy),
                    "threshold": "1000"
                })
        return array[0]
