import asyncio
import base64
from Socket import Socket
from os import system
from datetime import datetime
from  settings import IP_SERVER, PORT_SERVER
from user import User


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
    
    async def listen_socket(self, listened_socket: object=None):
        while True:
            data = await self.main_loop.sock_recv(self.socket, 2048)
            decode_data = base64.b64decode(data)
            
            self.messages += f"{datetime.now().date()}: {decode_data.decode('utf-8')}\n"
            system('cls')
            print(self.messages)
            
    async def send_data(self): 
        while True:
            data = await self.main_loop.run_in_executor(None, input, f"{user.user_name} >>> ")
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
    client.set_up(IP_SERVER, PORT_SERVER)

    client.start()
