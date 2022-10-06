from typing import List, Dict

from aime.titles.wacca.handlers.base import BaseRequest
from aime.titles.wacca.handlers.helpers import UserItemInfoV1, UserStatusV1, UserStatusV2, ProfileStatus
from aime.titles.wacca.handlers.helpers import PlayVersionStatus, PlayModeCounts, SongDetail, SeasonalInfo
from aime.titles.wacca.handlers.helpers import UserItemInfoV2, UserItemInfoV3, BingoDetail, GateDetail
from aime.titles.wacca.handlers.helpers import LastSongDetail, FriendDetail

# ---user/status/get----
class UserStatusGetRequest(BaseRequest):
    aimeId: int = 0

    def __init__(self, data: Dict) -> None:
        super().__init__(data)
        self.aimeId = int(data["params"][0])

class UserStatusGetV1Response():
    userStatus: UserStatusV1 = UserStatusV1()
    setTitleId: int = 0
    setIconId: int = 0
    profileStatus: ProfileStatus = ProfileStatus.ProfileGood
    versionStatus: PlayVersionStatus = PlayVersionStatus.VersionGood
    lastGameVersion: str = ""

    def make(self) -> List:
        return [
            self.userStatus.make(),
            self.setTitleId,
            self.setIconId,
            self.profileStatus.value
            [
                self.versionStatus.value,
                self.lastGameVersion
            ]
        ]

class UserStatusGetV2Response(UserStatusGetV1Response):
    userStatus: UserStatusV2 = UserStatusV2()
    unknownArr: List = []

    def make(self) -> List:
        ret = super().make()

        ret.append(self.unknownArr)

        return ret

# ---user/status/getDetail----
class UserStatusGetDetailRequest(BaseRequest):
    userId: int = 0

    def __init__(self, data: Dict) -> None:
        super().__init__(data)
        self.userId = data["params"][0]

class UserStatusGetDetailResponseV1():
    userStatus: UserStatusV1 = UserStatusV1()
    options: List = []
    seasonalPlayModeCounts: List[PlayModeCounts] = []
    userItems: List[UserItemInfoV1] = []
    scores: List[SongDetail] = []
    songPlayStatus: List[int] = [0,0]
    seasonInfo: SeasonalInfo = []
    playAreaList: List = [ [0],[0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0],[0,0,0,0],[0,0,0,0,0,0,0],[0] ]
    songUpdateTime: int = 0

    def make(self) -> List:
        play_modes = []
        song_unlocks = []
        titles = []
        icons = []
        trophies = []
        skills = []
        tickets = []
        note_colors = []
        note_sounds = []
        navigators = []
        scores = []

        for x in self.seasonalPlayModeCounts:
            play_modes.append(x.make())
        
        for x in self.userItems:
            for y in x.songUnlocks:
                song_unlocks.append(y.make())
            for y in x.titles:
                titles.append(y.make())
            for y in x.icons:
                icons.append(y.make())
            for y in x.trophies:
                trophies.append(y.make())
            for y in x.tickets:
                tickets.append(y.make())
            for y in x.noteColors:
                note_colors.append(y.make())
            for y in x.noteSounds:
                note_sounds.append(y.make())
            for y in x.navigators:
                navigators.append(y.make())
        
        for x in self.scores:
            scores.append(x.make())

        return [
            self.userStatus.make(),
            self.options,
            play_modes,
            [
                song_unlocks,
                titles,
                icons,
                trophies,
                skills,
                tickets,
                note_colors,
                note_sounds,
                navigators
            ],
            scores,
            self.songPlayStatus,
            self.seasonInfo.make(),
            self.playAreaList,
            self.songUpdateTime
        ]

class UserStatusGetDetailResponseV2(UserStatusGetDetailResponseV1):
    userItems: List[UserItemInfoV2] = []
    favorites: List[int] = []
    stoppedSongIds: List[int] = []
    eventInfo: List[int] = []
    gateInfo: List[GateDetail] = []
    lastSongInfo: List[LastSongDetail] = []
    gateTutorialFlags: List[List[int]] = [ [1,1],[2,1],[3,1],[4,1],[5,1] ]
    gatchaInfo: List = []
    friendList: List[FriendDetail] = []

    def make(self) -> List:
        ret = super().make()
        plates = []
        gates = []
        last_song = []
        friends = []

        for x in self.userItems:
            for y in x.plates:
                plates.append(y.make())

        ret[3].append(plates)
        ret.append(self.favorites)
        ret.append(self.stoppedSongIds)
        ret.append(self.eventInfo)
        ret.append(gates)
        ret.append(last_song)
        ret.append(self.gateTutorialFlags)
        ret.append(self.gatchaInfo)
        ret.append(friends)

        return ret

class UserStatusGetDetailResponseV3(UserStatusGetDetailResponseV2):
    userItems: List[UserItemInfoV3] = []
    bingoStatus: BingoDetail = []

    def make(self) -> List:
        ret = super().make()
        touch_effect = []

        for x in self.userItems:
            for y in x.touchEffect:
                touch_effect.append(y)

        ret[3].append(touch_effect)
        ret.append(self.bingoStatus.make())

        return ret

# ---user/status/login----
