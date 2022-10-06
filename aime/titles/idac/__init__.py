from aime.titles.idac.index import IDACServlet
#from aime.titles.idac.frontend import IDACFrontend
#from aime.titles.idac.importer import IDACImporter
from aime.titles.idac.const import IDACConstants

#frontend = IDACFrontend # Frotnend class
main = IDACServlet
#importer = IDACImporter # Title server factory class
uri_hosts = (f"http://idac.$h/$v/", "http://idac.$h/$v/") # allnet response
alt_uri_hosts = {}
dev_uri_hosts = (f"http://$h:$p/$v/", "http://$h:$p/$v/")
dev_alt_uri_hosts = {}
config_name = IDACConstants.CONFIG_NAME
game_code = IDACConstants.GAME_CODE