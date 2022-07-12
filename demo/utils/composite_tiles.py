import os
import io
import logging
import shutil
import tarfile
import time
from zipfile import ZipFile
from functools import partial
from multiprocessing import Pool

from PIL import Image
import numpy as np

import tile_lon_lat_convert as tc


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

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
    return file_name.replace("\\", "/")


def check_tile_exist_tar(zoom, x, y, members_list):
    """检查瓦片是否存在tar包中"""
    tile_name = generate_file_name("satellite", zoom, x, y).replace("\\","/")
    
    if tile_name in members_list:
        return True
    else:
        return False


def get_tar_list_by_tileId(zoom,x,y,tar_dir):
    """根据瓦片编号生成tar包列表"""
    zoom_index_list = []
    
    if zoom < 8:
        zoom_index_list=[3]
    elif zoom <= 16:
        zoom_index_list=[8,10,13]
    else:
        zoom_index_list = [13]
    # zoom = int(tile_id.split('_')[0])
    # x = int(tile_id.split('_')[1])
    # y = int(tile_id.split('_')[2])
    tar_list = []
    for zoom_index in zoom_index_list:
        if zoom_index < zoom:
            i = int(x>>(zoom-zoom_index))
            j = int(y>>(zoom-zoom_index))
            tar_file_name = os.path.join(tar_dir, str(zoom_index) + "_" + str(i) + "_" + str(j) + ".tar")
            if os.path.exists(tar_file_name):
                tar_list.append(tar_file_name)
        elif zoom_index == zoom:
            tar_file_name = os.path.join(tar_dir, str(zoom_index) + "_" + str(x) + "_" + str(y) + ".tar")
            if os.path.exists(tar_file_name):
                tar_list.append(tar_file_name)
        elif zoom_index > zoom:
            x_min,x_max,y_min,y_max,z = tc.low_room_tile_to_high_room_tile(x,y,zoom,zoom_index)
            tile_list = tc.xyz_to_tile_list(x_min, x_max, y_min, y_max,z)
            for tile_xyz in tile_list:
                tar_file_name = os.path.join(tar_dir, tile_xyz + ".tar")               
                if os.path.exists(tar_file_name):
                    tar_list.append(tar_file_name)    
        else:
            pass
    return tar_list


def get_raster_zip_list(raster_zip_path):
    """获取raster zip包列表"""
    raster_zip_list = []
    for root, dirs, files in os.walk(raster_zip_path):
        for file in files:
            if file.endswith(".zip"):
                raster_zip_list.append(os.path.join(root, file).replace("\\","/"))
    return raster_zip_list


def get_image_tar_list(image_tar_path):
    """获取影像tar包列表"""
    image_tar_list = []
    for root, dirs, files in os.walk(image_tar_path):
        for file in files:
            if file.endswith(".tar"):
                image_tar_list.append(os.path.join(root, file).replace("\\","/"))
    return image_tar_list


def composite_tiles(image_tar_path,temp_path,raster_zip_path):
    """合成瓦片"""
    composite_image_dict = {}
    with ZipFile(raster_zip_path, 'r') as zip_file:
        for name in zip_file.namelist():
            if name == 'default':
                pass         
            else:
                z,x,y = name.split("_")[1],name.split("_")[2],name.split("_")[3]
                tar_list = get_tar_list_by_tileId(int(z),int(x),int(y),image_tar_path)
                
                if len(tar_list) == 0:
                    pass
                else:
                    for tar_file in tar_list:
                        with tarfile.open(tar_file,'r') as tar:
                            members = tar.getnames()
                            if check_tile_exist_tar(int(z),int(x),int(y),members):
                                # print("Find a matching tile: %s. "%(name))
                                logging.info("Find a matching tile: %s. "%(name))
                                raster_img = Image.open(zip_file.open(name))
                                if np.all(np.asarray(raster_img) == 0):
                                    pass                              
                                else:
                                    image_name = generate_file_name("satellite", int(z), int(x), int(y))
                                    image_img = Image.open(io.BytesIO(tar.extractfile(image_name).read()))
                                    image_img.paste(raster_img, (0,0), raster_img)
                                    composite_image_dict[image_name] = image_img
                    else:
                        pass

    if len(composite_image_dict) > 0:        
        with tarfile.open(os.path.join(temp_path, raster_zip_path.split('/')[-1].replace(".zip",".tar")), 'w') as new_tar_file:
            for key in composite_image_dict.keys():
                if composite_image_dict[key].mode == "RGB":
                    img_byte_arr = io.BytesIO()
                    composite_image_dict[key].save(img_byte_arr, format='JPEG')
                    data = img_byte_arr.getvalue()
                    tarinfo = tarfile.TarInfo(key)
                    tarinfo.size = len(data)
                    new_tar_file.addfile(tarinfo, fileobj=io.BytesIO(data))                
                else:
                    img_byte_arr = io.BytesIO()
                    composite_image_dict[key].save(img_byte_arr, format='PNG')
                    data = img_byte_arr.getvalue()
                    tarinfo = tarfile.TarInfo(key)
                    tarinfo.size = len(data)
                    new_tar_file.addfile(tarinfo, fileobj=io.BytesIO(data))
        composite_image_dict.clear()   
    else:
        composite_image_dict.clear()


def roll_all_image_tiles(temp_path, output_path, image_tar_file):
    """获取完成的影像输出"""
    # image_tar_list = get_image_tar_list(image_tar_path)
    composite_tar_list = get_image_tar_list(temp_path)

    # for image_tar_file in image_tar_list:
    image_tar = tarfile.open(image_tar_file, 'r')
    image_names = image_tar.getnames()
    with tarfile.open(os.path.join(output_path, image_tar_file.split('/')[-1]), 'w') as new_tar_file:
        for composite_tar_file in composite_tar_list:
            composite_tar = tarfile.open(composite_tar_file,'r')
            composite_names = composite_tar.getnames()
            for name in image_names:
                if name in composite_names and name not in new_tar_file.getnames():
                    new_tar_file.addfile(composite_tar.getmember(name),composite_tar.extractfile(name))
                elif name not in new_tar_file.getnames():
                    new_tar_file.addfile(image_tar.getmember(name),image_tar.extractfile(name))
                else:
                    pass
            composite_tar.close()
    new_tar_file.close()
    image_tar.close()

    
if __name__ == '__main__':
    # 栅格瓦片zip包路径
    raster_zip_path = 'C:/Users/Administrator/Desktop/beijing_raster'
    # 影像瓦片tar包路径
    image_tar_path = 'C:/Users/Administrator/Desktop/tar_test'
    # 合成瓦片输出路径
    output_path = 'C:/Users/Administrator/Desktop/new'
    # 指定进程数
    pool = Pool(processes=6)
    
    start_time = time.time()

    # 合成id匹配的栅格和影像瓦片
    print("-----------------------------------------")
    print("Start to composite raster and image tile.")
    temp_path = os.path.join(output_path, "temp")
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)
    raster_zip_list = get_raster_zip_list(raster_zip_path)
    partial_composite = partial(composite_tiles, image_tar_path, temp_path)
    pool.map_async(partial_composite, raster_zip_list)
    pool.close()
    pool.join()

    # 输出所有的影像瓦片
    image_tar_list = get_image_tar_list(image_tar_path)
    partial_roll = partial(roll_all_image_tiles, temp_path, output_path)
    pool.map_async(partial_roll, image_tar_list)
    pool.close()
    pool.join()
    # roll_all_image_tiles(image_tar_path, temp_path, output_path)

    # 删除临时文件
    shutil.rmtree(temp_path)

    print("-----------------------------------------")
    print("Composite raster and image tile finished.")
    end_time = time.time()
    logging.info("Time used: " + str(round((end_time - start_time)/60,3)) + "min.") 