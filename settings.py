import os
from socket import gethostname 

# Настройки сервера
IP_SERVER = gethostname()
PORT_SERVER = 4141

# Настройки json
DIR = os.path.dirname(os.path.abspath(__file__))
USERS_JSON = f"{DIR}/data/users.json"