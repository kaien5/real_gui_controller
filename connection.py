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
    print(receive)
    message_slice = time_stamp[:3] + time_stamp[4:6] + time_stamp[7:11] + '_' + time_stamp[12:14] + time_stamp[15:17] + time_stamp[18:21]
    message2 = "R{CD1," + message_slice + "}\r\n"
    message2 = message2.encode('utf-8')

    # Send message to receive payload from last measurement taken
    s.sendto(message2, (IP, port))
    receive, adr = s.recvfrom(4096)
    print(receive)

    # Defining the payload
    payload = receive[7:-1]
    # print(f'Length {len(payload)} : {payload}')

    # Step 1: Base64 decoding
    decoded = base64.decodebytes(payload)
    print(f'Length {len(decoded)} : {decoded}\n')

    # Size of the lookup table
    size = struct.unpack('!H', decoded[:2])[0]  # Not sure about the 'H' unpacking
    print(f'The size of the lookup table is: {size}')

    # Step 2: Decompression
    # The lookup table
    lookup_table = decoded[2: 2 + size * 4]
    print(f'Lookup_table: {lookup_table}')
    print(f'With byte length: {len(lookup_table)}\n')

    # Decoding the lookup table to integers
    decode_string = {'decodeString': '!' + (str(size) + 'i')}
    lookup_table = struct.unpack(decode_string['decodeString'], lookup_table)

    # The list of references
    list_of_references = decoded[2 + size * 4:]
    print(f'List of reference: {list_of_references}')
    print(f'With byte length: {len(list_of_references)}\n')

    # Decoding the list of references
    decode_string2 = {'decodeString': '!' + (str(int(len(list_of_references)/2)) + 'H')}
    list_of_references = struct.unpack(decode_string2['decodeString'], list_of_references)
    print(list(list_of_references))

    decompressed_value = [lookup_table[x] for x in list_of_references]

    # Step 3: Integration
    for _ in range(len(decompressed_value)):
        if _ > 0:
            decompressed_value[_] = decompressed_value[_] + decompressed_value[_ - 1]

    # Step 4: convert to physical values
    integrated_value = decompressed_value
    chromatogram_value = [x * 0.0001 for x in integrated_value]

    # Plotting the chromatogram_value
    plt.plot(chromatogram_value)
    plt.show()

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
#
# This function will start a sequence method
# client.write_coil(0x044C, 0x01)
