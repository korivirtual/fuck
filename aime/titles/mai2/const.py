class Mai2Constants():
    GAME_CODE = "SDEZ"

    CONFIG_NAME = "mai2.yaml"

    VER_MAIMAI_DX = 0
    VER_MAIMAI_DX_PLUS = 1
    VER_MAIMAI_DX_SPLASH = 2
    VER_MAIMAI_DX_SPLASH_PLUS = 3
    VER_MAIMAI_DX_UNIVERSE = 4

    VERSION_STRING = ("maimai Delux", "maimai Delux+", "maimai Delux Splash", "maimai Delux Splash+", "maimai Delux Universe")

    @classmethod
    def game_ver_to_string(cls, ver: int):
            return cls.VERSION_STRING[ver]