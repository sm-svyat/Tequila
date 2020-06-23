# Tequila
Messenger

Client-server application based on sockets.

Functionality: registration, contacts, support for group chat, etc.

The application is adapted to work on a PC with Microsoft Windows and Linux systems.

## Installation
```sh
virtualenv -p python3 tquila_env
source tquila_env/bin/activate
pip install -r requirments.txt
```

## Start server
```sh
cd serer
python start_server.py
```

## Start client
```sh
cd client
python start_client.py
```
