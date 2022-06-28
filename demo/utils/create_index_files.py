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
import tarfile
import time
from itertools import chain

import build_index_structure as bi
import cal_tile_range as ctr
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


def create_index_file_from_dir(start_zoom, end_zoom, tile_id_list, tile_dir, index_dir):
    for tile_id in tile_id_list:
        zoom = int(tile_id.split('_')[0])
        x = int(tile_id.split('_')[1])
        y = int(tile_id.split('_')[2])
        if zoom != start_zoom:
            continue
        index_file_path = create_single_index_file(tile_id, index_dir)
        morton_dict = {}
        ctr.search_tile_from_dir_recursively(zoom, x, y, end_zoom,tile_dir,morton_dict)
        morton_dict = dict(sorted(morton_dict.items(), key=lambda x: x[0]))

        bits_chain = "".join(list(chain(*morton_dict.values())))
        bits_chain,end_zoom_new = bi.remove_invalid_bits(bits_chain)
        bits_chain_full = bi.concatenate_bits_chain(bits_chain)

        bi.write_index_header(zoom, end_zoom_new, index_file_path)
        bi.write_index_data(bits_chain_full, index_file_path)
        print("create index file: " + os.path.basename(index_file_path))


def create_index_file_from_tar(start_zoom, end_zoom, tile_id_list, tar_dir, index_dir):
    for tile_id in tile_id_list:
        zoom = int(tile_id.split('_')[0])
        x = int(tile_id.split('_')[1])
        y = int(tile_id.split('_')[2])
        if zoom != start_zoom:
            continue
        index_file_path = create_single_index_file(tile_id, index_dir)
        morton_dict = {}

        tar_list = ctr.generate_tar_list_by_tileId(tile_id, tar_dir)
        members_list = []
        for tar_file in tar_list:
            with tarfile.open(tar_file,'r') as tar:
                members = tar.getnames()
                members_list.extend(members)

        ctr.search_tile_from_tar_recursively(zoom, x, y, end_zoom, members_list, morton_dict)
        morton_dict = dict(sorted(morton_dict.items(), key=lambda x: x[0]))

        bits_chain = "".join(list(chain(*morton_dict.values())))
        bits_chain,end_zoom_new = bi.remove_invalid_bits(bits_chain)
        bits_chain_full = bi.concatenate_bits_chain(bits_chain)

        bi.write_index_header(zoom, end_zoom_new, index_file_path)
        bi.write_index_data(bits_chain_full, index_file_path)
        print("create index file: " + os.path.basename(index_file_path))


def create_global_index_file(start_zoom, end_zoom,index_dir):
    """
    create global index files of zoom 10 to zoom 14 海洋索引文件
    """
    start_zoom = start_zoom
    end_zoom = end_zoom

    for x in range(0,1024):
        for y in range(0,1024):
            tile_id = str(10) + '_' + str(x) + '_' + str(y)
            index_file_path = create_single_index_file(tile_id, index_dir)
            morton_dict = {}
            ctr.calculate_global_tile_xyz_recursively(10, x, y, 14,morton_dict)
            bits_chain = "".join(list(chain(*morton_dict.values())))
            bits_chain,end_zoom_new = bi.remove_invalid_bits(bits_chain)
            bits_chain_full = bi.concatenate_bits_chain(bits_chain)
            bi.write_index_header(start_zoom, end_zoom_new, index_file_path)
            bi.write_index_data(bits_chain_full, index_file_path)
            print("create index file: " + os.path.basename(index_file_path))

    
if __name__ == '__main__':
    start_zoom = 10
    end_zoom = 18
    tar_dir = r"C:\Users\Administrator\Desktop\2m"
    tile_dir = r"C:\Users\Administrator\Desktop\2m"
    index_dir = r"C:\Users\Administrator\Desktop\index\2m"
    tile_list = ci.get_tile_id_from_tar(tar_dir)
    tile_list_convert = ci.convert_tile_id(tile_list)

    start_time = time.time()
    print("start to create index file ...")
    print("-----------------------------------------")

    # # 从文件夹中创建索引文件
    # create_index_file_from_dir(start_zoom, end_zoom, tile_list_convert, tile_dir, index_dir)

    # 从tar文件中创建索引文件
    create_index_file_from_tar(start_zoom, end_zoom, tile_list_convert, tar_dir, index_dir)

    end_time = time.time()
    print("-----------------------------------------")
    print("create index file completed!")
    print("time used: " + str(round((end_time - start_time)/60,3)) + "min.") 

    # # create global index file from zoom 10 to zoom 14
    # index_dir = r"C:\Users\Administrator\Desktop\global_index"
    # start_time = time.time()
    # create_global_index_file(10, 14,index_dir)
    # end_time = time.time()
    # print("build index file completed!")
    # print("time used: " + str((end_time - start_time)/3600) + "hour.")
