from typing import Any, List, Dict
import logging
import json

from datetime import datetime, timedelta
import pytz

from aime.data import Data, Config
from aime.titles.wacca.config import WaccaConfig
from aime.titles.wacca.const import WaccaConstants

class WaccaBase():
    ITEM_TYPES = {
        "xp": 1,
        "wp": 2,
        "music_unlock": 3,
        "music_difficulty_unlock": 4,
        "title": 5,
        "icon": 6,
        "trophy": 7,
        "skill": 8,
        "ticket": 9,
        "note_color": 10,
        "note_sound": 11,
        "baht_do_not_send": 12,
        "boost_badge": 13,
        "gate_point": 14,
        "navigator": 15,
        "user_plate": 16,
    }
    
    OPTIONS = {
        "note_speed": 1, # 1.0 - 6.0
        "field_mask": 2, # 0-4
        "note_sound": 3, # ID
        "note_color": 4, # ID
        "bgm_volume": 5, # 0-100 incremements of 10
        "bg_video": 7, # ask, on, or off

        "mirror": 101, # none or left+right swap
        "judge_display_pos": 102, # center, under, over, top or off
        "judge_detail_display": 103, # on or off
        "measure_guidelines": 105, # on or off
        "guideline_mask": 106, # 0 - 5
        "judge_line_timing_adjust": 108, # -10 - 10
        "note_design": 110, # 1 - 5
        "bonus_effect": 114, # on or off
        "chara_voice": 115, # "usually" or none
        "score_display_method": 116, # add or subtract
        "give_up": 117, # off, no touch, can't achieve s, ss, sss, pb
        "guideline_spacing": 118, # none, or a-g type
        "center_display": 119, # none, combo, score add, score sub, s ss sss pb boarder
        "ranking_display": 120, # on or off
        "stage_up_icon_display": 121, # on or off
        "rating_display": 122, # on or off
        "player_level_display": 123, # on or off
        "touch_effect": 124, # on or off
        "guide_sound_vol": 125, # 0-100 incremements of 10
        "touch_note_vol": 126, # 0-100 incremements of 10
        "hold_note_vol": 127, # 0-100 incremements of 10
        "slide_note_vol": 128, # 0-100 incremements of 10
        "snap_note_vol": 129, # 0-100 incremements of 10
        "chain_note_vol": 130, # 0-100 incremements of 10
        "bonus_note_vol": 131, # 0-100 incremements of 10
        "gate_skip": 132, # on or off
        "key_beam_display": 133, # on or off

        "left_slide_note_color": 201, # red blue green or orange
        "right_slide_note_color": 202, # red blue green or orange
        "forward_slide_note_color": 203, # red blue green or orange
        "back_slide_note_color": 204, # red blue green or orange

        "master_vol": 1001, # 0-100 incremements of 10
        "set_title_id": 1002, # ID
        "set_icon_id": 1003, # ID
        "set_nav_id": 1004, # ID
        "set_plate_id": 1005, # ID
    }
    def __init__(self, cfg: Config, game_cfg: WaccaConfig) -> None:
        self.config = cfg # Config file
        self.game_config = game_cfg # Game Config file
        self.game = WaccaConstants.GAME_CODE # Game code
        self.version = WaccaConstants.VER_WACCA # Game version
        self.data = Data(cfg) # Database
        self.logger = logging.getLogger("title") # Title logger
        self.srvtime = datetime.now()
        self.season = 1
    
    def handle_housing_get_request(self, data: Dict) -> List[Any]:
        # TODO: Store this in the machine table's data column
        return [1337, 0]

    def handle_housing_start_request(self, data: Dict) -> List[Any]:
        return [
            1, # Region ID
            [ # "favorite songs", probably attract role
                1269,1007,1270,1002,1020,1003,1008,1211,1018,1092,1056,32,
                1260,1230,1258,1251,2212,1264,1125,1037,2001,1272,1126,1119,
                1104,1070,1047,1044,1027,1004,1001,24,2068,2062,2021,1275,
                1249,1207,1203,1107,1021,1009,9,4,3,23,22,2014,13,1276,1247,
                1240,1237,1128,1114,1110,1109,1102,1045,1043,1036,1035,1030,
                1023,1015
            ]
        ]
    
    def handle_advertise_GetNews_request(self, data: Dict) -> List[Any]:
        return [
            # Notice name, title, message, something, something, show on title screen, welcome screen, start time, end time, voice?
            [], # Notices
            [], # Coppyright listings
            [], # Stopped song IDs
            [], # Stopped jacket IDs
            [], # Stopped movie IDs
            [], # Stopped icon IDs
        ]

    def handle_user_status_logout_request(self, data: Dict) -> List[Any]:
        return []

    def handle_user_status_login_request(self, data: Dict) -> List[Any]:
        game_id = data["params"][0]        
        first_login_daily = 0
        last_login_time = 0

        profile = self.data.game.get_profile(self.game, self.version, game_id=game_id)
        if profile is not None: # This is to account for guest play
            user_id = profile["user"]
            pdata = json.loads(profile["data"])

            pdata["profile"]["logins_today"] += 1
            pdata["profile"]["last_game_ver"] = data["appVersion"]

            last_login_time = int(pdata["profile"]["last_login_timestamp"])
            
            # If somebodies login timestamp < midnight of current day, then they are logging in for the first time today
            if pdata["profile"]["last_login_timestamp"] < int(datetime.now().replace(hour=0,minute=0,second=0,microsecond=0).timestamp()):
                first_login_daily = 1
                pdata["profile"]["login_days"] += 1
                pdata["profile"]["login_consec_days"] += 1
                pdata["profile"]["logins_today"] = 1

            # If somebodies login timestamp > midnight of current day + 1 day, then they broke their daily login streak
            elif pdata["profile"]["last_login_timestamp"] > int((datetime.now().replace(hour=0,minute=0,second=0,microsecond=0) + timedelta(days=1)).timestamp()):
                pdata["profile"]["login_consec_days"] = 1        
            # else, they are simply logging in again on the same day, and we don't need to do anything for that
            
            # After logging in, there will always be at least 1 consecutive login. This is to ensure that fact.
            if pdata["profile"]["login_consec"] == 0:
                pdata["profile"]["login_consec"] = 1

            pdata["profile"]["last_login_timestamp"] =  int(datetime.now().timestamp())
            self.data.game.put_profile(user_id, self.game, self.version, data=pdata)

        return [ # TODO: Login bonus
            # user ticket id, ticket id, expiration date | item type, item id, item quantity | message
            #[[[15, 106002, int(self.srvtime.timestamp())]], [[0,0, 1]], "a"],
            [
                [[[15, 106001, int(self.srvtime.timestamp())]], [], ""]
            ], # Daily login bonus info
            [], # Consecutive login bonus info
            [], # Other login bonus info
            first_login_daily, # First login of the day flag
        ]

    def handle_user_status_get_request(self, data: Dict) -> List[Any]:
        aime_id = data["params"][0]
        profile = self.data.game.get_profile(self.game, self.version, user_id=aime_id)
        if profile is None:
            return [[], 0, 0, 1, [0, ""]]
        
        pdata = json.loads(profile["data"])
        mods = json.loads(profile["mods"])

        # Not writing this back to database is fine because it's getting changed next request anyway
        # if the user doesn't login then it doesn't matter anyway 
        if pdata["profile"]["last_login_timestamp"] < int(datetime.now().replace(hour=0,minute=0,second=0,microsecond=0).timestamp()):
            pdata["profile"]["logins_today"] = 0
        
        if not profile["name"]:
            username = pdata["profile"]["username"]
        else: 
            username = profile["name"]

        ver_status = 0
        ver_split = data["appVersion"].split(".")
        lpv_split = pdata["profile"]["last_game_ver"].split(".")
        
        # If an omnimix ever comes out for LilyR we'll need to find a way to not send omnimix songs
        # TODO: More nuance here
        if int(lpv_split[0]) < int(ver_split[0]) or int(lpv_split[1]) < int(ver_split[1]):
            ver_status = 2
        elif int(lpv_split[0]) > int(ver_split[0]) or int(lpv_split[1]) > int(ver_split[1]):
            ver_status = 1
        
        vip_expire_time = 0

        if "vip_expire_time" in pdata["profile"]:
            vip_expire_time = pdata["profile"]["vip_expire_time"]

        if "always_vip" in mods and mods["always_vip"] or self.game_config.always_vip:
            vip_expire_time = int((self.srvtime + timedelta(days=30)).timestamp())

        return [
            [
                profile["game_id"], # User ID
                username, # Username
                1, # User type
                pdata["profile"]["xp"], # XP
                pdata["profile"]["dan_level"], # Dan Level
                pdata["profile"]["dan_type"], # Dan type
                pdata["profile"]["wp"], # WP
                pdata["profile"]["title_part_ids"],
                profile["use_count"], # Total logins
                pdata["profile"]["login_days"], # Number of days logged in
                pdata["profile"]["login_consec"], # Consecutive logins
                pdata["profile"]["login_consec_days"], # Consecutive login days
                vip_expire_time, #pdata["profile"]["vip_end"], # VIP end time
            ],
            pdata["option"]["set_title_id"], # Title ID?
            pdata["option"]["set_icon_id"], # Icon ID?
            0, # profile status, 0 good, 1 register, 2 in use, 3 is regionlock, 4 and above softlocks
            [ # Version verification
                ver_status, # verification status, 1 is data too new, 2 is upgrade, anything else is good
                pdata["profile"]["last_game_ver"]
            ]
        ]
    
    def handle_user_status_create_request(self, data: Dict) -> List[Any]:
        user_id = int(data["params"][0])
        username = data["params"][1]
        game_id = self.data.base.generate_id()

        profileid = self.data.game.put_profile(user_id, self.game, self.version, game_id=game_id, name=username, mods={}, 
        data={
            "profile": {
                "xp": 0,
                "dan_level": 0,
                "dan_type": 0,
                "title_part_ids": [
                    0,
                    0,
                    0
                ],
                "rating": 0,
                "wp": 0,
                "total_wp_gained": 0,
                "logins_today": 1,
                "login_days": 1,
                "login_consec": 1,
                "login_consec_days": 1,
                "last_login_timestamp": int(self.srvtime.timestamp()),
                "last_game_ver": data["appVersion"],
                "play_counts": [0,0,0]
            },
            "option": {
                "note_speed": 5,
                "field_mask": 0,
                "note_sound": 105001,
                "note_color": 203001,
                "bgm_volume": 10,
                "bg_video": 0,
                "mirror": 0,
                "judge_display_pos": 0,
                "judge_detail_display": 0,
                "measure_guidelines": 1,
                "guideline_mask": 1,
                "judge_line_timing_adjust": 10,
                "note_design": 3,
                "bonus_effect": 1,
                "chara_voice": 1,
                "score_display_method": 0,
                "give_up": 0,
                "guideline_spacing": 1,
                "center_display": 1,
                "ranking_display": 1,
                "stage_up_icon_display": 1,
                "rating_display": 1,
                "player_level_display": 1,
                "touch_effect": 1,
                "guide_sound_vol": 3,
                "touch_note_vol": 8,
                "hold_note_vol": 8,
                "slide_note_vol": 8,
                "snap_note_vol": 8,
                "chain_note_vol": 8,
                "bonus_note_vol": 8,
                "gate_skip": 0,
                "key_beam_display": 1,
                "left_slide_note_color": 4,
                "right_slide_note_color": 3,
                "forward_slide_note_color": 1,
                "back_slide_note_color": 2,
                "master_vol": 3,
                "set_title_id": 104001,
                "set_icon_id": 102001,
                "set_nav_id": 210002,
                "set_plate_id": 211001
            }
        })

        if profileid is None: return []

        # Insert starting items
        self.data.game.put_item(user_id, self.game, self.version, self.ITEM_TYPES["title"], 104001, 
        {"obtainedDate": int(self.srvtime.timestamp())})
        self.data.game.put_item(user_id, self.game, self.version, self.ITEM_TYPES["title"], 104002, 
        {"obtainedDate": int(self.srvtime.timestamp())})
        self.data.game.put_item(user_id, self.game, self.version, self.ITEM_TYPES["title"], 104003, 
        {"obtainedDate": int(self.srvtime.timestamp())})
        self.data.game.put_item(user_id, self.game, self.version, self.ITEM_TYPES["title"], 104005, 
        {"obtainedDate": int(self.srvtime.timestamp())})
        
        self.data.game.put_item(user_id, self.game, self.version, self.ITEM_TYPES["icon"], 102001, 
        {"obtainedDate": int(self.srvtime.timestamp()), "uses": 0})
        self.data.game.put_item(user_id, self.game, self.version, self.ITEM_TYPES["icon"], 102002, 
        {"obtainedDate": int(self.srvtime.timestamp()), "uses": 0})
        
        self.data.game.put_item(user_id, self.game, self.version, self.ITEM_TYPES["note_color"], 103001, 
        {"obtainedDate": int(self.srvtime.timestamp())})
        self.data.game.put_item(user_id, self.game, self.version, self.ITEM_TYPES["note_color"], 203001, 
        {"obtainedDate": int(self.srvtime.timestamp())})
        
        self.data.game.put_item(user_id, self.game, self.version, self.ITEM_TYPES["note_sound"], 105001, 
        {"obtainedDate": int(self.srvtime.timestamp())})
        self.data.game.put_item(user_id, self.game, self.version, self.ITEM_TYPES["note_sound"], 105005, 
        {"obtainedDate": int(self.srvtime.timestamp())})
        
        self.data.game.put_item(user_id, self.game, self.version, self.ITEM_TYPES["navigator"], 210001, 
        {"obtainedDate": int(self.srvtime.timestamp()), "uses": 0, "season_uses": 0})

        self.data.game.put_item(user_id, self.game, self.version, self.ITEM_TYPES["user_plate"], 211001, 
        {"obtainedDate": int(self.srvtime.timestamp())})
        
        return [
            [
                game_id, # User ID
                username, # Username
                1, # User type
                0, # XP
                0, # Dan Level
                0, # Dan type
                0, # WP
                [ # Title part IDs??
                    0,
                    0,
                    0
                ],
                0, # Total logins
                0, # Number of days logged in
                0, # Consecutive logins
                0, # Consecutive login days
                0, # VIP end time
            ],
        ]

    def handle_user_status_getDetail_request(self, data: Dict) -> List[Any]:
        game_id = data["params"][0]
        profile = self.data.game.get_profile(self.game, self.version, game_id=game_id)
        if profile is None: return []
        user_id = profile["user"]
        pdata = json.loads(profile["data"])
        mods = json.loads(profile["mods"])
        songs = self.data.game.get_best_scores(profile["user"], self.game)

        if not profile["name"]:
            username = pdata["profile"]["username"]
        else: 
            username = profile["name"]

        vip_expire_time = 0
        song_update_time = 0
        last_song_info = [0,0,0,0,0]
        song_play_status = [0,0]
        cumulative_score = 0 # This would be pretty resource-intensive to calculate...
        total_gate_pt = 0
        friends_list = []
        options = []
        scores = []
        gates = []
        song_unlocks = []
        titles = []
        icons = []
        trophies = []
        tickets = []
        note_colors = []
        note_sounds = []
        navigators = []
        plates = []

        if "vip_expire_time" in pdata["profile"]:
            vip_expire_time = pdata["profile"]["vip_expire_time"]

        if "always_vip" in mods and mods["always_vip"] or self.game_config.always_vip:
            vip_expire_time = int((self.srvtime + timedelta(days=31)).timestamp())

        if "song update_time" in pdata["profile"]:
            song_update_time = pdata["profile"]["song update_time"]

        if "last_song_info" in pdata["profile"]:
            last_song_info = pdata["profile"]["last_song_info"]
            song_play_status = [pdata["profile"]["last_song_info"][0], 1]
        
        if "friends" in pdata and pdata["friends"]:
            for friend in pdata["friends"]:
                friend_profile = self.data.game.get_profile(self.game, self.version, game_id=friend)                
                if friend_profile is None:
                    self.logger.warn(f"No profile found for friend's game_id {friend} in handle_user_status_getDetail_request", extra={"game": "WaccaLilyR"})
                    continue
                
                friend_info = [friend, friend_profile["username"], 1, []]
                friend_user_id = friend_profile["user"]
                friend_scores = self.data.game.get_best_scores(friend_user_id, self.game)

                for score in friend_scores:
                    friend_info[3].append([score[4], score[5], score[6]])
                
                friends_list.append(friend_info)
        
        for k,v in self.OPTIONS.items():
            options.append([v, pdata["option"][k]])

        for song in songs:
            if self.game_config.safe_song_load:
                game_song_info = self.data.static.get_game_music(self.game, self.version, int(song["song_id"]), song["chart_id"])
            else:
                game_song_info = []

            if game_song_info or not self.game_config.safe_song_load:
                sdata = json.loads(song["data"])
                scores.append([int(song["song_id"]), song["chart_id"], self.util_int_to_bitmask_array(song["fc1"], 5), 
                self.util_int_to_bitmask_array(song["fc1"], 5), self.util_int_to_bitmask_array(song["grade"], 10),
                song["score1"], sdata["max_combo"], 0, 1, sdata["rating"]])
        
        user_items = []
        for x in range(self.version + 1):
            user_items += self.data.game.get_items(user_id, self.game, version = x)
        if user_items:
            for item in user_items:
                try:
                    item_data = json.loads(item[6])
                    if item[4] == self.ITEM_TYPES["music_difficulty_unlock"] or item[4] == self.ITEM_TYPES["music_unlock"]:
                        pass
                        for x in range(0, 4):
                            if item_data["difficulty"][x] == 1:
                                # id, difficulty, apperance date, unlock date
                                song_unlocks.append([item[5], x + 1, 0, 
                                item_data["obtainedDate"]])

                    elif item[4] == self.ITEM_TYPES["title"]:
                        titles.append([item[5], 1, item_data["obtainedDate"]])

                    elif item[4] == self.ITEM_TYPES["icon"]:
                        if "uses" in item_data:
                            use_ct = item_data["uses"]
                        else:
                            use_ct = 0
                        icons.append([item[5], 1, use_ct, item_data["obtainedDate"]])

                    elif item[4] == self.ITEM_TYPES["trophy"]:
                        if "progress" in item_data:
                            progress = item_data["progress"]
                        else:
                            progress = 0
                        trophies.append([item[5], 0, progress, 0])

                    elif item[4] == self.ITEM_TYPES["ticket"]:
                        if "quantity" in item_data:
                            for x in range(item_data["quantity"]):
                                tickets.append([x, item["item_id"], int((self.srvtime + timedelta(days=30)).timestamp())])
                        else:
                            tickets.append([1, item["item_id"], int((self.srvtime + timedelta(days=30)).timestamp())])

                    elif item[4] == self.ITEM_TYPES["note_color"]:
                        note_colors.append([item[5], 1, item_data["obtainedDate"]])

                    elif item[4] == self.ITEM_TYPES["note_sound"]:
                        note_sounds.append([item[5], 1, item_data["obtainedDate"]])

                    elif item[4] == self.ITEM_TYPES["navigator"]:
                        if "uses" in item_data:
                            use_ct = item_data["uses"]
                        else:
                            use_ct = 0
                        if "season_uses" in item_data:
                            season_use_ct = item_data["season_uses"]
                        else:
                            season_use_ct = 0
                        navigators.append([item[5], 1, item_data["obtainedDate"], use_ct, season_use_ct])

                    elif item[4] == self.ITEM_TYPES["user_plate"]:
                        plates.append([item[5], 1, item_data["obtainedDate"]])

                except:
                    self.logger.error(f"Failed to load item {item['item_id']} for user {user_id}", extra={"game": "WaccaLilyR"})

        return [
            [
                profile["game_id"], # User ID
                username, # Username
                1, # User type?
                pdata["profile"]["xp"], # XP
                pdata["profile"]["dan_level"], # Dan level
                pdata["profile"]["dan_type"], # Dan type
                pdata["profile"]["wp"], # Lily Point
                pdata["profile"]["title_part_ids"],
                profile["use_count"], # Total logins
                pdata["profile"]["login_days"], # Number of days logged in
                pdata["profile"]["login_consec"], # Consecutive logins
                pdata["profile"]["login_consec_days"], # Consecutive login days
                vip_expire_time, # VIP end time
            ], # see user status get above
            options, # Options, includes customization
            # play mode info [season id, mode id, number of plays]
            [[2, 0, pdata["profile"]["play_counts"][0]], [2, 1, pdata["profile"]["play_counts"][1]], [2, 2, pdata["profile"]["play_counts"][2]]], 
            [ # Item info
                song_unlocks, # Song unlocks [songid, difficulty, apperiance date, unlock date]
                titles, # Titles [id, type, aquired]
                icons, # Icons [id, type, uses, aquired date]
                trophies, # Trophies
                [], # Skill info? [type, level, flag, badge]
                tickets, # Tickets [4876,106001,1642204085] is expert unlock [user ticket id, ticket id, expiration date]
                note_colors, # Note colors [id, type, aquired]
                note_sounds, # Note sounds [id, type, aquired]
                navigators, # Navs [id, type, aquired, uses, uses today]
                #plates  # Plates [id, type, aquired]
            ],
            scores, # [played, cleared, missless, fc, am] [same but this season only] [d, c, b, a, aa, aaa, s, ss, sss, master], 
            song_play_status, # Song play status?
            # [level, wp obtained, wp spend, cumulative score, # titles, # icons, # skill points, # colors, # input sounds, # plates, # gate points]
            [pdata["profile"]["xp"],pdata["profile"]["total_wp_gained"],0,cumulative_score,len(titles),len(icons),0,len(note_colors),len(note_sounds),len(plates),total_gate_pt], # TODO: Season info
            [ [0],[0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0],[0,0,0,0],[0,0,0,0,0,0,0],[0] ], # Play area info
            song_update_time, # Song list inquiry time?
            #[] if "favorite" not in pdata else pdata["favorite"],
            #[], # Stopped song IDs?
            #[], # Event info
            #gates, # gates
            #last_song_info,
            #[ [1,1],[2,1],[3,1],[4,1],[5,1] ], # TODO: Gate tutorial flags, 1 - 5
            #[], # Gacha info id, # pulls (not supported)
            #friends_list#friends_list# TODO: Friend info ID, Username, user type?, songlist consisting of songid, difficulty, and score
        ]

    # Thanks mon!
    def util_int_to_bitmask_array(self, num: int, length: int) -> List[int]:
        return [(num >> i) & 1 for i in range(length)]

    def util_bitmask_array_to_int(self, bitmask: List[int]) -> int:
        return sum(bit << i for i, bit in enumerate(bitmask))

    def util_put_items(self, user_id: int, profile_data: Dict, items_obtained: List[List[int]]) -> Dict:
        if items_obtained:
            for item in items_obtained:
                
                if item[0] == self.ITEM_TYPES["xp"]:
                    profile_data["profile"]["xp"] += item[2]

                elif item[0] == self.ITEM_TYPES["wp"]:
                    profile_data["profile"]["wp"] += item[2]
                    profile_data["profile"]["total_wp_gained"] += item[2]
                
                elif item[0] == self.ITEM_TYPES["music_difficulty_unlock"] or item[0] == self.ITEM_TYPES["music_unlock"]:
                    old_unlock = self.data.game.get_items(user_id, self.game, self.version, self.ITEM_TYPES["music_difficulty_unlock"])
                    difficulty = [0,0,0,0]

                    for unlock in old_unlock:
                        if unlock[5] == item[1]:
                            idata = json.loads(unlock[6])
                            difficulty = idata["difficulty"]
                            break
                    
                    difficulty[item[2] - 1] = 1

                    song_difficulty_unlock_data = {
                        "obtainedDate": int(self.srvtime.timestamp()),
                        "difficulty": difficulty
                    }

                    self.data.game.put_item(user_id, self.game, self.version, item[0], item[1], song_difficulty_unlock_data)

                    if item[2] > 2:
                        old_score = self.data.game.get_best_scores(user_id, self.game, item[1], item[2])
                        if not old_score:
                            self.data.game.put_best_score(user_id, self.game, self.version, item[1], item[2], 0, 0, 0, 0, 0, 0, {
                                "lowest_miss_count": 0,
                                "rating": 0,
                                "play_count": 0,
                                "max_combo": 0
                            })

                elif item[0] == self.ITEM_TYPES["ticket"]: # Treat tickets as non-unique with infinite expire time for now...
                    old_ticket = self.data.game.get_items(user_id, self.game, item_type=item[0], item_id=item[1])
                    if old_ticket:
                        ticket_data = json.loads(old_ticket[0]["data"])
                        ticket_data["quantity"] += 1
                    else:
                        ticket_data = {"quantity": 1}
                    
                    self.data.game.put_item(user_id, self.game, self.version, item[0], item[1], ticket_data)

                elif item[0] == self.ITEM_TYPES["boost_badge"]: # Don't save boosts
                    pass
                    
                elif item[0] == self.ITEM_TYPES["icon"]:
                    self.data.game.put_item(user_id, self.game, self.version, item[0], item[1], 
                    {"obtainedDate": int(self.srvtime.timestamp()), "uses": 0})

                elif item[0] == self.ITEM_TYPES["navigator"]:
                    self.data.game.put_item(user_id, self.game, self.version, item[0], item[1], 
                    {"obtainedDate": int(self.srvtime.timestamp()), "uses": 0, "season_uses": 0 })

                elif item[0] == self.ITEM_TYPES["trophy"]:
                    self.data.game.put_item(user_id, self.game, self.version, item[0], item[1], 
                    {"updatedDate": int(self.srvtime.timestamp()), "progress": item[2]})

                else:
                    self.data.game.put_item(user_id, self.game, self.version, item[0], item[1], {"obtainedDate": int(self.srvtime.timestamp())})
        
        return profile_data
