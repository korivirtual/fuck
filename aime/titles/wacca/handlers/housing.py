from typing import List, Dict

from aime.titles.wacca.handlers.base import BaseRequest

# ---housing/get----
class HousingGetResponse():
    housingId: int = 1337
    unknown1: int = 0

    def __init__(self, housingId: int) -> None:
        self.housingId = housingId

    def make(self) -> List:
        return [self.housingId, self.unknown1]

# ---housing/start----
class HousingStartRequest(BaseRequest):
    lanInstallType: str = "SERVER"
    countryName: str = "JPN"

    def __init__(self, data: Dict) -> None:
        super().__init__(data)
        self.lanInstallType = data["params"][0, 1]
        self.countryName = data["params"][1, 1]

class HousingStartResponse():
    regionId: int = 1
    songList: List[int] = []

    def __init__(self, regionId: int, songList: List[int]) -> None:
        self.regionId = regionId
        self.songList = songList

    def make(self) -> List:
        return [self.regionId, self.songList]
