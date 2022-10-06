class WaccaConstants():
    CONFIG_NAME = "wacca.yaml"
    GAME_CODE = "SDFE"

    VER_WACCA = 0
    VER_WACCA_S = 1
    VER_WACCA_LILY = 2
    VER_WACCA_LILY_R = 3
    VER_WACCA_REVERSE = 4

    VERSION_NAMES = ("WACCA", "WACCA S", "WACCA Lily", "WACCA Lily R", "WACCA Reverse")

    @classmethod
    def game_ver_to_string(cls, ver: int):
        cls.VERSION_NAMES[ver]