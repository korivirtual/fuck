from aime.titles.idz.index import IDZServlet
#from aime.titles.idz.frontend import IDZFrontend
#from aime.titles.idz.importer import IDZImporter
from aime.titles.idz.const import IDZConstants

#frontend = IDZFrontend # Frotnend class
main = IDZServlet
#importer = IDZImporter # Title server factory class
uri_hosts = (f"", "$h:$p") # allnet response
alt_uri_hosts = {}
dev_uri_hosts = (f"", "$h:$p")
dev_alt_uri_hosts = {}
config_name = IDZConstants.CONFIG_NAME
game_code = IDZConstants.GAME_CODE