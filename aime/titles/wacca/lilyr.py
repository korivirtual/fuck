from typing import Any, List, Dict
from datetime import datetime, timedelta
import json

from aime.data import Config
from aime.titles.wacca.base import WaccaBase
from aime.titles.wacca.config import WaccaConfig
from aime.titles.wacca.const import WaccaConstants

class WaccaLilyR(WaccaBase):
    def __init__(self, cfg: Config, game_cfg: WaccaConfig) -> None:
        super().__init__(cfg, game_cfg)
        self.version = WaccaConstants.VER_WACCA_LILY_R
        self.season = 2
        
    def handle_advertise_GetNews_request(self, data: Dict) -> List[Any]:
        return [
            # Notice name, title, message, something, something, show on title screen, welcome screen, start time, end time, voice?
            [], # Notices
            [], # Coppyright listings
            [], # Stopped song IDs
            [], # Stopped jacket IDs
            [], # Stopped movie IDs
            [], # Stopped icon IDs
            [], # Stopped product IDs
            [], # Stopped navigator IDs
            []  # Stopped navigator voice IDs
        ]
    
    def handle_user_status_get_request(self, data: Dict) -> List[Any]:
        aime_id = data["params"][0]
        profile = self.data.game.get_profile(self.game, self.version, user_id=aime_id)
        if profile is None:
            profile = self.data.game.get_profile(self.game, self.version - 1, user_id=aime_id)
            if profile is None:
                return [[],0,0,1,[1,""],[]]
        
        pdata = json.loads(profile["data"])
        mods = json.loads(profile["mods"])

        if not profile["name"]:
            username = pdata["profile"]["username"]
        else: 
            username = profile["name"]

        # Not writing this back to database is fine because it's getting changed next request anyway
        # if the user doesn't login then it doesn't matter anyway 
        if pdata["profile"]["last_login_timestamp"] < int(datetime.now().replace(hour=0,minute=0,second=0,microsecond=0).timestamp()):
            pdata["profile"]["logins_today"] = 0

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

        if self.game_config.always_vip:
                vip_expire_time = int((self.srvtime + timedelta(days=30)).timestamp())
        elif "vip_expire_time" in pdata["profile"]:
                vip_expire_time = pdata["profile"]["vip_expire_time"]

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
                pdata["profile"]["logins_today"], # Logins today
                pdata["profile"]["rating"] # Rating
            ],
            pdata["option"]["set_title_id"], # Title ID?
            pdata["option"]["set_icon_id"], # Icon ID?
            0, # profile status, 0 good, 1 register, 2 in use, 3 is regionlock, 4 and above softlocks
            [ # Version verification
                ver_status, # verification status, 1 is data too new, 2 is upgrade, anything else is good
                pdata["profile"]["last_game_ver"]
            ],
            [# Unknown, needs to be blank
                
            ]
        ]

    def handle_user_status_login_request(self, data: Dict) -> List[Any]:
        game_id = data["params"][0]        
        first_login_daily = 0
        last_login_time = 0

        profile = self.data.game.get_profile(self.game, self.version, game_id=game_id)
        if profile is None:
            profile = self.data.game.get_profile(self.game, self.version - 1, game_id=game_id)
        if profile is not None: # This is to account for guest play
            user_id = profile["user"]
            pdata = json.loads(profile["data"])
            ver_split = data["appVersion"].split(".")

            pdata["profile"]["logins_today"] += 1
            pdata["profile"]["last_game_ver"] = f"{ver_split[0]}.{ver_split[1]}.{ver_split[2]}"

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
            self.data.game.put_profile(user_id, self.game, self.version, data=pdata, game_id=game_id)

        return [ # TODO: Login bonus
            # user ticket id, ticket id, expiration date | item type, item id, item quantity | message
            #[[[15, 106002, int(self.srvtime.timestamp())]], [[0,0, 1]], "a"],
            [[[[15, 106001, int(self.srvtime.timestamp())]], [], ""]] if first_login_daily == 1 else [], # Daily login bonus info
            [], # Consecutive login bonus info
            [], # Other login bonus info
            first_login_daily, # First login of the day flag
            [ # VIP page info: year, month, day
                (self.srvtime).year,
                (self.srvtime).month,
                (self.srvtime).day,
                1, # number of items we're on
                [
                    #[[], [], ""]
                ], # Present information, needs to be here for daily vip bonus to show
                [                    
                    [1,0,[2,1,1000]],
                    [2,0,[13,209001,1]],
                    [3,0,[13,209002,1]],
                    [4,0,[9,106002,1]],
                    [5,0,[1,1,50]],
                    [6,0,[13,209003,1]],
                    [7,0,[9,206001,1]],
                    [8,0,[9,206002,1]],
                ]  # VIP login bonus item info
            ],
            last_login_time # Last login date
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

        if self.game_config.always_vip:
                vip_expire_time = int((self.srvtime + timedelta(days=30)).timestamp())
        elif "vip_expire_time" in pdata["profile"]:
                vip_expire_time = pdata["profile"]["vip_expire_time"]

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
        
        if data["appVersion"].startswith("2.53"):
            for gate in self.game_config.enabled_gates:
                if not "gate" in pdata:
                    gates.append([gate,1,0,0,0,0,0])
                else:
                    for user_gate in pdata["gate"]:
                        added_gate = False

                        if user_gate["id"] == gate:
                            total_gate_pt += user_gate["progress"]
                            try:
                                gates.append([user_gate["id"],user_gate["type"],user_gate["page"],user_gate["progress"],
                                user_gate["loops"],user_gate["last_used"], user_gate["mission_flag"]])
                            except:
                                gates.append([user_gate["id"],user_gate["type"],user_gate["page"],user_gate["progress"],
                                user_gate["loops"],user_gate["last_used"], 0])
                            added_gate = True
                            break

                    if not added_gate:
                        gates.append([gate,1,0,0,0,0,0])
        else:
            for gate in self.game_config.enabled_gates:
                if not "gate" in pdata:
                    gates.append([gate,1,0,0,0,0])
                else:
                    for user_gate in pdata["gate"]:
                        added_gate = False

                        if user_gate["id"] == gate:
                            total_gate_pt += user_gate["progress"]
                            gates.append([user_gate["id"],user_gate["type"],user_gate["page"],user_gate["progress"],
                            user_gate["loops"],user_gate["last_used"]])
                            added_gate = True
                            break

                    if not added_gate:
                        gates.append([gate,1,0,0,0,0])

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
                pdata["profile"]["logins_today"], # Logins today
                pdata["profile"]["rating"] # Rating * 10
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
                plates  # Plates [id, type, aquired]
            ],
            scores, # [played, cleared, missless, fc, am] [same but this season only] [d, c, b, a, aa, aaa, s, ss, sss, master], 
            song_play_status, # Song play status?
            # [level, wp obtained, wp spend, cumulative score, # titles, # icons, # skill points, # colors, # input sounds, # plates, # gate points]
            [pdata["profile"]["xp"],pdata["profile"]["total_wp_gained"],0,cumulative_score,len(titles),len(icons),0,len(note_colors),len(note_sounds),len(plates),total_gate_pt], # TODO: Season info
            [ [0],[0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0],[0,0,0,0],[0,0,0,0,0,0,0],[0] ], # Play area info
            song_update_time, # Song list inquiry time?
            [] if "favorite" not in pdata else pdata["favorite"],
            [], # Stopped song IDs?
            [], # Event info
            gates, # gates
            last_song_info,
            [ [1,1],[2,1],[3,1],[4,1],[5,1] ], # TODO: Gate tutorial flags, 1 - 5
            [], # Gacha info id, # pulls (not supported)
            friends_list#friends_list# TODO: Friend info ID, Username, user type?, songlist consisting of songid, difficulty, and score
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
        self.data.game.put_item(user_id, self.game, self.version, self.ITEM_TYPES["navigator"], 210002, 
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
                0, # Days left
                0 # Rating
            ],
        ]

    def handle_user_status_update_request(self, data: Dict) -> List[Any]:
        game_id = data["params"][0]
        play_type = data["params"][1] # Counters for single, vs and coop play
        items_obtained = data["params"][2]
        is_continue = data["params"][3]
        is_first_play_free = data["params"][4]
        used_items = data["params"][5] # TODO: used items
        last_song_info = data["params"][6] # song_id, difficulty, folder order, folder id, song order        

        profile = self.data.game.get_profile(self.game, self.version, game_id=game_id)
        if profile is None: return []
        pdata = json.loads(profile["data"])
        user_id = profile["user"]

        pdata["profile"]["last_song_info"] = last_song_info # Might make this a dict later
        pdata["profile"]["play_counts"][play_type] += 1
        
        if is_continue == 1:
            pdata["profile"]["login_consec"] += 1
        else:
            pdata["profile"]["login_consec"] = 0

        icon_id = pdata["option"]["set_icon_id"]
        nav_id = pdata["option"]["set_nav_id"]
        icon = self.data.game.get_items(user_id, self.game, item_type=self.ITEM_TYPES["icon"], item_id=icon_id)
        nav = self.data.game.get_items(user_id, self.game, item_type=self.ITEM_TYPES["navigator"], item_id=nav_id)

        if icon and nav:
            icon_data = json.loads(icon[0][6])
            nav_data = json.loads(nav[0][6])
            icon_data["uses"] += 1
            nav_data["uses"] += 1
            nav_data["season_uses"] += 1
            self.data.game.put_item(user_id, self.game, self.version, self.ITEM_TYPES["icon"], icon_id, icon_data)
            self.data.game.put_item(user_id, self.game, self.version, self.ITEM_TYPES["navigator"], nav_id, nav_data)
        
        pdata = self.util_put_items(user_id, pdata, items_obtained)
        self.data.game.put_profile(user_id, self.game, self.version, data=pdata, should_inc_use=True)
        return []

    def handle_user_status_logout_request(self, data: Dict) -> List[Any]:
        return []

    def handle_user_music_update_request(self, data: Dict) -> List[Any]:
        game_id = data["params"][0]
        play_order = data["params"][1]
        # [song_id, difficulty, level, score, [marvs, greats, goods, misses], combo, rating, clear, 
        # missless, fc, am, gave_up, skill pt, fast, late, new_record]
        song_info = data["params"][2]        
        items_obtained = data["params"][3] # type, id, count

        #user_id = self.data.game.game_id_to_user_id(game_id, self.game, self.version)
        profile = self.data.game.get_profile(self.game, self.version, game_id=game_id)
        
        if profile is None:
            self.logger.warn(f"No profile for game_id {game_id} in handle_user_music_update_request", extra={"game": "WaccaLilyR"})
            return []
        
        user_id = profile["user"]
        pdata = self.util_put_items(user_id, json.loads(profile["data"]), items_obtained)
        self.data.game.put_profile(user_id, self.game, self.version, data=pdata)

        tmp = [0] * 10
        tmp[song_info[6] - 1] = 1
        grade = self.util_bitmask_array_to_int(tmp)

        fc_arr = [1,song_info[7],song_info[8],song_info[9],song_info[10]]
        fc = self.util_bitmask_array_to_int(fc_arr)
        self.data.game.put_score(user_id, self.game, self.version, song_info[0], song_info[1], song_info[3], 0, fc, 0, song_info[7], 
        grade, {
            "marv_count": song_info[4][0],
            "great_count": song_info[4][1],
            "good_count": song_info[4][2],
            "miss_count": song_info[4][3],
            "max_combo": song_info[5],
            "fast_count": song_info[13],
            "late_count": song_info[14],
        })

        old_score = self.data.game.get_best_scores(user_id, self.game, song_info[0], song_info[1])

        if not old_score:
            self.data.game.put_best_score(user_id, self.game, self.version, song_info[0], song_info[1], song_info[3], 0, fc, 0, song_info[7], 
            grade, {
                "lowest_miss_count": song_info[4][3],
                "rating": 0, # this will be updated once the user/rating/update endpoint is called
                "play_count": 1,
                "max_combo": song_info[5]
            })
            return [
                # song_id, difficulty, clear level bitmask, clear level bitmask (this season), grade bitmask, high score,
                # lowest miss count, 0, locked, rating
                [song_info[0],song_info[1],
                    [1,song_info[7],song_info[8],song_info[9],song_info[10]],
                    [1,song_info[7],song_info[8],song_info[9],song_info[10]],
                    tmp,
                    song_info[3],song_info[4][3],0,0,0
                ],
                [song_info[0],0], # number of (consecutive?) plays
                [0,0,0,0,0,0,0,0,0,0,0], # seasonal info
                [] # ranking info [type, rank]
            ]

        else:
            old_score = old_score[0]
            old_score_data = json.loads(old_score["data"])

            best_points = max(song_info[3], old_score["score1"])

            old_fc = self.util_int_to_bitmask_array(old_score["fc1"], 5)
            best_fc = self.util_bitmask_array_to_int([fc_arr[0] | old_fc[0], fc_arr[1] | old_fc[1], fc_arr[2] | old_fc[2], 
            fc_arr[3] | old_fc[3], fc_arr[4] | old_fc[4]])

            best_miss_count = min(song_info[4][3], old_score_data["lowest_miss_count"])

            best_grade = self.util_int_to_bitmask_array(old_score["grade"], 10)
            best_grade[song_info[6] - 1] = 1
            best_max_combo = max(old_score_data["max_combo"], song_info[5])
            print(best_grade)

            best_clear = song_info[7] | old_score["cleared"]

            if song_info[3] > old_score["score1"]:
                best_data = {
                    "lowest_miss_count": best_miss_count,
                    "rating": old_score_data["rating"],
                    "max_combo": best_max_combo,
                    "play_count": 1 if "play_count" not in old_score_data else old_score_data["play_count"] + 1
                }
            else:
                best_data = old_score_data
                best_data["lowest_miss_count"] = best_miss_count
                        
            self.data.game.put_best_score(user_id, self.game, self.version, song_info[0], song_info[1], best_points, 0, best_fc, 0, 
            best_clear, self.util_bitmask_array_to_int(best_grade), best_data)

            return [
                # song_id, difficulty, clear level bitmask, clear level bitmask (this season), grade bitmask, high score,
                # lowest miss count, 0, locked, rating
                [song_info[0],song_info[1],
                    [1,song_info[7],song_info[8],song_info[9],song_info[10]],
                    [1,song_info[7],song_info[8],song_info[9],song_info[10]],
                    best_grade,
                    song_info[3],song_info[4][3],0,0,0
                ],
                [song_info[0],0], # number of (consecutive?) plays
                [0,0,0,0,0,0,0,0,0,0,0], # seasonal info
                [] # rank-in info (unsure) [type, rank]
            ]
    
    def handle_user_music_unlock_request(self, data: Dict) -> List[Any]:
        game_id = data["params"][0]
        song_id = data["params"][1]
        difficulty = data["params"][2]
        # type, id, count
        items_used = data["params"][3] # It makes more sense that this would be a list of items used to purchase but w/e

        profile = self.data.game.get_profile(self.game, self.version, game_id=game_id)
        if profile is None: return []
        pdata = json.loads(profile["data"])
        user_id = profile["user"]

        items = self.data.game.get_items(user_id, self.game)
        tickets = []
        new_tickets = []
        old_difficulty = [0, 0, 0, 0]

        for item in items:
            if item[4] == self.ITEM_TYPES["ticket"]:
                tickets.append(item)

            elif item[4] == self.ITEM_TYPES["music_difficulty_unlock"] or item[4] == self.ITEM_TYPES["music_unlock"]:
                if item[5] == song_id:
                    idata = json.loads(item[6])
                    old_difficulty = idata["difficulty"]

        if difficulty == 0: # special case
            old_difficulty = [1, 1, 0, 0]
        else:
            old_difficulty[difficulty - 1] = 1

        for item in items_used:
            if item[0] == self.ITEM_TYPES["wp"]:
                if pdata["profile"]["wp"] >= item[2]:
                    pdata["profile"]["wp"] -= item[2]
                else: return []

            elif item[0] == self.ITEM_TYPES["ticket"]:
                for ticket in tickets:
                    if item[1] == ticket[5]:
                        tdata = json.loads(ticket[6])

                        if tdata["quantity"] >= item[2]:
                            tdata["quantity"] -= item[2]
                        else: return []

                        self.data.game.put_item(user_id, self.game, self.version, self.ITEM_TYPES["ticket"], ticket[5], tdata)
                        break
        
        self.data.game.put_profile(user_id, self.game, self.version, data=pdata)
        
        for x in range(0, len(tickets)):
            tdata = json.loads(tickets[x][6])
            for y in range(tdata["quantity"] - 1):
                new_tickets.append([y, tickets[x][5], 9999999999])

        # wp, ticket info
        self.data.game.put_item(user_id, self.game, self.version, self.ITEM_TYPES["music_difficulty_unlock"], song_id, {
            "obtainedDate": int(self.srvtime.timestamp()),
            "difficulty": old_difficulty
        })
        if difficulty > 2:
            old_score = self.data.game.get_best_scores(user_id, self.game, song_id, difficulty)
            if not old_score:
                self.data.game.put_best_score(user_id, self.game, self.version, song_id, difficulty, 0, 0, 0, 0, 0, 0, {
                    "lowest_miss_count": 0,
                    "rating": 0, 
                    "play_count": 0,
                    "max_combo": 0
                })

        return [pdata["profile"]["wp"], new_tickets]
    
    def handle_user_info_getMyroom_request(self, data: Dict) -> List[Any]:
        game_id = data["params"][0]
        return [
            0,0,0,0,0,[],0,0
        ]

    def handle_user_sugoroku_update_request(self, data: Dict) -> List[Any]:
        game_id = data["params"][0]
        gate_id = data["params"][1]
        page = data["params"][2]
        progress = data["params"][3]
        loops = data["params"][4]
        boosts_used = data["params"][5]
        items_obtained = data["params"][6] # Item type, item id, quantity gained
        total_points_on_gate = data["params"][7]
        found_gate = False
        if data["appVersion"].startswith("2.53"):
            mission_flag = data["params"][8]
        else:
            mission_flag = 0


        profile = self.data.game.get_profile(self.game, self.version, game_id=game_id)
        if profile is None: return []

        user_id = profile["user"]
        pdata = self.util_put_items(user_id, json.loads(profile["data"]), items_obtained)

        if not "gate" in pdata:
            pdata["gate"] = [{
                "id":gate_id, 
                "type": 1, # Unsure where this comes from
                "page": page, 
                "progress": progress, 
                "loops": loops, 
                "last_used": int(self.srvtime.timestamp()),
                "mission_flag": mission_flag,
                "total_points": total_points_on_gate
            }]

        else:
            for user_gate in pdata["gate"]:
                if user_gate["id"] == gate_id:
                    found_gate = True
                    user_gate["page"] = max(page, user_gate["page"])
                    user_gate["loops"] = max(loops, user_gate["loops"])
                    user_gate["progress"] = progress
                    user_gate["last_used"] = int(self.srvtime.timestamp())
                    user_gate["total_points"] = total_points_on_gate
                    break
        
            if not found_gate:
                pdata["gate"].append({
                    "id":gate_id, 
                    "type": 1,
                    "page": page, 
                    "progress": progress, 
                    "loops": loops, 
                    "last_used": int(self.srvtime.timestamp()),
                    "mission_flag": mission_flag,
                    "total_points": total_points_on_gate
                })
        
        self.data.game.put_profile(user_id, self.game, self.version, data=pdata)
        return []

    def handle_user_rating_update_request(self, data: Dict) -> List[Any]:
        game_id = data["params"][0]
        total_rating = data["params"][1]        
        songs = data["params"][2] # song_id, difficulty, rating
        profile = self.data.game.get_profile(self.game, self.version, game_id=game_id)

        if profile is None:
            self.logger.error(f"No profild found for game_id {game_id} in user_rating_update", extra={"game": "WaccaLilyR"})
            return []

        user_id = profile["user"]
        pdata = json.loads(profile["data"])

        for song in songs:
            song_id = song[0]
            chart_id = song[1]
            new_rating = song[2]

            scores = self.data.game.get_best_scores(user_id, self.game, song_id, chart_id)
            if scores:
                score = scores[0]
                sdata = json.loads(score["data"])
                sdata["rating"] = new_rating

                self.data.game.put_best_score(user_id, self.game, self.version, song_id, chart_id, score["score1"],
                score["score2"], score["fc1"], score["fc2"], score["cleared"], score["grade"], sdata)

        pdata["profile"]["rating"] = total_rating
        self.data.game.put_profile(user_id, self.game, self.version, data=pdata)

        return []

    def handle_user_info_getRanking_request(self, data: Dict) -> List[Any]:
        # total score, high score by song, cumulative socre, stage up score, other score, WP ranking
        # This likely requies calculating standings at regular intervals and caching the results
        return [0,0,0,0,0,0]

    def handle_user_trial_update_request(self, data: Dict) -> List[Any]:
        game_id = data["params"][0]
        dan_id = data["params"][1]
        dan_level = data["params"][2]
        clear_type = data["params"][3]
        scores = data["params"][4]
        num_cleared = data["params"][5]
        items_obtained = data["params"][6]
        unknown = data["params"][7]
        total_score = 0
        for score in scores:
            total_score += score

        profile = self.data.game.get_profile(self.game, self.version, game_id=game_id)
        if profile is None: return []
        pdata = json.loads(profile["data"])
        user_id = profile["user"]
        dans = self.data.game.get_achievements(user_id, self.game, self.version, 0, dan_id)

        if not dans:            
            self.data.game.put_achievement(user_id, self.game, self.version, 0, dan_id, {
                "dan_level": dan_level,
                "clear": clear_type,
                "clear_song_ct": num_cleared,
                "score1": scores[0],
                "score2": 0 if len(scores) < 2 else scores[1],
                "score3": 0 if len(scores) < 3 else scores[2],
                "total_score": total_score,
                "attemps": 1
            })

            if dan_level > 0 and clear_type > 0:
                if dan_level > pdata["profile"]["dan_level"] or (dan_level == pdata["profile"]["dan_level"] and clear_type > pdata["profile"]["dan_type"]):
                    pdata["profile"]["dan_level"] = dan_level
                    pdata["profile"]["dan_type"] = clear_type
                    self.data.game.put_profile(user_id, self.game, self.version, data=pdata)
        else:
            dan = dans[0]
            dan_data = json.loads(dan[6])

            if clear_type > dan_data["clear"]:
                self.data.game.put_achievement(user_id, self.game, self.version, 0, dan_id, {
                    "dan_level": dan_level,
                    "clear": clear_type,
                    "clear_song_ct": num_cleared,
                    "score1": scores[0],
                    "score2": 0 if len(scores) < 2 else scores[1],
                    "score3": 0 if len(scores) < 3 else scores[2],
                    "total_score": total_score,
                    "attemps": dan_data["attemps"] + 1
                })

                if clear_type > 0 and dan_level > 0:
                    if dan_level > pdata["profile"]["dan_level"] or (dan_level == pdata["profile"]["dan_level"] and clear_type > pdata["profile"]["dan_type"]):
                        pdata["profile"]["dan_level"] = dan_level
                        pdata["profile"]["dan_type"] = clear_type
                        self.data.game.put_profile(user_id, self.game, self.version, data=pdata)

        pdata = self.util_put_items(user_id, pdata, items_obtained)
        return []

    def handle_user_music_updateTrial_request(self, data: Dict) -> List[Any]:
        return self.handle_user_music_update_request(data)

    #TODO: Coop and vs data
    def handle_user_music_updateCoop_request(self, data: Dict) -> List[Any]:
        coop_info = data["params"][4]
        return self.handle_user_music_update_request(data)

    def handle_user_music_updateVersus_request(self, data: Dict) -> List[Any]:
        vs_info = data["params"][4]
        return self.handle_user_music_update_request(data)

    def handle_user_goods_purchase_request(self, data: Dict) -> List[Any]:
        game_id = data["params"][0]
        purchase_id = data["params"][1]
        purchase_count = data["params"][2]
        purchase_type = data["params"][3] # 1 is credit, 2 is wp
        cost = data["params"][4]
        items_obtained = data["params"][5]

        profile = self.data.game.get_profile(self.game, self.version, game_id=game_id)
        if profile is None: return []

        user_id = profile["user"]
        pdata = json.loads(profile["data"])        
        have_tickets = []

        if purchase_type == 2:
            pdata["profile"]["wp"] -= cost

        pdata = self.util_put_items(user_id, pdata, [items_obtained])

        tickets = self.data.game.get_items(user_id, self.game, item_type=self.ITEM_TYPES["ticket"])
        for ticket in tickets:
            have_tickets.append([1, ticket["item_id"], int((self.srvtime + timedelta(days=30)).timestamp())])
        
        return [pdata["profile"]["wp"], have_tickets]

    def handle_user_info_update_request(self, data: Dict) -> List[Any]:
        game_id = data["params"][0]
        option_updates = data["params"][1]
        date_updates = data["params"][3] # 1-9, I think we only care about 1
        songs_favotired = data["params"][4]
        songs_unfavotired = data["params"][5]

        profile = self.data.game.get_profile(self.game, self.version, game_id=game_id)
        if profile is None: return []

        pdata = json.loads(profile["data"])
        user_id = profile["user"]

        for opt in option_updates:
            for k,v in self.OPTIONS.items():
                if opt[0] == v:
                    pdata["option"][k] = opt[1]
                    break

        for update in date_updates:
            if update[0] == 1:
                pdata["profile"]["song_update_time"] = update[1]

        if not "favorite" in pdata:
            pdata["favorite"] = []

        for fav in songs_favotired:
            pdata["favorite"].append(fav)

        for unfav in songs_unfavotired:
            pdata["favorite"].remove(unfav)

        self.data.game.put_profile(user_id, self.game, self.version, data=pdata)
        return []

    def handle_user_trial_get_request(self, data: Dict) -> List[Any]:
        game_id = data["params"][0]
        user_id = self.data.game.game_id_to_user_id(game_id, self.game, self.version)
        dan_list =  [
                [2501,1,0,0,[0,0,0], 1],
                [2502,2,0,0,[0,0,0], 1],
                [2503,3,0,0,[0,0,0], 1],
                [2504,4,0,0,[0,0,0], 1],
                [2505,5,0,0,[0,0,0], 1],
                [2506,6,0,0,[0,0,0], 1],
                [2507,7,0,0,[0,0,0], 1],
                [2508,8,0,0,[0,0,0], 1],
                [2509,9,0,0,[0,0,0], 1],
                [210001,0,0,0,[0,0,0], 1],
                [210002,0,0,0,[0,0,0], 1],
                [210003,0,0,0,[0,0,0], 1],
            ]

        if user_id is None:
            self.logger.error(f"Could not find user_id for game_id {game_id} in handle_user_trial_get_request", extra={"game": "WaccaLilyR"})
            return []

        dans = self.data.game.get_achievements(user_id, self.game, self.version, 0)
        self.logger.info(dans)
        if dans is None or not dans:
            return [dan_list]
        
        for dan in dans:
            dan_data = json.loads(dan[6])

            if dan[5] == 2509 and dan_data["clear"] > 0:
                dan_list.append([2510,10,0,0,[0,0,0], 1])
            if dan[5] == 2510 and dan_data["clear"] > 0:
                dan_list.append([2511,11,0,0,[0,0,0], 1])
            if dan[5] == 2511 and dan_data["clear"] > 0:
                dan_list.append([2512,12,0,0,[0,0,0], 1])
            if dan[5] == 2512 and dan_data["clear"] > 0:
                dan_list.append([2513,13,0,0,[0,0,0], 1])
            if dan[5] == 2513 and dan_data["clear"] > 0:
                dan_list.append([2514,14,0,0,[0,0,0], 1])

            for base in dan_list:
                if dan[5] == base[0]:
                    base[2] = dan_data["clear"]
                    base[3] = dan_data["clear_song_ct"]
                    base[4][0] = dan_data["score1"]
                    base[4][1] = dan_data["score2"]
                    base[4][2] = dan_data["score3"]

        return [
           dan_list
        ]
    
    def handle_user_vip_get_request(self, data: Dict) -> List[Any]:
        game_id = data["params"][0]
        rollover = 0

        profile = self.data.game.get_profile(self.game, self.version, game_id=game_id)
        if profile is None: return []
        pdata = json.loads(profile["data"])
        
        if self.game_config.always_vip:
            rollover = int((self.srvtime + timedelta(days=30)).timestamp())
        elif "vip_expire_time" in pdata["profile"] and pdata["profile"]["vip_expire_time"] > int(self.srvtime.timestamp()):
            rollover = int((pdata["profile"]["vip_expire_time"] - int(self.srvtime.timestamp())) / 86400)

        return [ # TODO: proper VIP get, this works for now tho
            30 + rollover, 
            [
                1,1,
                [
                    [1,0,[16,211025,1]],
                    [2,0,[6,202086,1]],
                    [3,0,[11,205008,1]],
                    [4,0,[10,203009,1]],
                    [5,0,[16,211026,1]],
                    [6,0,[9,206001,1]]
                ]
            ]
        ]

    def handle_user_vip_start_request(self, data: Dict) -> List[Any]:
        game_id = data["params"][0]
        cost = data["params"][1]
        time = data["params"][2] # matches the value from vip get

        profile = self.data.game.get_profile(self.game, self.version, game_id=game_id)
        if profile is None: return []
        pdata = json.loads(profile["data"])
        mods = json.loads(profile["mods"])
        user_id = profile["user"]

        # This should never happen because wacca stops you from buying VIP
        # if you have more then 10 days remaining, but this IS wacca we're dealing with...
        if self.game_config.always_vip:
            return [int((self.srvtime + timedelta(days=time)).timestamp()), []]

        pdata["profile"]["vip_expire_time"] = int((self.srvtime + timedelta(days=time)).timestamp())

        self.data.game.put_profile(user_id, self.game, self.version, data=pdata)
        return [pdata["profile"]["vip_expire_time"], []] # TODO: present

    def handle_competition_status_login_request(self, data: Dict) -> List[Any]:
        return []

    def handle_competition_status_update_request(self, data: Dict) -> List[Any]:
        return []
