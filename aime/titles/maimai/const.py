class MaimaiConstants():
    GAME_CODE = "SDEY" # Not sure how to handle game code changes between versions...

    VER_MAIMAI = 0
    VER_MAIMAI_PLUS = 1
    VER_MAIMAI_GREEN = 2
    VER_MAIMAI_GREEN_PLUS = 3
    VER_MAIMAI_ORANGE = 4
    VER_MAIMAI_ORANGE_PLUS = 5
    VER_MAIMAI_PINK = 6
    VER_MAIMAI_PINK_PLUS = 7
    VER_MAIMAI_MURASAKI = 8
    VER_MAIMAI_MURASAKI_PLUS = 9
    VER_MAIMAI_MILK = 10
    VER_MAIMAI_MILK_PLUS = 11
    VER_MAIMAI_FINALE = 12

    VERSION_NAMES = ("maimai","maimai PLUS","maimai GReeN","maimai GReeN PLUS","maimai ORANGE","maimai ORANGE PLUS",
    "maimai PiNK","maimai PiNK PLUS","maimai MURASAKi","maimai MURASAKi PLUS","maimai MiLK","maimai MiLK PLUS","maimai FiNALE")

    @classmethod
    def game_ver_to_string(cls, ver: int):
        cls.VERSION_NAMES[ver]