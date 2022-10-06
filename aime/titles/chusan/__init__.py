from aime.titles.chusan.index import ChusanServlet
from aime.titles.chusan.const import ChusanConstants

main = ChusanServlet
game_code = ChusanConstants.GAME_CODE
config_name = "chusan.yaml"
uri_hosts = ("http://chusan.$h/$v/", "")
dev_uri_hosts = ("http://$h:9006/$v/", "")
alt_uri_hosts = {}
dev_alt_uri_hosts = {}
