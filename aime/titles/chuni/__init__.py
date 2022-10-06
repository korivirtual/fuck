from aime.titles.chuni.index import ChuniServlet
from aime.titles.chuni.const import ChuniConstants

main = ChuniServlet
game_code = ChuniConstants.GAME_CODE
config_name = "chuni.yaml"
uri_hosts = ("http://chuni.$h/$v/", "")
dev_uri_hosts = ("http://$h:9001/$v/", "")
alt_uri_hosts = {}
dev_alt_uri_hosts = {}