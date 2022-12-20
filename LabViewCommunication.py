import struct


def ascii_message(text):
    if len(text) < 32:
        amount_null = 32 - len(text)
        message = text + amount_null * ' '
        message = message.encode('ascii')
        return message


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
