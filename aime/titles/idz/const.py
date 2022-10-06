class IDZConstants():
    GAME_CODE = "SDDF"

    CONFIG_NAME = "idz.yaml"

    VER_IDZ_V110 = 0
    VER_IDZ_V130 = 1
    VER_IDZ_V210 = 2
    VER_IDZ_V230 = 3

    VERSION_STRING = ("InitialD Arcade Stage Zero", "InitialD Arcade Stage Zero Version 2")

    @classmethod
    def game_ver_to_string(cls, ver: int):
            return cls.VERSION_STRING[ver]