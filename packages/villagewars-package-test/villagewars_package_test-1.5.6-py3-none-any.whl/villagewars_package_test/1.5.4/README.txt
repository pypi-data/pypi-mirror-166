Welcome to VillageWars!

Here's some info on how to play this game successfully.

First, you need to install python at https://www.python.org/ftp/python/3.10.6/python-3.10.6-amd64.exe
If python is already installed, move on.

VillageWars needs certain third-party modules for python including pygame and pyautougi.
Run these commands in the Command Prompt the first time you play:

py -m pip install pygame
py -m pip install pyautogui

Last of all, when running the server for VillageWars, the computer has to access and give information through port 5555. If you can customize your firewall to let this port be used by python, then great. Otherwise you'll have to turn off the firewall temporarily while running the server.

You should be good to go!

Open /src with file explorer.
Double-click on VillageWarsServer.py to start the server. The server only needs to be run on one computer.
To play the game, double-click on VillageWarsClient.py.