import socket

# port = 7197
port = 502

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect(('127.0.0.1', port))
except Exception as e:
    print("Cannot connect to the server:", e)
print("Connected")
message = b"{TLA}\r\n"


# s.sendto(message.encode('utf-16'), ('127.0.0.1', port))
s.sendto(message, ('127.0.0.1', port))
receive = s.recvfrom(1024)
print(receive)


# import minimalmodbus
# instrument = minimalmodbus.Instrument('/dev/ttyUSB1', 1)
#
# try:
#     print(instrument.read_register(30300))
# except IOError:
#     print('Failed to read from instrument')
# except ValueError:
#     print('Instrument response in invalid')


# import serial
#
# ser = serial.Serial()
# ser.port = 'COM1'
# ser.baudrate = 9600
# ser.bytesize = serial.SEVENBITS
# ser.parity = serial.PARITY_NONE
# ser.stopbits = serial.STOPBITS_ONE
# ser.timeout = 3
#
# ser.open()
#
# # device_write = ser.write(bytearray.fromhex('AA 55 00 00 07 00 12 19 00'))
# device_write = ser.write(b'R{TLA}\r\n')
# print(ser.readall())
# device_read = ser.read_until()
# print(device_read)
