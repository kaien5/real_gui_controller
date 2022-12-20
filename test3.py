# from matplotlib.widgets import RectangleSelector
# import matplotlib.pyplot as plt
#
#
# # Function to be executed after selection
# def onselect_function(eclick, erelease):
#     # Obtain (xmin, xmax, ymin, ymax) values
#     # for rectangle selector box using extent attribute.
#     extent = rect_selector.extents
#     print("Extents: ", extent)
#
#     # Zoom the selected part
#     # Set xlim range for plot as xmin to xmax
#     # of rectangle selector box.
#     plt.xlim(extent[0], extent[1])
#
#     # Set ylim range for plot as ymin to ymax
#     # of rectangle selector box.
#     plt.ylim(extent[2], extent[3])
#
#
# # plot a line graph for data n
# fig, ax = plt.subplots()
# n = [4, 5, 6, 10, 12, 15, 20, 23, 24, 19]
# ax.plot(n)
#
# # Define a RectangleSelector at given axes ax.
# # It calls a function named 'onselect_function'
# # when the selection is completed.
# # Rectangular box is drawn to show the selected region.
# # Only left mouse button is allowed for doing selection.
# rect_selector = RectangleSelector(
#     ax, onselect_function, drawtype='box', button=[1])
#
# # Display graph
# plt.show()
import struct


def ascii_message(text):
    if len(text) < 32:
        amount_null = 32 - len(text)
        message = text + amount_null * ' '
        message = message.encode('ascii')
        return message
    else:
        print('The text is too long, maximum of 32 characters')


# For more information on what format to use in pack: https://docs.python.org/3/library/struct.html
def pack_payload(value):
    """
    Packing the value to the corresponding bytes type and size
    """
    if isinstance(value, float):
        value = struct.pack('!d', value)
    elif isinstance(value, int):
        value = struct.pack('!i', value)
    elif isinstance(value, bool):
        value = struct.pack('!?', value)
    return value


def unpack_payload(value, sort):
    """
    Unpacking the byte(s) to their corresponding value
    """
    if isinstance(sort, float):
        value = struct.unpack('!d', value)
    elif isinstance(sort, int):
        value = struct.unpack('!i', value)
    elif isinstance(sort, bool):
        value = struct.unpack('!?', value)
    return value


indicator = 'SCAN'
command = 'START'
payload = 1022.2

print(indicator)
print(command)
print(payload, '\n')

indicator_message = ascii_message(indicator)
command_message = ascii_message(command)
payload_message = pack_payload(payload)

print(indicator_message)
print(command_message)
print(payload_message, '\n')

message = indicator_message + command_message + payload_message

labview_indicator = message[:32].decode('ascii')
labview_command = message[32:64].decode('ascii')
labview_payload = unpack_payload(message[64:], payload)

print(labview_indicator)
print(labview_command)
print(labview_payload[0])
