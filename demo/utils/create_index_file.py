from email import header
from itertools import chain
import time


# -*- encoding: utf-8 -*-

'''
@File    :   create_index_file.py
@Time    :   2022/06/15 07:44:10
@Author  :   Lee
@Version :   1.0
@License :   (C)Copyright Cennavi, Li Wei
@Desc    :   create index file
'''

import os
import build_index_structure as bi
import cal_tile_range as ct
import cal_index_id as ci


def create_single_index_file(tile_id, index_file_path):
    """
    创建单个索引文件
    """
    index_file_name = tile_id + '.idx'
    index_file_path = os.path.join(index_file_path, index_file_name)
    return index_file_path

def create_index_file(tile_id_list, index_file_path):
    """
    创建索引文件
    """
    index_file_list = []
    for tile_id in tile_id_list:
        index_file_list.append(create_single_index_file(tile_id, index_file_path))
    return index_file_list

if __name__ == '__main__':
    start_zoom = 10
    end_zoom = 13
    tar_dir = r"C:\Users\Administrator\Desktop\16m"
    tile_dir = r"C:\Users\Administrator\Desktop\tile_index"
    index_dir = r"C:\Users\Administrator\Desktop\tile_index\satellite\index"
    tile_list = ci.get_tile_id_from_tar(tar_dir)
    # tile_list_convert = ci.convert_tile_id(tile_list)
    # tile_list_convert = ["10_806_401"]
    tile_list_convert = ["10_806_401","10_807_401","10_807_402"]

    start_time = time.time()
    print("start to create index file.")

    
    for tile_id in tile_list_convert:
        zoom = int(tile_id.split('_')[0])
        x = int(tile_id.split('_')[1])
        y = int(tile_id.split('_')[2])
        index_file_path = create_single_index_file(tile_id, index_dir)
        morton_dict = {}
        ct.calculate_tile_xyz_recusively(zoom, x, y, end_zoom,tile_dir,morton_dict)
        morton_dict = dict(sorted(morton_dict.items(), key=lambda x: x[0]))
        # print(len(morton_dict))
        print(morton_dict)
        bits_chain = "".join(list(chain(*morton_dict.values())))
        bits_chain,end_zoom_new = bi.remove_invalid_bits(bits_chain)
        bits_chain_full = bi.concatenate_bits_chain(bits_chain)
        print(bits_chain_full)

        bi.write_index_header(zoom, end_zoom_new, index_file_path)
        bi.write_index_data(bits_chain_full, index_file_path)
        print("create index file: " + os.path.basename(index_file_path))

    

    # print(tile_list_convert)
    end_time = time.time()
    print("build index file completed!")
    print("time used: " + str((end_time - start_time)/60) + "min.") 
    pass