# -*- encoding: utf-8 -*-

'''
@File    :   composite_tiles_v2.0.py
@Time    :   2022/07/23 10:50:09
@Author  :   Lee
@Version :   1.0
@License :   (C)Copyright Cennavi, Li Wei
@Desc    :   None
'''


import io
import logging
from math import ceil
import os
import shutil
import time
import tarfile
from zipfile import ZipFile
from functools import partial
from multiprocessing import Pool

from PIL import Image
import numpy as np

from tile_lon_lat_convert import low_room_tile_to_high_room_tile


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def get_image_tar_list(image_tar_path):
    """
    获取影像tar包列表
    :param image_tar_path:
    :return: image_tar_list
    """
    image_tar_list = []
    for root, dirs, files in os.walk(image_tar_path):
        for file in files:
            if file.endswith(".tar"):
                image_tar_list.append(os.path.join(
                    root, file).replace("\\", "/"))
    return sorted(image_tar_list)


def get_raster_zip_list(raster_zip_path):
    """
    获取raster zip包列表
    :param raster_zip_path:
    :return: raster_zip_list
    """
    raster_zip_list = []
    for root, dirs, files in os.walk(raster_zip_path):
        for file in files:
            if file.endswith(".zip"):
                raster_zip_list.append(os.path.join(
                    root, file).replace("\\", "/"))
    return raster_zip_list


def get_zip_list_by_tileId(zoom, x, y, zip_dir):
    """
    根据瓦片编号生成zip包列表
    :param zoom:
    :param x:
    :param y:
    :param zip_dir:
    :return: zip_list
    """
    zip_list = get_raster_zip_list(zip_dir)
    zip_filter_list = []
    zoom_index_list = []
    if zoom == 3:
        zoom_index_list = [0, 3]
    
    elif zoom == 8:
        zoom_index_list = [3, 7]
    
    elif zoom == 10:
        zoom_index_list = [7]
    
    elif zoom == 13:
        zoom_index_list = [7]
    
    elif zoom < 3:
        zoom_index_list = None
    
    else:
        zoom_index_list = [0,3,7]

    zip_tile_list = []
    for zoom_index in zoom_index_list:
        if zoom >= zoom_index:
            zip_tile_x = int(x >> (zoom-zoom_index))
            zip_tile_y = int(y >> (zoom-zoom_index))
            zip_tile_list.append(
                (str(zoom_index) + "_" + str(zip_tile_x) + "_" + str(zip_tile_y)))
        else:
            x_min, x_max, y_min, y_max, z_high = low_room_tile_to_high_room_tile(x,y,zoom,zoom_index)
            for x_index in range(x_min, x_max+1):
                for y_index in range(y_min, y_max+1):
                    zip_tile_list.append(
                        (str(zoom_index) + "_" + str(x_index) + "_" + str(y_index)))

    for zip_file in zip_list:
        for zip_tile in zip_tile_list:
            if zip_file.find(zip_tile) != -1:
                zip_filter_list.append(zip_file)
    return zip_filter_list


def group_list(tar_list, process_num):
    """
    list分组
    :param tar_list:
    :param group_size:
    :return: group_list
    """
    tar_group_list = []
    group_size = ceil(len(tar_list) / process_num)

    for i in range(0, len(tar_list), group_size):
        b = tar_list[i:i+group_size]
        tar_group_list.append(b)
    return tar_group_list


def composite_tiles(image_tar_list, raster_zip_path, output_dir):
    """
    合成瓦片
    :param image_tar_list:
    :param raster_zip_path:
    :param output_dir:
    :return:
    """
    # image_tar_list = get_image_tar_list(image_tar_path)
    zip_temp_dict = {}
    zip_temp_list = []
    zip_members_name_temp_dict = {}
    for image_tar in image_tar_list:
        logging.info("matching image and raster tile: {}.".format(image_tar))
        image_tar_name = os.path.basename(image_tar)
        image_tar_tileId = image_tar_name.split(".")[0]
        try:
            z, x, y = image_tar_tileId.split("_")
        except:
            logging.error("image_tar_tileId: {} is invalid.".format(image_tar_tileId))
            shutil.copy(image_tar, output_dir)
            continue
        zip_list = get_zip_list_by_tileId(
            int(z), int(x), int(y), raster_zip_path)
        if (zip_list == None) or (len(zip_list) == 0) or ("_" not in image_tar_tileId):
            logging.info("no raster tile found: {}.".format(image_tar))
            shutil.copy(image_tar, output_dir)
            continue
        zip_dict = {}
        zip_members_name_dict = {}
        if zip_list == zip_temp_list:
            zip_dict = zip_temp_dict
            for zip_file in zip_list:
                zip_members_name_dict = zip_members_name_temp_dict
        
        else:
            for zip_file_path in zip_list:
                zip_file = ZipFile(zip_file_path)
                zip_members = zip_file.namelist()
                zip_memebers_dict = {}
                for zip_member in zip_members:
                    zip_memebers_dict[zip_member] = zip_file.open(zip_member)
                zip_dict[zip_file_path] = zip_memebers_dict
                zip_members_name_dict[zip_file_path] = zip_members

        tar_file = tarfile.open(image_tar)
        tar_members = tar_file.getmembers()
        new_tar_file = tarfile.open(
            os.path.join(output_dir, image_tar_name), "w")

        for tar_member in tar_members:
            tar_member_name = tar_member.name
            raster_name = "raster_" + \
                (tar_member_name.split("/")[-1].split(".")[0])
            
            tile_exist = False
            tile_exist_zip_path = None
            for zip_file_path in zip_members_name_dict.keys():
                if raster_name in zip_members_name_dict[zip_file_path]:
                    tile_exist = True
                    tile_exist_zip_path = zip_file_path
                    break
                else:
                    continue

            if tile_exist:
                image_img = Image.open(io.BytesIO(
                    tar_file.extractfile(tar_member_name).read()))
                raster_img = Image.open(
                    zip_dict[tile_exist_zip_path][raster_name])

                if np.all(np.asarray(raster_img) == 0):
                    new_tar_file.addfile(tar_file.getmember(
                        tar_member_name), tar_file.extractfile(tar_member_name))

                else:
                    image_img.paste(raster_img, (0, 0), raster_img)

                    if image_img.mode != "RGB":
                        img_byte_arr = io.BytesIO()
                        image_img.save(img_byte_arr, format="PNG")
                        # image_img.save(os.path.join(output_dir, os.path.basename(tar_member_name)), format="PNG")
                        data = img_byte_arr.getvalue()
                        tarinfo = tarfile.TarInfo(tar_member_name)
                        tarinfo.size = len(data)
                        new_tar_file.addfile(tarinfo, io.BytesIO(data))

                    else:
                        img_byte_arr = io.BytesIO()
                        image_img.save(img_byte_arr, format="JPEG")
                        # image_img.save(os.path.join(output_dir, os.path.basename(tar_member_name)), format="JPEG")
                        data = img_byte_arr.getvalue()
                        tarinfo = tarfile.TarInfo(tar_member_name)
                        tarinfo.size = len(data)
                        new_tar_file.addfile(tarinfo, io.BytesIO(data))
            
            else:
                new_tar_file.addfile(tar_file.getmember(
                    tar_member_name), tar_file.extractfile(tar_member_name))

        new_tar_file.close()
        tar_file.close()
        zip_temp_list = zip_list
        zip_temp_dict = zip_dict   # 将zip_dict存入zip_temp_dict中，以便后续使用
        zip_members_name_temp_dict = zip_members_name_dict # 将zip_members_name_dict存入zip_temp_dict中，以便后续使用
        zip_dict = {}           # 清空zip_dict
        zip_members_name_dict = {} # 清空zip_members_name_dict


if __name__ == "__main__":
    # 栅格瓦片zip包路径
    raster_zip_path = "/app2/tmp/raster_image_merge/raster_0_14"
    # 影像瓦片tar包路径
    image_tar_path = "/app2/tmp/raster_image_merge/tar_test"
    # 合成瓦片输出路径
    output_path = "/app2/tmp/raster_image_merge/output"
    # 指定进程数,建议设置8个进程
    process_num = 8

    start_time = time.time()

    # 合成id匹配的栅格和影像瓦片
    print("-----------------------------------------")
    print("Start to composite raster and image tile.")
    print("-----------------------------------------")

    # 获取影像tar包列表
    image_tar_list = get_image_tar_list(image_tar_path)
    # 分组
    image_tar_list_group = group_list(image_tar_list, process_num)
    partial_composite = partial(
        composite_tiles, raster_zip_path=raster_zip_path, output_dir=output_path)

    # 合成瓦片
    composite_pool = Pool(processes=process_num)
    composite_pool.map_async(partial_composite, image_tar_list_group)
    composite_pool.close()
    composite_pool.join()

    print("-----------------------------------------")
    print("Composite raster and image tile finished.")
    print("-----------------------------------------")
    end_time = time.time()
    print("Time used: " + str(round((end_time - start_time)/60, 3)) + "min.")