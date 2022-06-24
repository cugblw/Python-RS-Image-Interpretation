#!/usr/bin/python3
# -*- encoding: utf-8 -*-

'''
@File    :   image_tiler.py
@Time    :   2022/06/24 10:45:53
@Author  :   Weil Lee
@Version :   1.0
@Email   :   cugblw2014@outlook.com
@Desc    :   None
'''


import io
import os
import tarfile
import time
import sys
from multiprocessing import Pool

import numpy as np
from PIL import Image

sys.path.append('./')

from core import cal_tile_range as ctr
from core import read_subset_of_image as rsoi
from core import read_image as ri
from core import get_zoom_level as gzl
from core.image_util import convert_image_transparency


# 单线程切图
def cut_image_tile(tile_range, tile_size, dataset,tile_dir):
    """裁剪影像瓦片"""
    for key in tile_range:
        start_time = time.time()
        x_min, x_max, y_min, y_max=tile_range[key]
        for x in range(x_min, x_max+1):
            for y in range(y_min, y_max+1):
                img =rsoi.read_image_data_by_tile(key, x, y, tile_size, dataset)
                save_tile(tile_dir, key, x, y, img)
        end_time = time.time()
        print("cut image into tile, zoom = {zoom}".format(zoom = str(key)) + 
              ", time used: " + str(round(end_time - start_time, 3)) + "s.")

# 多线程切图
def cut_image_tile_multi_process(tile_set):
    """裁剪影像瓦片"""
    tile_range, tile_size, geotiff_path, tile_dir, zoom_divide = (tile_set[0], tile_set[1], tile_set[2], 
                                                                  tile_set[3], tile_set[4])
    dataset = ri.read_geotiff(geotiff_path)
    zoom, zoom_max, x_min, x_max, y_min, y_max=tile_range
    if zoom < zoom_divide:
        # start_time = time.time()
        # for x in range(x_min, x_max+1):
        #     for y in range(y_min, y_max+1):
        #         # ds_subset = rsoi.get_geotiff_subset(dataset, zoom, x, y)
        #         img =rsoi.read_image_data_by_tile(zoom, x, y, tile_size, dataset)
        #         # img =rsoi.read_geotiff_by_tile(zoom, x, y, tile_size, ds_subset)
        #         if np.all(np.asarray(img) == 0):
        #             img = None
        #         save_tile(tile_dir, zoom, x, y, img)
        # end_time = time.time()
        # print("cut image into tile, zoom = {zoom}".format(zoom = str(zoom)) + 
        #       ", time used: " + str(round(end_time - start_time, 3)) + "s.")
        pass
    else:
        ds_subset = rsoi.get_geotiff_subset(dataset, zoom, x_min, y_min)
        tile_dict = {}
        start_time = time.time()
        cut_image_tile_recursive(zoom, zoom_max, x_min, y_min, tile_size, ds_subset, tile_dir, tile_dict)
        end_time = time.time()
        print("cut image into tile, zoom = {zoom} - {zoom_max}".format(zoom = str(zoom),zoom_max = 
              str(zoom_max)) + ", time used: " + str(round(end_time - start_time, 3)) + "s.")
        tar_name = str(zoom) + "_" + str(x_min) + "_" + str(y_min) + ".tar"
        with tarfile.open(os.path.join(tile_dir, tar_name), "w") as tar:
            for key in tile_dict.keys():
                if tile_dict[key] is not None:
                    img_byte_arr = io.BytesIO()
                    tarinfo = tarfile.TarInfo(name=key+".png")
                    tile_dict[key].save(img_byte_arr, format='PNG')
                    data = img_byte_arr.getvalue()
                    tarinfo.size = len(data)
                    tar.addfile(tarinfo, fileobj=io.BytesIO(data))
                else:
                    pass
        tar.close()

def cut_image_tile_recursive(zoom, end_zoom, x, y, tile_size, dataset, tile_dir, tile_dict):
    if zoom>end_zoom:
        return

    img =rsoi.read_image_data_by_tile(zoom, x, y, tile_size, dataset)
    # save_tile(tile_dir, zoom, x, y, img)
    tile_id = str(zoom) + '/'+str(zoom) + "_" + str(x) + "_" + str(y)
    tile_dict[tile_id] = img
    cut_image_tile_recursive(zoom+1, end_zoom, x * 2, y * 2, tile_size, dataset, tile_dir, tile_dict)
    cut_image_tile_recursive(zoom+1, end_zoom, x * 2 + 1, y * 2, tile_size, dataset, tile_dir, tile_dict)
    cut_image_tile_recursive(zoom+1, end_zoom, x * 2, y * 2 + 1, tile_size, dataset, tile_dir, tile_dict)
    cut_image_tile_recursive(zoom+1, end_zoom, x * 2 + 1, y * 2 + 1, tile_size, dataset, tile_dir, tile_dict)


# 保存瓦片
def save_tile(tile_dir,zoom,x,y,img):
    """保存瓦片"""
    if img is None:
        pass
    tile_name = str(zoom) + "_" + str(x) + "_" + str(y) + ".png"
    tile_path = os.path.join(tile_dir, str(zoom), tile_name)
    try:
        img.save(tile_path)
    except:
        pass

def __image_composite(source_dict, z, x, y, extension, img_format):
    IMAGE_SIZE = 256  # 每张小图片的大小
    IMAGE_ROW = 2  # 图片间隔，也就是合并成一张图后，一共有几行
    IMAGE_COLUMN = 2  # 图片间隔，也就是合并成一张图后，一共有几列

    to_image = Image.new('RGBA', (IMAGE_COLUMN * IMAGE_SIZE, IMAGE_ROW * IMAGE_SIZE))  # 创建一个新图

    for y_delta in [0, 1]:
        for x_delta in [0, 1]:
            x_split = x * 2 + x_delta
            y_split = y * 2 + y_delta
            key = str(z + 1) + "_" + str(x_split) + "_" + str(y_split)
            if key not in source_dict:
                continue
            from_image = Image.open(io.BytesIO(source_dict[key])).resize((IMAGE_SIZE, IMAGE_SIZE), Image.Resampling.LANCZOS)
            if extension == "jpg":
                from_image.convert("RGBA")
            to_image.paste(from_image, (x_delta * IMAGE_SIZE, y_delta * IMAGE_SIZE))

    data_combined = io.BytesIO()
    to_image = to_image.resize((IMAGE_SIZE, IMAGE_SIZE), Image.Resampling.LANCZOS)
    img_out = convert_image_transparency(to_image)

    if img_out is None:
        # return
        img_out = Image.new("RGBA", (IMAGE_SIZE,IMAGE_SIZE),(255, 255, 255, 0))
    if img_out == "part-blank":
        extension = "PNG"
    else:
        to_image = img_out

    if extension == "jpg":
        to_image.convert("RGB").save(data_combined, format='JPEG')
    else:
        to_image.save(data_combined, format='PNG')
    # print(z, x, y,extension)
    # if extension == "PNG":
    #     to_image.close()
    #     save_util.delete_tmp_image(z,x,y)

    data = data_combined.getvalue()
    return data

def create_low_zoom_tar(tar_dir, tar_new_dir, max_zoom, min_zoom, img_format):
    extension = None
    image_dict = {}
    for file_name in os.listdir(tar_dir):
        if not file_name.endswith(".tar"):
            continue
        tar = tarfile.open(os.path.join(tar_dir, file_name), "r")

        for name in tar.getnames():
            member = tar.getmember(name)
            f = tar.extractfile(member)
            data = f.read()
            if (sys.platform == "win32"):
                pic_name = name.replace("/","\\").split(os.path.sep)[-1]
            else:
                pic_name = name.rsplit(os.path.sep)[-1]
            if pic_name.split("_")[0] != str(max_zoom):
                continue
            image_dict[pic_name.split(".")[0]] = data
            if extension is None:
                extension = pic_name.split(".")[-1].lower()

    tmp_dict = {}
    for zoom in range(max_zoom - 1, min_zoom - 1, -1):
        start_time = time.time()
        tar_file_new = os.path.join(tar_new_dir, str(zoom) + ".tar")
        tar = tarfile.open(tar_file_new, "w")
        for key in image_dict.keys():
            z, x, y = key.split("_")
            z = int(int(z) - 1)
            x = int(int(x) / 2)
            y = int(int(y) / 2)
            key_new = str(z) + "_" + str(x) + "_" + str(y)

            if key_new in tmp_dict:
                continue
            data_new = __image_composite(image_dict, z, x, y, extension, img_format)
            tmp_dict[key_new] = data_new
            tile_name = str(zoom) + '/'+str(zoom) + "_" + str(x) + "_" + str(y) + "." + extension
            tarinfo = tarfile.TarInfo(name=tile_name)
            tarinfo.size = len(data_new)

            tar.addfile(tarinfo, io.BytesIO(data_new))
        tar.close()
        image_dict = tmp_dict
        tmp_dict.clear()
        end_time = time.time()
        print("cut image into tile, zoom = {zoom}".format(zoom = str(zoom)) + 
              ", time used: " + str(round(end_time - start_time, 3)) + "s.")


if __name__ == "__main__":
    tile_size = 256
    tile_dir = "C:/Users/cugbl/Desktop/tile_test"
    geotiff_path = "E:/Data/test/lanzhou_05m_test.tif"

    time_start = time.time()
    if not os.path.exists(tile_dir):
        os.makedirs(tile_dir)
    dataset = ri.read_geotiff(geotiff_path)
    bands = ri.get_geotiff_bands(dataset)
    print("This image has %d bands" % len(bands))
    if len(bands) != 3:
        print("This Image has more than 3 bands, please check it!")
        exit(1)

    extent = ri.get_geotiff_extent(geotiff_path)
    optimal_zoom = gzl.get_optimal_zoom_level(geotiff_path, tile_size)
    start_zoom = gzl.get_one_tile_zoom_level(extent, tile_size)
    end_zoom = gzl.get_optimal_zoom_level(geotiff_path, tile_size)
    # print("Start zoom",start_zoom)
    # print("End zoom",end_zoom)
    zoom_divide = int((end_zoom + start_zoom)/2)

    # for zoom in range(start_zoom,end_zoom+1):
    #     if not os.path.exists(tile_dir + "/" + str(zoom)):
    #         os.makedirs(tile_dir + "/" + str(zoom))
    # # 单线程切图
    # tile_range_dict = ctr.tile_range_dict(extent, start_zoom, end_zoom)
    # cut_image_tile(tile_range_dict, tile_size, dataset, tile_dir)

    # 多线程切图
    tile_range = ctr.tile_range_list(extent, start_zoom, end_zoom)
    tile_range_list = []
    for i in tile_range:
        tile_range_list.append([i,tile_size,geotiff_path,tile_dir,zoom_divide])
    del dataset
    pool = Pool(processes=6)
    pool.map(cut_image_tile_multi_process, tile_range_list)

    # 创建瓦片压缩包
    create_low_zoom_tar(tile_dir, tile_dir, zoom_divide, start_zoom, "png")

    time_end = time.time()
    print("Time used: %s" % str(round((time_end - time_start)/60, 3)) + "min.")