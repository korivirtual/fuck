from pathlib import Path
import logging
from typing import Optional

try:
    from UE4Parse.Assets.PackageReader import LegacyPackageReader
    from UE4Parse.BinaryReader import BinaryStream
    from UE4Parse.Provider import DefaultFileProvider
    from UE4Parse.Versions import EUEVersion, VersionContainer
except:
    pass

from aime.data import Config, Data
from aime.titles.wacca.lilyr import WaccaLilyR

class WaccaImporter():
    def __init__(self, cfg: Config, cfg_dir: str) -> None:
        self.config = cfg
        self.data = Data(cfg)
        self.logger = logging.getLogger("importer")
    
    def importer(self, ver: int, bin: str, opt: str):
        try:
            music = self.load(f"{bin}/Table/MusicParameterTable.uasset", f"{bin}/Table/MusicParameterTable.uexp")
            # Maybe music unlocks?
            
            trophy_table = self.load(f"{bin}/Table/TrophyTable.uasset", f"{bin}/Table/TrophyTable.uexp")
            trophy_message = self.load(f"{bin}/Message/TrophyMessage.uasset", f"{bin}/Table/TrophyMessage.uexp")

            icon_table = self.load(f"{bin}/Table/IconTable.uasset", f"{bin}/Table/IconTable.uexp")
            icon_message = self.load(f"{bin}/Message/IconMessage.uasset", f"{bin}/Table/IconMessage.uexp")

            title_table = self.load(f"{bin}/Table/GradeTable.uasset", f"{bin}/Table/GradeTable.uexp")
            title_message = self.load(f"{bin}/Message/GradeMessage.uasset", f"{bin}/Table/GradeMessage.uexp")
            # Maybe include title parts at some point?
            
            skill_table = self.load(f"{bin}/Table/SkillTable.uasset", f"{bin}/Table/SkillTable.uexp")
            skill_message = self.load(f"{bin}/Message/SkillMessage.uasset", f"{bin}/Table/SkillMessage.uexp")

            ticket_table = self.load(f"{bin}/Table/TicketItemTable.uasset", f"{bin}/Table/TicketItemTable.uexp")
            ticket_message = self.load(f"{bin}/Message/TicketItemMessage.uasset", f"{bin}/Table/TicketItemMessage.uexp")

            note_color_table = self.load(f"{bin}/Table/NoteColorTable.uasset", f"{bin}/Table/NoteColorTable.uexp")
            note_color_message = self.load(f"{bin}/Message/NoteColorMessage.uasset", f"{bin}/Table/NoteColorMessage.uexp")

            note_se_table = self.load(f"{bin}/Table/SESetTable.uasset", f"{bin}/Table/SESetTable.uexp")
            note_se_message = self.load(f"{bin}/Message/SESetMessage.uasset", f"{bin}/Table/SESetMessage.uexp")

            nav_table = self.load(f"{bin}/Table/NavigateCharacterTable.uasset", f"{bin}/Table/NavigateCharacterTable.uexp")
            nav_message = self.load(f"{bin}/Message/NavigateCharacterMessage.uasset", f"{bin}/Table/NavigateCharacterTable.uexp")

            plate_table = self.load(f"{bin}/Table/UserPlateBackgroundTable.uasset", f"{bin}/Table/UserPlateBackgroundTable.uexp")
            plate_message = self.load(f"{bin}/Message/UserPlateBackgroundMessage.uasset", f"{bin}/Table/UserPlateBackgroundMessage.uexp")
        except:
            self.logger.error("Could not import wacca assets, please make sure you have specified the correct directory, and that UE4Parse is installed.")
        
        # WaccaLilyR.LILYR_ITEM_TYPES
        

    def load(self, uasset: Path, uexp: Path) -> Optional[dict]:
        provider = DefaultFileProvider([], VersionContainer(EUEVersion.GAME_UE4_19))

        package = LegacyPackageReader(
            uasset=BinaryStream(str(uasset)),
            uexp=BinaryStream(str(uexp)),
            provider=provider,
        )

        if package is None:
            self.logger.error(f"Failed to read the uasset/uexp pair at {uasset}")
            return None
        
        return package.get_dict()