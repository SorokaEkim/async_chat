import asyncio
import base64
from Socket import Socket
from os import system
from datetime import datetime
from  settings import IP_SERVER, SERVERS_JSON
from user import User
from module_for_json import *

class Client(Socket):
    def __init__ (self, user: object):
        super(Client, self).__init__()
        self.messages = ""
        self.user = user
    
    def set_up(self, ip: str, port: int):
        try:
            self.socket.connect((ip, port))
        except ConnectionRefusedError:
            print("Server is not online right now :(")
            exit(0)
        else:
            self.socket.setblocking(False)
    
    def show_list_empty_servers (self):
        data = read_json_file(SERVERS_JSON)
        print("Список свободных портов")
        for server_hash in data:
            if server_hash['Название сервера'] == "Свободный порт":
                print(f"{server_hash['Название сервера']}: {server_hash['Порт']}")

    def show_list_servers(self):
        print("Выберите чат для подключения:")
        data = read_json_file(SERVERS_JSON)
        for server_hash in data:
            if server_hash['Название сервера'] != "Свободный порт":
                print(f"{server_hash['Название сервера']}: {server_hash['Порт']}")
    
    def show_free_server(self):
        data = read_json_file(SERVERS_JSON)
        for server_hash in data:
            for server_hash in data:
                if server_hash["Пароль"] == '':
                    print(f"{server_hash['Название сервера']}: {server_hash['Порт']}")
    
    def check_password(self, port_server, password_server):
        data = read_json_file(SERVERS_JSON)
        for server_hash in data:
            if port_server == server_hash["Порт"]:
                if password_server == server_hash['Пароль']:
                    print("Вы успешно вошли в чат")
                else:
                    print("Пароль неверный")
                    exit(0)

    def create_chat(self, name_server, password_server, port_server):
        data = read_json_file(SERVERS_JSON)
        for server_hash in data:
            if server_hash['Порт'] == port_server:
               server_hash['Название сервера'] = name_server 
               server_hash['Пароль'] = password_server
               write_json_file(SERVERS_JSON, data)

    async def listen_socket(self, listened_socket: object=None):
        while True:
            data = await self.main_loop.sock_recv(self.socket, 2048)
            decode_data = base64.b64decode(data)
            
            self.messages += f"{datetime.now().date()}: {decode_data.decode('utf-8')}\n"
            system('cls')
            print(self.messages)
            
    async def send_data(self): 
        while True:
            data = await self.main_loop.run_in_executor(None, input, f">>>")
            encode_data = base64.b64encode(data.encode("UTF-8"))
            
            await  self.main_loop.sock_sendall(self.socket, encode_data)

    async def main(self):
        await asyncio.gather(
            self.main_loop.create_task(self.listen_socket()),
            self.main_loop.create_task(self.send_data())
        )

if __name__ == "__main__":

    User.get_all_users()

    choice = int(input("Здраствуйте!\nЯ новый пользователь ==> введите 1\
                       \nЯ старый пользователь ==> ввведите 2\n"))
    actions = {
        1: User,
        2: User.user_authorization
    }
    
    user_name = input("Введите имя пользователя\n")
    user_password = input("Введите пароль\n")
    user = actions[choice]({'username':user_name, 'password': user_password})
    user.add_new_user()
    
    print(f"Добро пожаловать {user.user_name}")
    
    client = Client(user)

    choice = int(input("1. Создать чат комнату\
                      \n2. Подключиться чату\
                      \n3. Подключится к чату со свободным доступом\
                      \n4. Создать чат со свободным доступом"))
    
    if choice == 1:
        client.show_list_empty_servers()
        port_server = int(input("Введите порт\n"))
        name_server = input("Введите название чата\n")
        password_server = input("Введите пароль для чата\n")
        client.create_chat(name_server, password_server, port_server)
    elif choice == 2:
        client.show_list_servers()
        port_server = int(input("Введите порт\n"))
        password_server = input("Введите пароль\n")
        client.check_password(port_server, password_server)
    elif choice == 3:
        client.show_free_server()
        port_server = int(input("Введите порт\n"))
    elif choice == 4:
        client.show_list_empty_servers()
        port_server = int(input("Введите порт\n"))
        name_server = input("Введите название чата\n")
        client.create_chat(name_server, '', port_server)

    client.set_up(IP_SERVER, port_server)
    client.start()
    