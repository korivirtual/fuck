import argparse, yaml
from random import choice

from aime.data import Config, Data
from aime.data.const import KeychipPlatformsCodes

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Aime service provider")
    parser.add_argument("--type", "-t", type=str, help="Type of serial to generate (keychip, mainboard)")
    parser.add_argument("--platform", "-p", type=str, help="Platform to generate for (ringedge, ringwide, nu, nusx, alls)")
    parser.add_argument("--revision", "-r", type=str, help="Hardware revision to generate for (1 - 3, depends on platform)")
    parser.add_argument("--config", "-c", type=str, help="Config folder to use", default="config")
    args = parser.parse_args()

    cfg = Config()
    cfg.update(yaml.safe_load(open(f"{args.config}/core.yaml")))
    data = Data(cfg)

    if args.type == "keychip" or args.type == "kc":
        if args.platform == "ringedge":
            id = data.arcade.generate_keychip_serial(KeychipPlatformsCodes.RING)
        elif args.platform == "ringwide":
            id = data.arcade.generate_keychip_serial(KeychipPlatformsCodes.RING)
        elif args.platform == "nu":
            id = data.arcade.generate_keychip_serial(choice(KeychipPlatformsCodes.NU))
        elif args.platform == "nusx":
            id = data.arcade.generate_keychip_serial(choice(KeychipPlatformsCodes.NUSX))
        elif args.platform == "alls":
            id = data.arcade.generate_keychip_serial(KeychipPlatformsCodes.ALLS)
        else:
            id = "Invalid platform!"
    
        print(id)
    
    else:
        print("Only keychip generation is supported for now")