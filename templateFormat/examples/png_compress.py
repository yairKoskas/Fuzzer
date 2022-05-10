import zlib

# make a scan over the data
# return the number of bytes read and the scan data
def _scan(data: bytes, rows : int, columns : int, pixel_size : int) -> (int, bytes):
    if rows == 0 or columns == 0:
        return 0, b''

    new_data = b''
    for row in range(0, columns*pixel_size*rows, columns*pixel_size):
        new_data += b'\x00' + data[row:row + columns*pixel_size]

    return columns*pixel_size*rows, new_data

def compress_data(data: bytes, rows : int, columns : int,  pixel_size : int, interlance_mode : int) -> bytes:
    new_data = b''

    if interlance_mode == 0:
        _, new_data = _scan(data, rows, columns, pixel_size)
        
    else:
        '''
        scan order is:
            16462646
            77777777
            56565656
            77777777
            36463646
            77777777
            56565656
            77777777
        '''

        # 1st scan
        row_len = columns // 8 + (columns % 8 > 0)
        column_len = rows // 8 + (rows % 8 > 0)
        bytes_read, scan_data = _scan(data, column_len, row_len, pixel_size)
        new_data += scan_data
        data = data[bytes_read:]

        # 2nd scan
        row_len = columns // 8 + (columns % 8 > 4)
        column_len = rows // 8 + (rows % 8 > 0)
        bytes_read, scan_data = _scan(data, column_len, row_len, pixel_size)
        new_data += scan_data
        data = data[bytes_read:]

        # 3rd scan
        row_len = (columns // 8)*2 + ((columns%8-1)//4 + 1)
        column_len = rows // 8 + (rows%8 > 4)
        bytes_read, scan_data = _scan(data, column_len, row_len, pixel_size)
        new_data += scan_data
        data = data[bytes_read:]

        # 4th scan
        row_len = (columns // 8)*2 + ((columns%8-3)//4 + 1)
        column_len = (rows // 8)*2 + ((rows%8-1)//4 + 1)
        bytes_read, scan_data = _scan(data, column_len, row_len, pixel_size)
        new_data += scan_data
        data = data[bytes_read:]

        # 5th scan
        row_len = (columns // 8)*4 + ((columns%8-1)//2 + 1)
        column_len = (rows // 8)*2 + ((rows%8-3) //4 + 1)
        bytes_read, scan_data = _scan(data, column_len, row_len, pixel_size)
        new_data += scan_data
        data = data[bytes_read:]

        # 6th scan
        row_len = (columns // 8)*4 + ((columns%8-2)//2 + 1)
        column_len = (rows // 8)*4 + ((rows%8-1)//2 + 1)
        bytes_read, scan_data = _scan(data, column_len, row_len, pixel_size)
        new_data += scan_data
        data = data[bytes_read:]

        # 7th scan
        row_len = (columns // 8)*8 + (columns%8)
        column_len = (rows // 8)*4 + ((rows%8-2)//2 + 1)
        bytes_read, scan_data = _scan(data, column_len, row_len, pixel_size)
        new_data += scan_data
        data = data[bytes_read:]

    return zlib.compress(bytes(new_data))