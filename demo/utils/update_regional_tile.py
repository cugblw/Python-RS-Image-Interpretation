# -*- encoding: utf-8 -*-

'''
@File    :   regional_tile_update.py
@Time    :   2022/06/26 21:54:36
@Author  :   Lee
@Version :   1.0
@License :   (C)Copyright Cennavi, Li Wei
@Desc    :   update regional tiles
'''

import os 
import shutil
import time

import piexif
from PIL import Image

def generate_file_name(source_name, z, x, y):
    """通过瓦片编号计算瓦片存储路径"""
    if z > 6:
        dir_ = 1 << (z - 5)
        row = int(y / dir_)
        col = int(x / dir_)
        file_name = os.path.join(source_name, str(z), "R" + str(row), "C" + str(col),
                                 str(z) + "_" + str(x) + "_" + str(y) + ".jpg")
    else:
        file_name = os.path.join(source_name, str(z), str(z) + "_" + str(x) + "_" + str(y) + ".jpg")
    return file_name


def get_jpg_info(img):
    exif_dict = piexif.load(img.info['exif'])
    resolution = exif_dict['0th'][271].decode('utf-8')
    return resolution


def get_png_metadata(img):
    if img.text is None:
        return None
    resolution = img.text['resolution']
    return resolution


def get_img_info(img):
    if img.mode == "RGB":
        return get_jpg_info(img)
    else:
        return get_png_metadata(img)


def update_tile(base_tile_dir,regional_tile_dir):
    """
    Update regional tile
    """
    # Get regional tile list
    regional_tile_list = []
    for root, dirs, files in os.walk(regional_tile_dir):
        for file in files:
            if file.endswith(".jpg"):
                regional_tile_list.append(os.path.join(root, file))

    # print(regional_tile_list)

    for tile in regional_tile_list:
        tile_name = os.path.basename(tile)
        tile_id = tile_name.split('.')[0]
        zoom, x, y = tile_id.split('_')[0], tile_id.split('_')[1], tile_id.split('_')[2]
        base_tile_name = generate_file_name("satellite", int(zoom), int(x), int(y))
        if not os.path.exists( os.path.join(base_tile_dir, base_tile_name)):
            base_dir = os.path.dirname(os.path.join(base_tile_dir, base_tile_name))
            if not os.path.exists(base_dir):
                os.makedirs(base_dir)
            shutil.copy(tile, os.path.join(base_tile_dir, base_tile_name))
            print("Update tile: " + tile_name)


        else:
            try:
                tile_resolution = get_img_info(Image.open(tile))
                base_tile_resolution = get_img_info(Image.open(os.path.join(base_tile_dir, base_tile_name)))
            except:
                print("Error: This lile has no resolution info, please check it!")
                exit(1)
            # print("Tile resolution: " + tile_resolution)
            # print("Base tile resolution: " + base_tile_resolution)
            if base_tile_resolution == '0.5m':
                pass

            elif base_tile_resolution == '2m' and tile_resolution == '0.5m':
                shutil.copy(tile, os.path.join(base_tile_dir, base_tile_name))
                print("Update tile: " + tile_name)

            elif base_tile_resolution == '2m' and tile_resolution == '2m':
                pass

            elif base_tile_resolution == '2m' and tile_resolution == '16m':
                pass

            elif base_tile_resolution == '16m' and tile_resolution == '0.5m':
                shutil.copy(tile, os.path.join(base_tile_dir, base_tile_name))
                print("Update tile: " + tile_name)

            elif base_tile_resolution == '16m' and tile_resolution == '2m':
                shutil.copy(tile, os.path.join(base_tile_dir, base_tile_name))
                print("Update tile: " + tile_name)

            elif base_tile_resolution == '16m' and tile_resolution == '16m':
                pass

            else:
                print("Error: Tile resolution is not compatible with base tile resolution")
                exit(1)


if __name__ == '__main__':
    # 所有瓦片部署路径，包括16m,2m,0.5m
    base_tile_dir = 'C:/Users/cugbl/Desktop/tile_test'
    # 需要进行更新的瓦片路径
    regional_tile_dir = 'C:/Users/cugbl/Desktop/05m_new'

    start_time = time.time()
    update_tile(base_tile_dir,regional_tile_dir)
    end_time = time.time()
    print("Update tiles completed!")
    print("Time used: " + str(round((end_time - start_time), 2)) + " seconds")