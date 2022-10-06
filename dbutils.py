import yaml
import argparse
from aime.data import Config, Data
from aime.data.const import KeychipPlatformsCodes, MainboardPlatformCodes, MainboardRevisions

if __name__=='__main__':
    parser = argparse.ArgumentParser(description="Database utilities")
    parser.add_argument("--config", "-c", type=str, help="Config folder to use", default="config")
    parser.add_argument("--version", "-v", type=str, help="Version of the database to upgrade/rollback to")
    parser.add_argument("action", type=str, help="DB Action, create, recreate, upgrade, or rollback")
    args = parser.parse_args()

    cfg = Config()
    cfg.update(yaml.safe_load(open(f"{args.config}/core.yaml")))
    data = Data(cfg)

    if args.action == "create":
        data.create_database()
        
    elif args.action == "recreate":
        data.recreate_database()

    elif args.action == "migrate":
        if args.version is None:
            print("Must set version to migrate to")
        else:
            data.migrate_database(int(args.version))
    
    elif args.action == "generate":
        pass
