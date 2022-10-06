from aime.titles.mai2.index import Mai2Servlet
from aime.titles.mai2.frontend import Mai2Frontend
from aime.titles.mai2.importer import Mai2Importer
from aime.titles.mai2.const import Mai2Constants

frontend = Mai2Frontend # Frotnend class
main = Mai2Servlet
importer = Mai2Importer # Title server factory class
uri_hosts = (f"http://mai2.$h/$v/", "") # allnet response
alt_uri_hosts = {}
dev_uri_hosts = (f"http://$h:$p/$v/", "")
dev_alt_uri_hosts = {}
config_name = Mai2Constants.CONFIG_NAME
game_code = Mai2Constants.GAME_CODE