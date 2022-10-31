import socket

IP = '127.0.0.1'
# IP = '145.76.121.84'
# IP = 'localhost'
port = 7197
# port = 502

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    try:
        s.connect((IP, port))
        # s.bind((IP, port))
        print("Connected")
    except Exception as e:
        print("Cannot connect to the server:", e)

    # s.connect((IP, port))
    message = "R{TLA}\r\n"
    message = message.encode('utf-8')
    print(message)

    # s.sendto(message.encode('utf-8'), (IP, port))
    s.sendto(message, (IP, port))

    receive, adr = s.recvfrom(4096)
    print(receive)

# """This is working for communication through modbus"""
# from pymodbus.client.sync import ModbusTcpClient
#
# IP = '127.0.0.1'
# PORT = '502'
# client = ModbusTcpClient(host=IP, port=PORT)
# client.connect()
# print(client.is_socket_open())
#
# register = 0x03E8
# client.write_coil(register, 5)
# client.write_coil(0x044C, 1)
