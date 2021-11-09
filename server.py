import asyncio
from Socket import Socket
from  settings import IP_SERVER, SERVERS_JSON
from module_for_json import *

class Server(Socket):
    def __init__(self, port_server):
        super(Server, self).__init__()
        self.clients = []
        self.port_server = port_server

    def set_up(self, ip: str, port: int):
        self.socket.bind((ip, port))
        self.socket.listen()

        self.socket.setblocking(False)

    def add_to_json(self):
        """Добавление нового сервера в json"""
        data = read_json_file(SERVERS_JSON)
        if self.port_server not in data:
            data.append({"Название сервера": 'Свободный порт',
                         "Порт": self.port_server,
                         "Пароль": ''})
            write_json_file(SERVERS_JSON, data)
        else:
            return data
    
    async def send_data(self, data: str):
        for client in self.clients: await self.main_loop.sock_sendall(client, data)

    async def listen_socket(self, listened_socket: object=None):
        while True:
            try:
                data = await self.main_loop.sock_recv(listened_socket, 2048)
                print(data)
                await self.send_data(data)
            except ConnectionResetError:
                self.clients.remove(listened_socket)
                print("Client is gone...")
                return

    async def accept_sockets(self):
        while True:
            client_socket, address = await self.main_loop.sock_accept(self.socket)

            data = read_json_file(SERVERS_JSON)

            if len(self.clients) <= 4:
                self.clients.append(client_socket)
                print(f"{address[1]} connected")
            else:
                print("Пошел нахуй!")
                client_socket.close()
            
            self.main_loop.create_task(self.listen_socket(client_socket))

    async def main(self):
        await self.main_loop.create_task(self.accept_sockets())

if __name__ == "__main__":
    port_server = int(input('Введите порт для сервера:\n'))

    server = Server(port_server)
    server.add_to_json()
    server.set_up(IP_SERVER, port_server)

    server.start()
