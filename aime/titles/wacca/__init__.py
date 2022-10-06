from aime.titles.wacca.const import WaccaConstants
from aime.titles.wacca.index import WaccaServlet
from aime.titles.wacca.frontend import WaccaFrontend
from aime.titles.wacca.importer import WaccaImporter

frontend = WaccaFrontend
main = WaccaServlet
importer = WaccaImporter
game_code = WaccaConstants.GAME_CODE
config_name = WaccaConstants.CONFIG_NAME
uri_hosts = ("http://wacca.$h", "")
dev_uri_hosts = ("http://$h:9002/WaccaServlet", "")
alt_uri_hosts = {}
dev_alt_uri_hosts = {}