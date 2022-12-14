from aime.titles.idz.userdb_handler.base import IDZHandlerBase

from aime.titles.idz.userdb_handler.load_server_info import IDZHandlerLoadServerInfo1, IDZHandlerLoadServerInfo2

from aime.titles.idz.userdb_handler.load_config import IDZHandlerLoadConfigA1, IDZHandlerLoadConfigA2, IDZHandlerLoadConfigA3
from aime.titles.idz.userdb_handler.load_config import IDZHandlerLoadConfigB1, IDZHandlerLoadConfigB2

from aime.titles.idz.userdb_handler.load_top_ten import IDZHandlerLoadTopTen1, IDZHandlerLoadTopTen2
from aime.titles.idz.userdb_handler.load_top_ten import IDZHandlerLoadTopTen3, IDZHandlerLoadTopTen4

from aime.titles.idz.userdb_handler.update_story_clear_num import IDZHandlerUpdateStoryClearNum1, IDZHandlerUpdateStoryClearNum2
from aime.titles.idz.userdb_handler.update_story_clear_num import IDZHandlerUpdateStoryClearNum3, IDZHandlerUpdateStoryClearNum4

from aime.titles.idz.userdb_handler.save_expedition import IDZHandlerSaveExpedition1, IDZHandlerSaveExpedition2

from aime.titles.idz.userdb_handler.load_2on2 import IDZHandlerLoad2on21, IDZHandlerLoad2on22
from aime.titles.idz.userdb_handler.load_2on2 import IDZHandlerLoad2on23, IDZHandlerLoad2on24

from aime.titles.idz.userdb_handler.load_team_ranking import IDZHandlerLoadTeamRanking1, IDZHandlerLoadTeamRanking2
from aime.titles.idz.userdb_handler.load_team_ranking import IDZHandlerLoadTeamRanking3, IDZHandlerLoadTeamRanking4

from aime.titles.idz.userdb_handler.discover_profile import IDZHandlerDiscoverProfile1, IDZHandlerDiscoverProfile2
from aime.titles.idz.userdb_handler.discover_profile import IDZHandlerDiscoverProfile3

from aime.titles.idz.userdb_handler.lock_profile import IDZHandlerLockProfile1, IDZHandlerLockProfile2

from aime.titles.idz.userdb_handler.check_team_names import IDZHandlerCheckTeamName1, IDZHandlerCheckTeamName2

from aime.titles.idz.userdb_handler.unknown import IDZHandlerUnknown1, IDZHandlerUnknown2

from aime.titles.idz.userdb_handler.load_ghost import IDZHandlerLoadGhost1, IDZHandlerLoadGhost2

from aime.titles.idz.userdb_handler.create_profile import IDZHandlerCreateProfile1, IDZHandlerCreateProfile2
from aime.titles.idz.userdb_handler.create_profile import IDZHandlerCreateProfile3

from aime.titles.idz.userdb_handler.create_auto_team import IDZHandlerCreateAutoTeam1, IDZHandlerCreateAutoTeam2
from aime.titles.idz.userdb_handler.create_auto_team import IDZHandlerCreateAutoTeam3

from aime.titles.idz.userdb_handler.load_profile import IDZHandlerLoadProfile1, IDZHandlerLoadProfile2
from aime.titles.idz.userdb_handler.load_profile import IDZHandlerLoadProfile3, IDZHandlerLoadProfile4

from aime.titles.idz.userdb_handler.save_profile import IDZHandlerSaveProfile1, IDZHandlerSaveProfile2
from aime.titles.idz.userdb_handler.save_profile import IDZHandlerSaveProfile3, IDZHandlerSaveProfile4

from aime.titles.idz.userdb_handler.update_provisional_store_rank import IDZHandlerUpdateProvisionalStoreRank1
from aime.titles.idz.userdb_handler.update_provisional_store_rank import IDZHandlerUpdateProvisionalStoreRank2

from aime.titles.idz.userdb_handler.load_reward_table import IDZHandlerLoadRewardTable1, IDZHandlerLoadRewardTable2

from aime.titles.idz.userdb_handler.save_topic import IDZHandlerSaveTopic1, IDZHandlerSaveTopic2

__all__ = [IDZHandlerBase]

v110 = [IDZHandlerLoadServerInfo1, IDZHandlerLoadConfigA1, IDZHandlerLoadConfigB1, IDZHandlerLoadTopTen1, IDZHandlerUpdateStoryClearNum1,
IDZHandlerSaveExpedition1, IDZHandlerLoad2on21, IDZHandlerLoad2on22, IDZHandlerLoadTeamRanking1, IDZHandlerDiscoverProfile1,
IDZHandlerLockProfile1, IDZHandlerCheckTeamName1, IDZHandlerUnknown1, IDZHandlerCreateAutoTeam1, IDZHandlerCreateProfile1,
IDZHandlerLoadGhost1, IDZHandlerLoadProfile1, IDZHandlerSaveProfile1, IDZHandlerUpdateProvisionalStoreRank1, IDZHandlerLoadRewardTable1,
IDZHandlerSaveTopic1]

v130 = [IDZHandlerLoadServerInfo1, IDZHandlerLoadConfigA1, IDZHandlerLoadConfigB1, IDZHandlerLoadTopTen2, IDZHandlerUpdateStoryClearNum2,
IDZHandlerSaveExpedition2, IDZHandlerLoad2on21, IDZHandlerLoad2on22, IDZHandlerLoadTeamRanking1, IDZHandlerLoadTeamRanking3, 
IDZHandlerDiscoverProfile1, IDZHandlerLockProfile1, IDZHandlerCheckTeamName1, IDZHandlerUnknown1, IDZHandlerCreateAutoTeam1, 
IDZHandlerCreateProfile1, IDZHandlerLoadGhost1, IDZHandlerLoadProfile2, IDZHandlerSaveProfile2, IDZHandlerUpdateProvisionalStoreRank1, 
IDZHandlerLoadRewardTable1, IDZHandlerSaveTopic1]

v210 = [IDZHandlerLoadServerInfo2, IDZHandlerLoadConfigA2, IDZHandlerLoadConfigB2, IDZHandlerLoadTopTen3, IDZHandlerUpdateStoryClearNum3,
IDZHandlerSaveExpedition2, IDZHandlerLoad2on23, IDZHandlerLoad2on24, IDZHandlerLoadTeamRanking2, IDZHandlerLoadTeamRanking4,
IDZHandlerDiscoverProfile2, IDZHandlerLockProfile2, IDZHandlerCheckTeamName2, IDZHandlerUnknown2, IDZHandlerCreateAutoTeam2,
IDZHandlerCreateProfile2, IDZHandlerLoadGhost2, IDZHandlerLoadProfile3, IDZHandlerSaveProfile3, IDZHandlerUpdateProvisionalStoreRank2,
IDZHandlerLoadRewardTable2, IDZHandlerSaveTopic2]

v230 = [IDZHandlerLoadServerInfo2, IDZHandlerLoadConfigA3, IDZHandlerLoadConfigB2, IDZHandlerLoadTopTen4, IDZHandlerUpdateStoryClearNum4,
IDZHandlerSaveExpedition2, IDZHandlerLoad2on23, IDZHandlerLoad2on24, IDZHandlerLoadTeamRanking2, IDZHandlerLoadTeamRanking4, 
IDZHandlerDiscoverProfile3, IDZHandlerLockProfile2, IDZHandlerCheckTeamName2, IDZHandlerUnknown2, IDZHandlerCreateAutoTeam3,
IDZHandlerCreateProfile3, IDZHandlerLoadGhost2, IDZHandlerLoadProfile4, IDZHandlerSaveProfile4, IDZHandlerUpdateProvisionalStoreRank2,
IDZHandlerLoadRewardTable2, IDZHandlerSaveTopic2]