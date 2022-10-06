from aime.titles.diva.index import DivaServlet
from aime.titles.diva.const import DivaConstants

main = DivaServlet
game_code = DivaConstants.GAME_CODE
config_name = "diva.yaml"
uri_hosts = ("http://diva.$h/$v/", "")
dev_uri_hosts = ("http://$h:9007/$v/", "")
alt_uri_hosts = {}
dev_alt_uri_hosts = {}