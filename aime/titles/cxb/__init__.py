from aime.titles.cxb.index import CxbServlet
from aime.titles.cxb.const import CxbConstants

main = CxbServlet
game_code = CxbConstants.GAME_CODE
config_name = CxbConstants.CONFIG_NAME
uri_hosts = (f"https://$h/cxb/$v/", "")
dev_uri_hosts = (f"https://$h/", "")
alt_uri_hosts = {}
dev_alt_uri_hosts = {}