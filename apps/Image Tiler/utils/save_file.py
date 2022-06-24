# 保存瓦片
import string

import os
import tarfile

import PIL

def save_tile(tile_dir: string, zoom: int, x:int ,y:int ,img: PIL.Image):
    """保存瓦片"""
    if img is None:
        pass
    tile_name = str(zoom) + "_" + str(x) + "_" + str(y) + ".png"
    tile_path = os.path.join(tile_dir, str(zoom), tile_name)
    try:
        img.save(tile_path)
    except:
        pass

def save_tile_to_tar(tile_dir: string, zoom: int, x:int ,y:int ,img: PIL.Image, tar_path: string):
    """保存瓦片"""
    if img is None:
        pass
    tile_name = str(zoom) + "_" + str(x) + "_" + str(y) + ".png"
    tile_path = os.path.join(tile_dir, str(zoom), tile_name)
    try:
        img.save(tile_path)
        tar_file = tarfile.open(tar_path, "a")
        tar_file.add(tile_path)
        tar_file.close()
    except:
        pass