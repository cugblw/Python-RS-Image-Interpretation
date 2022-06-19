import os
import time
import sys
from multiprocessing import Pool

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
        if not os.path.exists(tile_dir + "/" + str(key)):
            os.makedirs(tile_dir + "/" + str(key))
        for x in range(x_min, x_max+1):
            for y in range(y_min, y_max+1):
                img =rsoi.read_image_data_by_tile(key, x, y, tile_size, dataset)
                save_tile(tile_dir, key, x, y, img)
        end_time = time.time()
        print("cut image into tile, zoom = {zoom}".format(zoom = str(key)) + ", time used: " + str(round(end_time - start_time, 3)) + "s.")

# 多线程切图
def cut_image_tile_multi_process(tile_set):
    """裁剪影像瓦片"""
    tile_range, tile_size, geotiff_path,tile_dir = tile_set[0], tile_set[1], tile_set[2], tile_set[3]
    dataset = ri.read_geotiff(geotiff_path)
    zoom, x_min, x_max, y_min, y_max=tile_range
    start_time = time.time()
    if not os.path.exists(tile_dir + "/" + str(zoom)):
        os.makedirs(tile_dir + "/" + str(zoom))
    for x in range(x_min, x_max+1):
        for y in range(y_min, y_max+1):
            img =rsoi.read_image_data_by_tile(zoom, x, y, tile_size, dataset)
            save_tile(tile_dir, zoom, x, y, img)
    end_time = time.time()
    print("cut image into tile, zoom = {zoom}".format(zoom = str(zoom)) + ", time used: " + str(round(end_time - start_time, 3)) + "s.")

# 保存瓦片
def save_tile(tile_dir,zoom,x,y,img):
    """保存瓦片"""
    tile_name = str(zoom) + "_" + str(x) + "_" + str(y) + ".png"
    tile_path = os.path.join(tile_dir, str(zoom), tile_name)
    img.save(tile_path)


if __name__ == "__main__":
    tile_size = 256
    tile_dir = r"C:\Users\cugbl\Desktop\tile_test"
    geotiff_path = r"C:\Users\cugbl\Desktop\src\lanzhou_05m_test.tif"

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

    # 单线程切图
    tile_range_dict = ctr.tile_range_dict(extent, start_zoom, end_zoom)
    cut_image_tile(tile_range_dict, tile_size, dataset, tile_dir)

    # # 多线程切图
    # tile_range = ctr.tile_range_list(extent, start_zoom, end_zoom)
    # tile_range_list = []
    # for i in tile_range:
    #     tile_range_list.append([i,tile_size,geotiff_path,tile_dir])
    # del dataset
    # pool = Pool(processes=4)
    # pool.map(cut_image_tile_multi_process, tile_range_list)

    time_end = time.time()
    print("Time used: %s" % str(round((time_end - time_start)/60, 3)) + "min.")