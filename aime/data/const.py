"""
Class for storing game codes. 
"""
class GameCodes():
    DUMMY = "SXXX"

"""
Class for storing internal references for game versions.
"""
class GameVersions():
    DUMMY = 0

class MainboardPlatformCodes():
    RINGEDGE = "AALE"
    RINGWIDE = "AAML"
    NU = "AAVE"
    NUSX = "AAWE"
    ALLS_UX = "ACAE"
    ALLS_HX = "ACAX"

class MainboardRevisions():
    RINGEDGE = 1
    RINGEDGE2 = 2

    RINGWIDE = 1

    NU1 = 1
    NU11 = 11
    NU2 = 12

    NUSX = 1
    NUSX11 = 11

    ALLS_UX = 1
    ALLS_HX = 11
    ALLS_UX2 = 2
    ALLS_HX2 = 12

class KeychipPlatformsCodes():
    RING = "A72E"
    NU = ("A60E", "A60E", "A60E")
    NUSX = ("A61X", "A69X")
    ALLS = "A63E"

class GameStrings():
    DUMMY = ("Dummy Game")

def game_ver_to_string(game: str, ver: int):
    """
    Given a game string and a version number, return a string representation of that game
    """
    if GameCodes.DUMMY in game:
        return GameStrings.DUMMY[ver]
    
