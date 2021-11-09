import os
from socket import gethostname 

# Настройки сервера
IP_SERVER = gethostname()

# Настройки json
DIR = os.path.dirname(os.path.abspath(__file__))
USERS_JSON = f"{DIR}/data/users.json"
SERVERS_JSON = f"{DIR}/data/servers.json"
