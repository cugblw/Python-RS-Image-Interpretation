# -*- encoding: utf-8 -*-

'''
@File    :   merge_index_files.py
@Time    :   2022/06/20 03:56:31
@Author  :   Lee
@Version :   1.0
@License :   (C)Copyright Cennavi, Li Wei
@Desc    :   None
'''


from operator import index
import os
import shutil
import build_index_structure as bis

def merge_index_files(index_dir_less, index_dir_more):
    """
    合并索引文件
    """
    # get all index_id list
    index_files_less = os.listdir(index_dir_less)
    index_files_more = os.listdir(index_dir_more)

    for index_file in index_files_less:
        if index_file in index_files_more:
            index_header_less = bis.read_index_header(os.path.join(index_dir_less, index_file))
            index_header_more = bis.read_index_header(os.path.join(index_dir_more, index_file))

            index_header_new = (0,0,0,0)
            if index_header_less[1] >= index_header_more[1]:
                index_header_new = index_header_less

                index_data_less = bis.read_index_data(os.path.join(index_dir_less, index_file))
                index_data_more = bis.read_index_data(os.path.join(index_dir_more, index_file))
                
                index_data_less_bits_chain = []
                index_data_more_bits_chain = []
                index_data_new_bits_chain = []
                    # bits_chain = []
                for i in range(len(index_data_less)):
                    # print(index_data[i])
                    # print(bin(index_data[i])[2:].zfill(8))
                    index_data_less_bits_chain.append(bin(index_data_less[i])[2:].zfill(8))
                index_data_less_bits_chain = "".join(index_data_less_bits_chain)
                # print(len(index_data_less_bits_chain))

                for j in range(len(index_data_more)):
                    # print(index_data[i])
                    # print(bin(index_data[i])[2:].zfill(8))
                    index_data_more_bits_chain.append(bin(index_data_more[j])[2:].zfill(8))
                index_data_more_bits_chain = "".join(index_data_more_bits_chain)
                # print(len(index_data_more_bits_chain))

                for i in range(len(index_data_less_bits_chain)):
                    try:
                        if index_data_less_bits_chain[i] == '1' or index_data_more_bits_chain[i] == '1':
                            index_data_new_bits_chain.append('1')
                        else:
                            index_data_new_bits_chain.append('0')
                    except IndexError:
                        index_data_new_bits_chain.append(index_data_less_bits_chain[i])
                index_data_new_bits_chain = "".join(index_data_new_bits_chain)
                # print(len(index_data_new_bits_chain))

                bis.write_index_header_expand(index_header_new, os.path.join(index_dir_more, index_file))
                bis.write_index_data(index_data_new_bits_chain, os.path.join(index_dir_more, index_file))


            else:
                index_header_new = index_header_more

                index_data_less = bis.read_index_data(os.path.join(index_dir_less, index_file))
                index_data_more = bis.read_index_data(os.path.join(index_dir_more, index_file))
                
                index_data_less_bits_chain = []
                index_data_more_bits_chain = []
                index_data_new_bits_chain = []
                    # bits_chain = []
                for i in range(len(index_data_less)):
                    # print(index_data[i])
                    # print(bin(index_data[i])[2:].zfill(8))
                    index_data_less_bits_chain.append(bin(index_data_less[i])[2:].zfill(8))
                index_data_less_bits_chain = "".join(index_data_less_bits_chain)
                # print(len(index_data_less_bits_chain))

                for j in range(len(index_data_more)):
                    # print(index_data[i])
                    # print(bin(index_data[i])[2:].zfill(8))
                    index_data_more_bits_chain.append(bin(index_data_more[j])[2:].zfill(8))
                index_data_more_bits_chain = "".join(index_data_more_bits_chain)
                # print(len(index_data_more_bits_chain))

                for i in range(len(index_data_more_bits_chain)):
                    try:
                        if index_data_more_bits_chain[i] == '1' or index_data_less_bits_chain[i] == '1':
                            index_data_new_bits_chain.append('1')
                        else:
                            index_data_new_bits_chain.append('0')
                    except IndexError:
                        index_data_new_bits_chain.append(index_data_more_bits_chain[i])
                index_data_new_bits_chain = "".join(index_data_new_bits_chain)
                # print(len(index_data_new_bits_chain))

                bis.write_index_header_expand(index_header_new, os.path.join(index_dir_more, index_file))
                bis.write_index_data(index_data_new_bits_chain, os.path.join(index_dir_more, index_file))

        else: 
            shutil.copy(os.path.join(index_dir_less, index_file), index_dir_more)


if __name__ == '__main__':
    index_dir_less = r'C:\Users\cugbl\Desktop\index2m'
    index_dir_more = r'C:\Users\cugbl\Desktop\index16m'

    merge_index_files(index_dir_less, index_dir_more)