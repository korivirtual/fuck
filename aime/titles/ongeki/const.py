class OngekiConstants():
    GAME_CODE = "SDDT"

    VER_ONGEKI = 0
    VER_ONGEKI_PLUS = 1
    VER_ONGEKI_SUMMER = 2
    VER_ONGEKI_SUMMER_PLUS = 3
    VER_ONGEKI_RED = 4
    VER_ONGEKI_RED_PLUS = 5
    VER_ONGEKI_BRIGHT = 6
    VER_ONGEKI_BRIGHT_MEMORY = 7

    ONGEKI = ("ONGEKI", "ONGEKI+", "ONGEKI Summer", "ONGEKI Summer+", "ONGEKI Red", "ONGEKI Red+", "ONGEKI Bright", "ONGEKI Bright Memory")

    @classmethod
    def game_ver_to_string(cls, ver: int):
        cls.VERSION_NAMES[ver]