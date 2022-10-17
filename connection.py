import socket

host = socket.gethostbyname(socket.gethostname())
print(host)
port = 7197

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect((host, port))
except Exception as e:
    print("Cannot connect to the server:", e)
print("Connected")

s.sendto(b'TLA', (host, port))
print(s.recvfrom(1024))
