# Megaime - Windows 10/11 Guide
This step-by-step guide assumes that you are using a fresh install of Windows 10/11 without MySQL installed, some of the steps can be skipped if you already have an installation with MySQL 8.0 or even some of the modules already present on your environment

# Setup
## Install Python Python 3.9 (recommended) or 3.10
1. Download Python 3.9 : https://www.python.org/ftp/python/3.9.13/python-3.9.13-amd64.exe
2. Install python-3.9.13-amd64.exe
    1. Select Customize installation
    2. Make sure that pip, tcl/tk, and the for all users are checked and hit Next
    3. Make sure that you enable "Create shortcuts for installed applications" and "Add Python to environment variables" and hit Install

## Install MySQL 8.0
1. Download MySQL 8.0 Server : https://dev.mysql.com/get/Downloads/MySQLInstaller/mysql-installer-community-8.0.29.0.msi
2. Install mysql-installer-community-8.0.29.0.msi
    1. Click on "Add ..." on the side
    2. Click on the "+" next to MySQL Servers
    3. Make sure MySQL Server 8.0.29 - X64 is under the products to be installed.
    4. Hit Next and Next once installed
    5. Select the configuration type "Development Computer"
    6. Hit Next
    7. Select "Use Legacy Authentication Method (Retain MySQL 5.x compatibility)" and hit Next
    8. Enter a root password and then hit Next >
    9. Leave everything under Windows Service as default and hit Next >
    10. Click on Execute and for it to finish and hit Next> and then Finish
3. Open MySQL 8.0 Command Line Client and login as your root user
4. Type those commands to create your user and the database
```
CREATE USER 'aime'@'localhost' IDENTIFIED WITH mysql_native_password BY 'MyStrongPass.';
GRANT ALL PRIVILEGES ON *.* TO 'aime'@'localhost'; 
CREATE DATABASE aime;
FLUSH PRIVILEGES;
exit
```

## Install Python modules
1. Change your work path to the megaime-master folder using 'cd' and install the requirements:
> pip install -r requirements_win.txt

## Adjust /config/core.yaml

1. Make sure to change both the server and title hostnames to be set to your local machine IP (ex.: 192.168.1.xxx) 
    - In case you want to run this only locally, set the following values:
```
server:
    hostname: 0.0.0.0 
title: 
    hostname: localhost
```
2. Adjust the proper MySQL information you created earlier
3. Add the AimeDB key at the bottom of the file

## Create the database tables for megaime
> python dbutils.py create

## Firewall Adjustements 
Make sure the following ports are open both on your router and local Windows firewall in case you want to use this for public use (NOT recommended):
> Port 80 (TCP), 443 (TCP), 8443 (TCP), 22345 (TCP), 9000 (TCP) to 9015 (TCP), 10000 to 10013 (UDP & TCP)

## Running the megaime instance
> python index.py

# Troubleshooting

## Game does not connect to Megaime
1. Double-check your core.yaml, the server hostname is most likely wrong

## Game does not connect to Title Server
1. Verify that your core.yaml is setup properly for both the server hostname and title hostname (usually set to 0.0.0.0 and 192.168.x.x)
2. Boot your game and verify that an AllNet response does show and if it does, attempt to open the URI that is shown under a browser such as Edge, Chrome & Firefox.
3. If a white page is shown, the server is working properly and if it doesn't, double check your port forwarding and also that you have entered the proper local IP under the Title hostname in core.yaml.

## Unhandled command under AimeDB
1. Double check your AimeDB key under core.yaml, it is incorrect.

## AttributeError: module 'collections' has no attribute 'Hashable'
1. This means the pyYAML module is obsolete, simply make sure to update pip and then reinstall the requirements
    - Change your work path to the megaime-master folder using 'cd' and run the following commands:
```
python -m pip install --upgrade pip
pip install -r requirements_win.txt
```
