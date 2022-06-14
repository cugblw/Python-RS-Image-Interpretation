from email import header


# -*- encoding: utf-8 -*-

'''
@File    :   create_index_file.py
@Time    :   2022/06/15 07:44:10
@Author  :   Lee
@Version :   1.0
@License :   (C)Copyright Cennavi, Li Wei
@Desc    :   批量创建索引文件
'''

import os


def create_single_index_file(tile_id, index_file_path):
    """
    创建单个索引文件
    """
    index_file_name = tile_id + '.idx'
    index_file_path = os.path.join(index_file_path, index_file_name)
    return index_file_path

if __name__ == '__main__':
    pass