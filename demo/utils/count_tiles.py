#!/usr/bin/python3
# -*- encoding: utf-8 -*-

'''
@File    :   count_tiles.py
@Time    :   2022/07/14 10:04:54
@Author  :   Weil Lee
@Version :   1.0
@Email   :   cugblw2014@outlook.com
@Desc    :   None
'''


import os
import tarfile
from zipfile import ZipFile


def count_zip_tiles_number(target_path):
    """统计瓦片数量"""
    zip_number = 0
    tiles_number = 0
    for root, dirs, files in os.walk(target_path):
        for file in files:
            if file.endswith(".zip"):
                zip_number += 1
                with ZipFile(os.path.join(root,file), 'r') as zip_file:
                    tile_number = len(zip_file.namelist())
                    tiles_number += tile_number
                zip_file.close()
    return zip_number,tiles_number

def count_tar_tiles_number(target_path):
    """统计瓦片数量"""
    tar_number = 0
    tiles_number = 0
    for root, dirs, files in os.walk(target_path):
        for file in files:
            if file.endswith(".tar"):
                tar_number += 1
                with tarfile.open(os.path.join(root,file), 'r') as tar:
                    tile_number = len(tar.getmembers())
                    tiles_number += tile_number
                tar.close()
    return tar_number,tiles_number


if __name__ == '__main__':
    zip_path = r"C:\Users\Administrator\Desktop\beijing_raster"
    tar_path = r"C:\Users\Administrator\Desktop\tar_test"
    zip_number,zip_tiles_number = count_zip_tiles_number(zip_path)
    tar_number,tar_tiles_number = count_tar_tiles_number(tar_path)
    print(zip_number,tar_number,zip_tiles_number,tar_tiles_number)