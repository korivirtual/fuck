from aime.titles.maimai.index import MaimaiServlet
from aime.titles.maimai.const import MaimaiConstants

main = MaimaiServlet
game_code = MaimaiConstants.GAME_CODE
config_name = "maimai.yaml"
uri_hosts = ("http://mai.$h/", "mai.$h")
dev_uri_hosts = ("http://$h:$p/", "$h")
alt_uri_hosts = {}
dev_alt_uri_hosts = {}