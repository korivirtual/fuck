from typing import List, Dict
from enum import Enum

class UserStatusV1():
    userId: int = -1
    username: str = ""
    userType: int = 1
    xp: int = 0
    danLevel: int = 0
    danType: int = 0
    wp: int = 0
    titlePartIds: List[int] = [0, 0, 0]
    useCount: int = 0
    loginDays: int = 0
    loginConsecutive: int = 0
    loginConsecutiveDays: int = 0
    vipExpireTime: int = 0

    def make(self) -> List:
        return [
            self.userId,
            self.username,
            self.userType,
            self.xp,
            self.danLevel,
            self.danType,
            self.wp,
            self.titlePartIds,
            self.useCount,
            self.loginDays,
            self.loginConsecutive,
            self.loginConsecutiveDays,
            self.vipExpireTime
        ]

class UserStatusV2(UserStatusV1):
    loginsToday: int = 0
    rating: int = 0

    def make(self) -> List:
        ret = super().make()

        ret.append(self.loginsToday)
        ret.append(self.rating)

        return ret

class ProfileStatus(Enum):
    ProfileGood = 0
    ProfileNeedRegister = 1
    ProfileInUse = 2
    ProfileWrongRegion = 3

class PlayVersionStatus(Enum):
    VersionGood = 0
    VersionTooNew = 1
    VersionNeedUpgrade = 2

class PlayModeCounts():
    seasonId: int = 0
    modeId: int = 0
    playNum: int = 0

    def __init__(self, seasonId: int, modeId: int, playNum: int) -> None:
        self.seasonId = seasonId
        self.modeId = modeId
        self.playNum = playNum
    
    def make(self) -> List:
        return [
            self.seasonId,
            self.modeId,
            self.playNum
        ]

class SongUnlock():
    songId: int = 0
    difficulty: int = 0
    whenAppeared: int = 0
    whenUnlocked: int = 0

    def __init__(self) -> None:
        pass

    def make(self) -> List:
        return [
            self.songId,
            self.difficulty,
            self.whenAppeared,
            self.whenUnlocked
        ]

class GenericItem():
    itemId: int = 0
    itemType: int = 0
    whenAcquired: int = 0

    def __init__(self, itemId: int, itemType: int, whenAcquired: int) -> None:
        self.itemId = itemId
        self.itemType = itemType
        self.whenAcquired = whenAcquired
    
    def make(self) -> List:
        return [
            self.itemId,
            self.itemType,
            self.whenAcquired
        ]

class IconItem(GenericItem):
    uses: int = 0

    def __init__(self, itemId: int, itemType: int, whenAcquired: int, uses: int) -> None:
        super().__init__(itemId, itemType, whenAcquired)
        self.uses = uses
    
    def make(self) -> List:
        return [
            self.itemId,
            self.itemType,
            self.uses,
            self.whenAcquired
        ]

class TrophyItem(GenericItem):
    progress: int = 0

    def __init__(self, itemId: int, itemType: int, whenAcquired: int, progress: int) -> None:
        super().__init__(itemId, itemType, whenAcquired)
        self.progress = progress
    
    def make(self) -> List:
        return [
            self.itemId,
            0,
            self.progress,
            0
        ]

class TicketItem():
    userTicketId: int = 0
    ticketId: int = 0
    whenExpires: int = 0

    def __init__(self, userTicketId: int, ticketId: int, whenExpires: int) -> None:
        self.userTicketId = userTicketId
        self.ticketId = ticketId
        self.whenExpires = whenExpires
    
    def make(self) -> List:
        return [
            self.userTicketId,
            self.ticketId,
            self.whenExpires
        ]


class NavigatorItem(IconItem):
    usesToday: int = 0

    def __init__(self, itemId: int, itemType: int, whenAcquired: int, uses: int, usesToday: int) -> None:
        super().__init__(itemId, itemType, whenAcquired, uses)
        self.usesToday = usesToday

    def make(self) -> List:
        return [
            self.itemId,
            self.itemType,
            self.whenAcquired,
            self.uses,
            self.usesToday
        ]

class UserItemInfoV1():
    songUnlocks: List[SongUnlock] = []
    titles: List[GenericItem] = []
    icons: List[IconItem] = []
    trophies: List[TrophyItem] = []
    skills: List = []
    tickets: List[TicketItem] = []
    noteColors: List[GenericItem] = []
    noteSounds: List[GenericItem] = []
    navigators: List[NavigatorItem] = []

class UserItemInfoV2(UserItemInfoV1):
    plates: List[GenericItem] = []

class UserItemInfoV3(UserItemInfoV2):
    touchEffect: List[GenericItem] = []

class SongDetail():
    def make(self) -> List:
        return []

class SeasonalInfo():
    def make(self) -> List:
        return []

class BingoPageStatus():
    def make(self) -> List:
        return []

class BingoDetail():
    pageNumber: int = 1
    pageStatus: List[BingoPageStatus] = []

    def __init__(self, pageNumber: int) -> None:
        self.pageNumber = pageNumber
    
    def make(self) -> List:
        status = []
        for x in self.pageStatus:
            status.append(x)

        return [
            self.pageNumber,
            status
        ]

class GateDetail():
    def make(self) -> List:
        return []

class LastSongDetail():
    def make(self) -> List:
        return []

class FriendDetail():
    def make(self) -> List:
        return []