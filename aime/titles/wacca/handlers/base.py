from typing import Dict, List
from datetime import datetime

class BaseRequest():
    requestNo: int = 0
    appVersion: str = ""
    boardId: str = ""
    chipId: str = ""

    def __init__(self, data: Dict) -> None:
        self.requestNo = data["requestNo"]
        self.appVersion = data["appVersion"]
        self.boardId = data["boardId"]
        self.chipId = data["chipId"]

class BaseResponse():
    status: int = 0
    message: str = ""
    serverTime: int = int(datetime.now().timestamp())
    maintNoticeTime: int = 0
    maintNotPlayableTime: int = 0
    maintStartTime: int = 0
    params: List = []

    def make(self) -> Dict:
        return []

class AdvertiseGetNewseV1Response():
    notices: List[str] = []
    copyright: List[str] = []
    stoppedSongs: List[int] = []
    stoppedJackets: List[int] = []
    stoppedMovies: List[int] = []
    stoppedIcons: List[int] = []

    def make(self) -> List:
        return [
            self.notices,
            self.copyright,
            self.stoppedSongs,
            self.stoppedJackets,
            self.stoppedMovies,
            self.stoppedIcons,
        ]

class AdvertiseGetNewseV2Response(AdvertiseGetNewseV1Response):
    stoppedProducts: List[int] = []

    def make(self) -> List:
        ret = super().make()

        ret.append(self.stoppedProducts)

        return ret
