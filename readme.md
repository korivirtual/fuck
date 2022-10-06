# Megaime
A network service emulator for games that use SEGA's ALL.Net service.

# ! ! ! This is a Work in Progress ! ! !
At the current moment in time, this "works" in that it turns on and does the minimum to get any supported game to boot. As time progresses, more features will be added. This software is nowehere near production ready!

This project does not support N-0 releases of games and requests for those will be denied.

# Supported games
## Full support
+ Chunithm
    + Amazon
    + Amazon Plus
    + Crystal
    + Crystal Plus
    + Paradise
    + Paradise Lost
    + New

+ Ongeki
    + Summer
    + Summer Plus
    + Red
    + Red Plus
    + Bright

+ Crossbeats
    + Rev
    + Rev Sunrise S1
    + Rev Sunrise S2

+ Wacca
    + Lily R
    + Reverse

+ Maimai
    + DX
    + DX Plus
    + Splash
    + Splash Plus
    + Universe

## Partial Support (does not support all features and/or incomplete state)
+ Hatsune Miku FT Arcade (no shop support)
+ Initial D
+ Wacca
    + Base (no profile support)
    + S (no profile support)
    + Lily (no profile support)

# Setup
## Development
### Requirements
+ A non-windows OS is <b>STRONGLY</b> recomended as memcache does not work on Windows.
+ For unix OSs, libmysqlclient-dev and libmemcached-dev are required.
+ Python v3.7 or newer
+ A MySql server
+ A valid hostname (eg. example.com) that points to the machine that will be hosting the server. (optional, required for some games)
    + For development, a simple host file edit is recomended, as long as whatever hostname you provide points back to your server's IP

### Memcached Configuration (Linux only)
Under the file /etc/memcached.conf, please make sure the following parameters are set:

-I 128m
-m 1024

This is mandatory to avoid memcached overload caused by Crossbeats

### Setup guide
1. Clone this repository
2. Create a directory that will hold all of your config files, and copy all of the yaml from "config" into it. This will be the config file for your development server
3. Edit the config file with the necessassary values. You must change `server.hostname` to whatever your server's hostname is, and `aimedb.key` to the aimedb AES key. you'll need to find this yourself, but it't not hard if you know where to look.
4. Create a python virtual environment with `python -m venv .venv` and activate it. More info on virtual environments can be found [here](https://docs.python.org/3/tutorial/venv.html)
5. Install dependencies with `pip install -r requirements.txt` (or `pip install -r requirements_win.txt` if youre on Windows)
6. Create the database with `python dbutils.py create -c PATH/TO/YOUR/CONFIG/FOLDER`
7. Run the server with `python index.py -c PATH/TO/YOUR/CONFIG/FOLDER`

From here, all services should start successfully, and you should be ready to receive game requests!

## Production
### Requirements
+ All the requirements for the development section, and...
+ A non-windows OS unless you want your database to get hammered everytime somebody cards in
+ A real domain name that points clients to your box (or a VPN setup if you want to be extra)
+ Nginx or similar to proxy requests

### Setup Guide
Windows 10/11 Basic Guide : Please refer to `INSTALL_WINDOWS.md`
Ubuntu 20.04 LTS Basic Guide : Please refer to `INSTALL_UBUNTU.md`

### Thank Yous
This project would not be what it is without the hard work of a lot of very smart people. Here are some of those people in no particular order:

+ The DJHackers team
    + Creating minime
    + All the reverse engineering work and tools that made it possible for this project to exist at all
    + Cool dudes
+ Midorica
    + Chuni, Ongeki, Diva & Crossbeats support
    + General code help
    + Cool dude
+ Subject38
    + Pointing me in the right direction and helping keep my head on
    + Caching
    + General code help
    + Cool dude
+ Stepland
    + UE4 importing
    + Cool dude
+ Tarben
    + Managing the dev server
    + Cool dude
    + bear tree
+ A bunch of other people and discord servers that probably don't want their names out there
