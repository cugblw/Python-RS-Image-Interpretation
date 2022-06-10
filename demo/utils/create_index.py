import struct

def write_index_header():
    start_zoom = 10
    end_room = 18
    # bin8 = lambda x : ''.join(reversed( [str((x >> i) & 1) for i in range(8)] ) )
    
    # header，依次为start_zoom, end_zoom, 预留2个字节，默认值为0
    header = [start_zoom, end_room,0,0]
    packed_header = map(lambda i: struct.pack("@b", i), header)
    
    with open('test.idx', 'wb') as f:
        for i in packed_header:
            f.write(i)
        # f.write(bin_array)
    f.close()


    # print(bin8(0))
    # pass

def write_index_data():
    s = "0000000010000000000000001111111111110000100000001111111111111111"
    i = 0
    buffer = bytearray()
    while i < len(s):
        buffer.append( int(s[i:i+8], 2) )
        i += 8

    # now write your buffer to a file
    with open('test.idx', 'ab+') as f:
        f.write(buffer)
    
    # write reserve buffer
    reserve_length = len(buffer)
    write_index_reserve(reserve_length)
    f.close()

def write_index_reserve(reserve_length):
    reserve_bits = '00000000'
    reverse_buffer = bytearray()
    for i in range(reserve_length):
        reverse_buffer.append(int(reserve_bits, 2))
    with open('test.idx', 'ab+') as f:
        f.write(reverse_buffer)
    f.close()

def read_index_header():
    with open('test.idx', 'rb') as f:
        data = f.read()
        header = data[0:4]
        header_list = struct.unpack("@4b", header)
    f.close()
    return header_list

def read_index_data():
    with open('test.idx', 'rb') as f:
        # data_length = int(len(f.read()[4:])/2)
        data_reserve = f.read()[4:]
        data_length = int(len(data_reserve)/2)
        data = data_reserve[0:data_length]
        # print(data)
        # for i in range(data_length):
        #     print(bin(data[i])[2:].zfill(8))

        data_list = struct.unpack("@"+str(data_length)+"b", data)
    f.close()
    return data_list


if __name__ == '__main__':
    write_index_header()
    write_index_data()
    read_index_header()
    print(read_index_data())