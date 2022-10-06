from aime.titles.ongeki.index import OngekiServlet
from aime.titles.ongeki.const import OngekiConstants

main = OngekiServlet
game_code = OngekiConstants.GAME_CODE
config_name = "ongeki.yaml"
uri_hosts = ("http://ong.$h/$v/", "")
dev_uri_hosts = ("http://$h:9005/$v/", "")
alt_uri_hosts = {}
dev_alt_uri_hosts = {}
