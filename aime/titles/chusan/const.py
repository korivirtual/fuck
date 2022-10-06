class ChusanConstants():
    GAME_CODE = "SDHD"

    VER_CHUNITHM = 0
    VER_CHUNITHM_NEW = 1
    VER_CHUNITHM_NEW_PLUS = 2

    VERSION_NAMES = ("Chunithm", "Chunithm New", "Chunithm New Plus")

    @classmethod
    def game_ver_to_string(cls, ver: int):
        cls.VERSION_NAMES[ver]
