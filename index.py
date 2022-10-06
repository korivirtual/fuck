import yaml
import argparse

from twisted.web import server
from twisted.internet import reactor, endpoints

from aime.data import Config
from aime import Allnet, Billing, AimedbFactory, Title, Frontend

if __name__=='__main__':
    parser = argparse.ArgumentParser(description="Aime service provider")
    parser.add_argument("--config", "-c", type=str, help="Config directory to use", default="config")
    args = parser.parse_args()

    core_cfg = Config()
    core_cfg.update(yaml.safe_load(open(f"{args.config}/core.yaml")))

    if core_cfg.server.develop:
        print("Starting server in development mode")
    else:
        print("Starting server in production mode")

    endpoints.serverFromString(reactor, f"tcp:80:interface={core_cfg.server.hostname}").listen(server.Site(Allnet(core_cfg, args.config)))
    endpoints.serverFromString(reactor, f"ssl:8443:interface={core_cfg.server.hostname}:privateKey={core_cfg.billing.ssl_key}:certKey={core_cfg.billing.ssl_cert}").listen(server.Site(Billing(core_cfg)))
    endpoints.serverFromString(reactor, f"tcp:22345:interface={core_cfg.server.hostname}").listen(AimedbFactory(core_cfg))
    if core_cfg.frontend.enable:
        endpoints.serverFromString(reactor, f"tcp:{core_cfg.frontend.port}:interface={core_cfg.server.hostname}").listen(server.Site(Frontend(core_cfg, args.config)))
    title = Title(core_cfg, args.config)
    title.loadAndRun()
    reactor.run()