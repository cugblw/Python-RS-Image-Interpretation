from operator import index
import os
import re
import struct

def write_index_header(start_zoom,end_room,index_file):
    # start_zoom = 10
    # end_room = 18
    # bin8 = lambda x : ''.join(reversed( [str((x >> i) & 1) for i in range(8)] ) )
    
    # header，依次为start_zoom, end_zoom, 预留2个字节，默认值为0
    header = [start_zoom, end_room, 0, 0]
    packed_header = map(lambda i: struct.pack("@b", i), header)
    
    with open(index_file, 'wb') as f:
        for i in packed_header:
            f.write(i)
        # f.write(bin_array)
    f.close()
    # print(bin8(0))

def write_index_data(bits_chain,index_file):
    # s = "0000000010000000000000001111111111110000100000001111111111111111"
    i = 0
    buffer = bytearray()
    while i < len(bits_chain):
        buffer.append( int(bits_chain[i:i+8], 2) )
        i += 8

    # now write your buffer to a file
    with open(index_file, 'ab+') as f:
        f.write(buffer)
    
    # write reserve buffer
    reserve_length = len(buffer)
    write_index_reserve(reserve_length,index_file)
    f.close()

def write_index_reserve(reserve_length,index_file):
    reserve_bits = '00000000'
    reverse_buffer = bytearray()
    for i in range(reserve_length):
        reverse_buffer.append(int(reserve_bits, 2))
    with open(index_file, 'ab+') as f:
        f.write(reverse_buffer)
    f.close()

def read_index_header(index_file):
    with open(index_file, 'rb') as f:
        data = f.read()
        header = data[0:4]
        header_list = struct.unpack("@4b", header)
    f.close()
    return header_list

def read_index_data(index_file):
    with open(index_file, 'rb') as f:
        # data_length = int(len(f.read()[4:])/2)
        data_reserve = f.read()[4:]
        data_length = int(len(data_reserve)/2)
        data = data_reserve[0:data_length]
        data_bits_list= []
        for i in range(data_length):
            # print(bin(data[i])[2:].zfill(8))
            data_bits_list.append(bin(data[i])[2:].zfill(8))

        data_list = struct.unpack("@"+str(data_length)+"b", data)
    f.close()
    return data
    return "".join(data_bits_list)

def fill_bits(bits):
    # s = "10"
    #左侧补足8位
    # bits = bits.zfill(8)
    
    #右侧补足8位
    bits = bits.ljust(8, '0')
    return bits

def concatenate_bits_chain(bits_chain):
    """将bits_chain连接起来"""
    # bits_chain = '1111110011001'
    bits_0 = fill_bits(bits_chain[0])
    bits_1 = fill_bits("".join(bits_chain[1:5]))
    bits_2 = "".join(bits_chain[5:])
    # print(bits_0, bits_1, bits_2)
    return bits_0+bits_1+bits_2

def remove_invalid_bits(bits_chain):
    """移除无效的bits，同时返回新的end_zoom"""
    start_zoom = 10
    if len(bits_chain) <= sum_bits_length(4,0,4):
        return bits_chain, start_zoom+4
    elif bits_chain[sum_bits_length(4,0,4):sum_bits_length(4,0,5)] == '0'*cal_bits_length(4,5):
        return bits_chain[0:sum_bits_length(4,0,4)], start_zoom+5
    elif bits_chain[sum_bits_length(4,0,5):sum_bits_length(4,0,6)] == '0'*cal_bits_length(4,6):
        return bits_chain[0:sum_bits_length(4,0,5)], start_zoom+5
    elif bits_chain[sum_bits_length(4,0,6):sum_bits_length(4,0,7)] == '0'*cal_bits_length(4,7):
        return bits_chain[0:sum_bits_length(4,0,6)], start_zoom+5
    elif bits_chain[sum_bits_length(4,0,7):sum_bits_length(4,0,8)] == '0'*cal_bits_length(4,8):
        return bits_chain[0:sum_bits_length(4,0,7)], start_zoom+5
    else:
        return bits_chain, start_zoom+8

def cal_bits_length(num,n):
    return num**n

def sum_bits_length(num,start,end):
    if start > end:
        return 0
    return num**start+sum_bits_length(num,start+1,end)


if __name__ == '__main__':
    # write_index_header()
    # write_index_data()
    # read_index_header()
    # read_index_data()
    # print(fill_bits("10"))

    # start_zoom = 10
    # end_zoom = 18
    # index_file = 'test.idx'
    # # index_file = r'C:\Users\Administrator\Desktop\tile_index\satellite\index\10_806_401.idx'
    # bits_chain = "11101" + "1"*16 + '1'*64+'1'*128+'0'*128 + '0'*1024

    # # print(bits_chain)
    # bits_chain,end_zoom_new = remove_invalid_bits(bits_chain)
    # # print(bits_chain,end_zoom_new)
    # bits_chain_full = concatenate_bits_chain(bits_chain)
    # print(bits_chain_full)
    # print(len(bits_chain))
    # print(len(bits_chain_full))
    # if os.path.exists(index_file):
    #     os.remove(index_file)
    # write_index_header(start_zoom,end_zoom_new,index_file)
    # write_index_data(bits_chain_full,index_file)
    # print(read_index_header(index_file))
    # index_data = read_index_data(index_file)
    # print(len(index_data))
    # print(bin(index_data[0])[2:].zfill(8))
    # print(sum_bits_length(4,0,4))


    index_file = r'C:\Users\Administrator\Desktop\tile_index\satellite\index\10_806_401.idx'
    print(read_index_header(index_file))
    index_data = read_index_data(index_file)
    print(len(index_data))
    bits_chain = []
    for i in range(len(index_data)):
        # print(bin(index_data[i])[2:].zfill(8))
        bits_chain.append(bin(index_data[i])[2:].zfill(8))
    bits_chain = "".join(bits_chain)
    print(bits_chain)
    # print(bin(index_data[0])[2:].zfill(8))

    # # print(206545-int(206545/256)*256)
    # # print(102863-int(102863/256)*256)
    # print(sum_bits_length(4,0,6))


    