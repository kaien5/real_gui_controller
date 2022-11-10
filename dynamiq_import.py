import base64
import socket
import struct
from os import getcwd

import pandas as pd


class DynamiQImport:
    def load(self, ip=None, port=None):
        ip = '127.0.0.1'
        port = 7197
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((ip, port))
            except Exception as e:
                print("Cannot connect to the server:", e)

            # Message to receive latest measurement timestamp
            message = "R{TLA}\r\n".encode('utf-8')

            # Send and receive message
            s.sendto(message, (ip, port))
            receive, adr = s.recvfrom(4096)

            # Message that is received will have to be decoded, sliced and stitched in order for retrieval command
            time_stamp = receive[6:27].decode('utf-8')
            message_slice = time_stamp[:3] + time_stamp[4:6] + time_stamp[7:11] + '_' + time_stamp[12:14] + time_stamp[15:17] + time_stamp[18:21]
            for i in range(1, 4):
                message2 = "R{CD" + str(i) + "," + message_slice + "}\r\n"
                message2 = message2.encode('utf-8')

                # Send message to receive payload from last measurement taken
                s.sendto(message2, (ip, port))
                receive, adr = s.recvfrom(64000)

                # Defining the payload
                payload = receive[7:-4]
                # print(f'Length {len(payload)} : {payload}')

                # Step 1: Base64 decoding
                decoded = base64.decodebytes(payload)

                # Size of the lookup table
                size = struct.unpack('!H', decoded[:2])[0]

                # Step 2: Decompression
                # The lookup table
                lookup_table = decoded[2: 2 + size * 4]

                # Decoding the lookup table to integers
                decode_string = {'decodeString': '!' + (str(size) + 'i')}
                lookup_table = struct.unpack(decode_string['decodeString'], lookup_table)

                # The list of references
                list_of_references = decoded[2 + size * 4:-2]

                # Decoding the list of references
                decode_string2 = {'decodeString': '!' + (str(int(len(list_of_references) / 2)) + 'H')}
                list_of_references = struct.unpack(decode_string2['decodeString'], list_of_references)

                decompressed_value = [lookup_table[x] for x in list_of_references]

                # Step 3: Integration
                for _ in range(len(decompressed_value)):
                    if _ > 0:
                        decompressed_value[_] = decompressed_value[_] + decompressed_value[_ - 1]

                # Step 4: convert to physical values
                integrated_value = decompressed_value
                if i == 1:
                    chromatogram1 = [round(x * 0.0001, 4) for x in integrated_value]
                if i == 2:
                    chromatogram2 = [round(x * 0.0001, 4) for x in integrated_value]
                if i == 3:
                    chromatogram3 = [round(x * 0.0001, 4) for x in integrated_value]

                # Retrieving the timescale
                time_value = []
                for t in range(len(chromatogram1)):
                    time_value.append(t / 100)

            filename = getcwd() + '\\' + str(message_slice[1:-1]) + '.txt'
            df = pd.DataFrame({'Time(s)': time_value, 'Ch1 (FF)': chromatogram1, 'Ch2 (FF)': chromatogram2, 'Ch3 (BF)': chromatogram3})
            df.to_csv(filename, sep='\t', index=False)

        return filename
