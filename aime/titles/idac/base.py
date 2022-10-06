from datetime import datetime, date, timedelta
from multiprocessing import Event
from typing import Any, List, Dict
import logging
import pytz
import json

from aime.data import Data, Config
from aime.titles.idac.const import IDACConstants
from aime.titles.idac.config import IDACConfig

class IDACBase():
    def __init__(self, cfg: Config, game_cfg: IDACConfig) -> None:
        self.core_config = cfg
        self.game_config = game_cfg
        self.game = IDACConstants.GAME_CODE
        self.version = IDACConstants.VER_IDAC_BASE
        self.data = Data(cfg)
        self.logger = logging.getLogger("idac")
    
    def handle_alive_get_request(self, data: Dict, headers: Dict):
        return {"status_code": "0", "server_status" : 1, "force_reboot_time": int(datetime.now().timestamp()) - 86400}
    
    def handle_boot_getconfigdata_request(self, data: Dict, headers: Dict):
        return {
            "status_code": "0",
            "free_continue_enable": 1,
            "free_continue_new": 1,
            "free_continue_play": 1,
            "difference_time_to_jp": 0,
            "asset_version": 1,
            "optional_version": 1,
            "disconnect_offset": 0,
            "boost_balance_version": 1,
            "time_release_number": 0,
            "play_stamp_enable": 1,
            "play_stamp_bonus_coin": 1,
            "gacha_chara_needs": 1,
            "both_win_system_control": 1,
            "subcard_system_congrol": 1,
            "server_maintenance_start_hour": 0,
            "server_maintenance_start_minutes": 0,
            "server_maintenance_end_hour": 0,
            "server_maintenance_end_minutes": 0,
            "domain_api_game": f"http://{self.core_config.title.hostname}:{self.game_config.ports.main}",
            "domain_matching": f"http://{self.core_config.title.hostname}:{self.game_config.ports.matching}",
            "domain_echo1": f"{self.core_config.title.hostname}:{self.game_config.ports.echo1}",
            "domain_echo2": f"{self.core_config.title.hostname}:{self.game_config.ports.echo2}",
            "domain_ping": f"{self.core_config.title.hostname}",
            "battle_gift_event_master": 1,
            "round_event": 1,
            "last_round_event": 1,
            "last_round_event_ranking": 1,
            "round_event_exp": 1,
            "stamp_info": 1,
            "timerelease_no": 1,
            "timerelease_avatar_gacha_no": 1,
            "takeover_reward": 1,
            "subcard_judge": 1,
            "special_promote": 1,
            "matching_id": 1,
            "matching_group": 1,
            "timetrial_disp_date": 1,
            "buy_car_need_cash": 1,
            "time_extension_limit": 1,
            "collabo_id": 0,
            "driver_debut_end_date": 0,
            "online_battle_param1": 1,
            "online_battle_param2": 1,
            "online_battle_param3": 1,
            "online_battle_param4": 1,
            "online_battle_param5": 1,
            "online_battle_param6": 1,
            "online_battle_param7": 1,
            "online_battle_param8": 1,
            "theory_open_version": "1.30",
            "theory_close_version": "1.50",
            "special_mode_data": 1111
        }
    
    def handle_boot_bookkeep_request(self, data: Dict, headers: Dict):
        pass
    
    def handle_boot_getgachadata_request(self, data: Dict, headers: Dict):
        pass

    def handle_boot_gettimereleasedata_request(self, data: Dict, headers: Dict):
        with open("./aime/titles/idac/data/timeRelease.json") as f:
            time_release_data = json.load(f)
        
        return time_release_data

    def handle_advertise_getrankingdata_request(self, data: Dict, headers: Dict):
        pass

    def handle_login_checklock_request(self, data: Dict, headers: Dict):
        # 1: good
        # 2: too new
        # other: in use
        return {
            "status_code": "0",
            "lock_result": 1,
            "lock_date": int(datetime.now().timestamp()),
            "daily_play": 0,
            "session": f"{data['id']}",
            "shared_security_key": "a",
            "session_procseq": "a",
            "new_player": 0,
            "server_status": 1
        }
    
    def handle_login_unlock_request(self, data: Dict, headers: Dict):
        pass

    def handle_user_getdata_request(self, data: Dict, headers: Dict):
        return {
            "status_code": "0", 
            "user_base_data": {
                "id": int(headers["session"]),
                "username": "あああ",                
                "store_name": "あ",                
                "country": 56,
                "store": 4816,
                "team_id": 0,
                "total_play": 1,
                "daily_play": 0,
                "day_play": 0,
                "mileage": 1000,
                "asset_version": 1,
                "last_played_date": int(datetime.now().timestamp()),
                "mytitle_id": 1,
                "mytitle_effect_id": 1,
                "sticker_id": 1,
                "sticker_effect_id": 1,
                "stamp_key_assign_0": 1,
                "stamp_key_assign_1": 1,
                "stamp_key_assign_2": 1,
                "stamp_key_assign_3": 1,
                "name_change_category": 0,
                "factory_disp": 1,
                "have_car_cnt": 1,
                "cash": 10,
                "dressup_point": 10,
                "avitar_point": 10,
                "total_cash": 10,
            },
            "avatar_data": {"sex":0,"face":1,"eye":1,"mouth":1,"hair":1,"glasses":0,"face_accessory":0,"body":1,"body_accessory":0,"behind":0,"bg":1,"effect":0,"special":0},
            "pick_up_car_data": [
                {
                    "maker_id": 3,
                    "style_car_id": 512,
                    "color": 0,
                    "kana": 12,
                    "s_no": 59,
                    "l_no": 5040,
                    "car_flag": 21527,
                    "tune_point": 20,
                    "tune_parts": 20,
                    "infinity_tune": 0,
                    "online_vs_win": 1,
                    "color_stock_list": "oAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAA",
                    "color_stock_new_list": "oAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAA",
                    "parts_stock_list": "AAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
                    "parts_stock_new_list": "AAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
                    "parts_set_equip_list": "AAEAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
                    "use_count": 1,
                    "story_use_count": 1,
                    "timetrial_use_count": 1,
                    "vs_use_count": 1,
                    "net_vs_use_count": 1,
                    "theory_use_count": 1,
                    "car_mileage": 10,
                    "pickup_seq": 1,
                    "purchase_seq": 1,
                    "equip_parts_count": 0,
                    "use_dt": 0,
                    "ticket_cnt": 0
                }
            ],
            "vsinfo_data": {},
            "stock_data": {},
            "mission_data": {},
            "weekly_mission_data": {},
            "course_data": {},
            "toppatu_event_data": {},
            "event_data": {},
            "rewards_data": {},
            "login_bonus_data": {},
            "penalty_data": {},
            "config_data": {'id': 0, 'steering_intensity': 4, 'transmission_type': 1, 'default_viewpoint': 1, 'favorite_bgm': 0, 'bgm_volume': 7, 'se_volume': 7, 'master_volume': 7, 'store_battle_policy': 0, 'battle_onomatope_display': 1, 'cornering_guide': 1, 'minimap': 2, 'line_guide': 1, 'ghost': 0, 'race_exit': 1, 'result_skip': 0},
            "battle_gift_data": {},
            "round_event": 0,
            "last_round_event": 0,
            "past_round_event": 0,
            "avatar_gacha_lottery_data": {},
            "fulltune_count": 1,
            "total_car_parts_count": 0,
            "car_layout_count": 0,
            "car_style_count": 0,
            "story_course": 0,
            "driver_debut": 0,
            "theory_data": {},
            "theory_course_data": {},
            "theory_partner_data": {},
            "theory_running_pram_data": {},
        }

    def handle_user_createaccount_request(self, data: Dict, headers: Dict):
        pass

    def handle_user_updatelogin_request(self, data: Dict, headers: Dict):
        pass

    def handle_timetrial_getcarbest_request(self, data: Dict, headers: Dict):
        pass

    def handle_factory_getcardata_request(self, data: Dict, headers: Dict):
        pass