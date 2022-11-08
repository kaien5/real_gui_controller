import codecs
import socket
import base64
import struct

# The IP address and port
from matplotlib import pyplot as plt

IP = '127.0.0.1'
port = 7197

# Establishing connection
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.connect((IP, port))
        print("Connection is established\n")
    except Exception as e:
        print("Cannot connect to the server:", e)

    # Message to receive latest measurement timestamp
    message = "R{TLA}\r\n".encode('utf-8')

    # Send and receive message
    s.sendto(message, (IP, port))
    receive, adr = s.recvfrom(4096)

    # Message that is received will have to be decoded, sliced and stitched in order for retrieval command
    time_stamp = receive[6:27].decode('utf-8')
    message_slice = time_stamp[:3] + time_stamp[4:6] + time_stamp[7:11] + '_' + time_stamp[12:14] + time_stamp[15:17] + time_stamp[18:21]
    message2 = "R{CD3," + message_slice + "}\r\n"
    message2 = message2.encode('utf-8')

    # Send message to receive payload from last measurement taken
    s.sendto(message2, (IP, port))
    receive, adr = s.recvfrom(4096)

    # Defining the payload
    payload = receive[7:-1]
    # print(f'Length {len(payload)} : {payload}')

    def bxor(b1):
        result = []
        for _ in b1:
            result.append(_ ^ 0x53A9)
            # result += _ ^ 0x53A9
        return result

    data = bxor(payload)
    print(len(data))


    # Decoding from base64 to bytes
    decoded = base64.decodebytes(payload)
    print(f'Length {len(decoded)} : {decoded}\n')

    # Size of the lookup table
    size = struct.unpack('>H', decoded[:2])[0]  # Not sure about the 'H' unpacking
    print(f'The size of the lookup table is: {size}')
    print(int.from_bytes(b'\x01\x02', byteorder='little'))

    # The lookup table
    lookup_table = decoded[2: 2 + size * 4]
    print(f'Lookup_table: {lookup_table}')
    print(f'With byte length: {len(lookup_table)}\n')

    # The list of references
    list_of_references = decoded[2 + size * 4:]
    print(f'List of reference: {list_of_references}')
    print(f'With byte length: {len(list_of_references)}\n')

    with open('file1.txt', 'wb') as f:
        f.write(lookup_table)

    # Decoding the lookup table to integers
    data = {'decodeString': '!' + ('HH' * size)}
    data2 = struct.unpack(data['decodeString'], lookup_table)
    print(data2)

    data = []
    for _ in list_of_references:
        data.append(_)
    print(data)

    plt.plot(data)
    plt.show()

#     # Rory's suggestion:
#     # i = b"0f45"
#     # print(int(i, 16))
#
# """This is working for communication through modbus"""
# from pymodbus.client.sync import ModbusTcpClient
#
# IP = '127.0.0.1'
# PORT = '502'
# client = ModbusTcpClient(host=IP, port=PORT)
# client.connect()
# print(client.is_socket_open())
#
# # This function will select the sequence to run and start as well
# client.write_register(0x9C41, 0x0004)
# client.write_register(0x9D08, 0x0001)

# This function will start a sequence method
# client.write_coil(0x044C, 0x01)
