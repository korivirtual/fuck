# Contributing to MegAime
Make sure to read this document, and look at examples in the codebase before starting!
## Support policy
The master branch will only support game versions that are at least a half-step down from what is currently live in arcades. PRs for newer versions will be rejected.

# Core
The MegAime core represents the bundle of services that make up the aime network. This includes Allnet auth service, Billing service, Aimedb service, the Title service (see below), and the Frontend service. The server is designed in such a way that, if you are just adding game support, you should never have to modify the core.

## Allnet
The Allnet service provides the initial cabinet network authentication, as well as providing the url of the title server that the game will use.

## Billing
The Billing service does credit management for games that use SEGA's billing service.

## AimeDB
The AimeDB service manages cards and users network-wide. Games will make contact with this service when a user cards in to get their network-wide aime id, which they usually pass onto their title servers to get the user's data. It is noteable in that unlike the other services, it is a socket server instead of an HTTP one. You must also provide the AES key used to decrypt the requests. Server owners are responsible for finding this themselves.

## Title
The Title services manages the available title servers. No actual dispatching is done via this service, it just exists to give the core a way to know that each title server is availble. See below for more details.

## Frontend
The Frontend service manages the webui, the web interface that users can use to view scores, change settings, and other functions. It is up to title server developers to make their frontends.

# Title servers
Title servers add support for games. Every title server will be it's own independant server listening on it's own port. This means title servers are responsible for their own request handling, from start to finish. No title server dispatching is done by the core.

## Structure
Every title server must be entirely located in a file in the `titles` directory, and have an `__init__.py` file that defines the following:

+ `main`
    + Title server entry point class. This class must have the following:
        + An `__init__` function that take 3 arguments: `self`, the core config as a Config object, and the directory to the config folder as a string
        + A `setup` function who's only argument is `self`, which sets up the server's twisted `endpoint`
+ `game_code`
    + String containing the game's 4 letter game code (ex. SDFE for Wacca)
+ `config_name`
    + String containing the name of the config file for the game. Should end in ".yaml"
+ `uri_hosts`
    + Tuple containing the allnet startup uri at position 0, and the allnet startup host at position 1
+ `alt_uri_hosts`
    + Dict where keys are versions and values are `uri_hosts` tuples, used when the same game has different startup uri requirements across versions
+ `dev_uri_hosts` and `dev_alt_uri_hosts`
    + Alternet startup uris to use when running in development mode
+ `frontend`
    + Title server's frontend handling class
+ `importer`
    + Title server's data import handling class

# Database
MegAime uses a common database for all games, and has several general-purpose functions to interact with the database such that a developer should never be writing actual SQL code.