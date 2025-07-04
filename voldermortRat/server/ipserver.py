import socket

s = socket.socket()
s.bind(("0.0.0.0", 5555))
s.listen(1)
print("[*] Serving Kali IP to clients on port 5555...")

while True:
    conn, addr = s.accept()
    conn.send(addr[0].encode())
    conn.close()
