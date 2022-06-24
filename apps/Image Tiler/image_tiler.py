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

sys.path.append('./')

from core import cal_tile_range as ctr
from core import read_subset_of_image as rsoi
from core import read_image as ri
from core import get_zoom_level as gzl


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
        start_time = time.time()
        for x in range(x_min, x_max+1):
            for y in range(y_min, y_max+1):
                # ds_subset = rsoi.get_geotiff_subset(dataset, zoom, x, y)
                img =rsoi.read_image_data_by_tile(zoom, x, y, tile_size, dataset)
                # img =rsoi.read_geotiff_by_tile(zoom, x, y, tile_size, ds_subset)
                if np.all(np.asarray(img) == 0):
                    img = None
                save_tile(tile_dir, zoom, x, y, img)
        end_time = time.time()
        print("cut image into tile, zoom = {zoom}".format(zoom = str(zoom)) + 
              ", time used: " + str(round(end_time - start_time, 3)) + "s.")
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


if __name__ == "__main__":
    tile_size = 256
    tile_dir = "C:/Users/cugbl/Desktop/tile_test"
    geotiff_path = "E:/Data/test/lanzhou.tif"

    if not os.path.exists(tile_dir):
        os.makedirs(tile_dir)

    time_start = time.time()
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

    for zoom in range(start_zoom,end_zoom+1):
        if not os.path.exists(tile_dir + "/" + str(zoom)):
            os.makedirs(tile_dir + "/" + str(zoom))
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

    time_end = time.time()
    print("Time used: %s" % str(round((time_end - time_start)/60, 3)) + "min.")