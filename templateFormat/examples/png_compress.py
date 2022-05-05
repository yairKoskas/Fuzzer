import zlib


def compress_data(data: bytes, row_len) -> bytes:
    new_data = b''
    for row in range(0, len(data), row_len):
        new_data += b'\x00' + data[row:row + row_len]
    return zlib.compress(bytes(new_data))