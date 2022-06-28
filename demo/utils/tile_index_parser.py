# -*- encoding: utf-8 -*-

'''
@File    :   tile_index_parser.py
@Time    :   2022/06/15 16:02:56
@Author  :   Lee
@Version :   1.0
@License :   (C)Copyright Cennavi, Li Wei
@Desc    :   解析索引文件
'''

import math
import os
import pymorton as pm
import build_index_structure as bs


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


def get_index(zoom,x,y,index_dir):
    """
    计算瓦片索引文件
    """
    if zoom < 10:
        return 
        
    x_index = int(x>>(zoom-10))
    y_index = int(y>>(zoom-10))
    z_index = 10
    # (x_min, x_max, y_min, y_max, z_low) = tc.high_room_tile_to_low_room_tile(x,y,zoom,10)
    # print(x_min,x_max,y_min,y_max,z_low)
    index_file = os.path.join(index_dir,str(z_index)+'_'+str(x_index)+'_'+str(y_index)+'.idx')
    
    if os.path.exists(index_file):
        print("find index:",index_file)
        return index_file
        
    else:
        print("index not found.")
        return None


def get_parent_tile(zoom,x,y):
    """
    获取父瓦片
    """
    if zoom <= 14:
        return None
        
    else:
        x_index = int(x>>(zoom-10))
        y_index = int(y>>(zoom-10))
        z_index = 10
        return str(z_index)+'_'+str(x_index)+'_'+str(y_index)


def search_partent_tile_recursively(zoom,x,y,tile_dir,index_dir,index_data,zoom_end=14):
    if zoom < zoom_end:
        print("there is no tile for the request.")
        return None
        
    tile_path = os.path.join(tile_dir,generate_file_name("satellite", zoom, x, y))
    before_zoom_bytes_length = bs.sum_bytes_length(4,0,zoom-11)
    zoom_bytes_length = bs.cal_bytes_length(4,(zoom-10))
    morton_code = pm.interleave(x-(int(x>>(zoom-10)<<(zoom-10))),y-(int(y>>(zoom-10)<<(zoom-10))))
    zoom_index_data = index_data[before_zoom_bytes_length:before_zoom_bytes_length+zoom_bytes_length][math.ceil(morton_code/8)]
    tile_bit = bin(zoom_index_data)[2:].zfill(8)[morton_code - int(morton_code/8)*8]
    
    if tile_bit == '1':
        print("find tile:",tile_path)
        return tile_path
        
    else:
        search_partent_tile_recursively(zoom-1,x,y,tile_dir,index_dir,index_data,zoom_end)


def request_tile(zoom,x,y,tile_dir,index_dir):
    """
    搜索瓦片是否存在，不存在则向上请求父级瓦片，直到找到瓦片为止
    """
    if zoom <= 14:
        tile_path = os.path.join(tile_dir,generate_file_name("satellite", zoom, x, y))
        
        if os.path.exists(tile_path):
            print("find tile:",tile_path)
            return tile_path
            
        else:
            print("tile not found.")
            return None
            
    else:
        index_file = get_index(zoom,x,y,index_dir)
        header_info = bs.read_index_header(index_file)
        index_data = bs.read_index_data(index_file)
        start_zoom = header_info[0]
        end_zoom = header_info[1]
        print("start_zoom:",start_zoom,"end_zoom:",end_zoom)
        
        if end_zoom == 14:
            print("there is no current tile, use its parent tile with zoom equal 14.")
            x_parent = int(x>>(zoom-14))
            y_parent = int(y>>(zoom-14))
            zoom_parent = 14
            tile_path = os.path.join(tile_dir,generate_file_name("satellite", zoom_parent, x_parent, y_parent))
            
        elif zoom >= start_zoom and zoom <= end_zoom:
            # print(len(index_data))
            # tile_path = os.path.join(tile_dir,generate_file_name("satellite", zoom, x, y))
            # before_zoom_length = bs.sum_bytes_length(4,0,zoom-11)
            # zoom_bits_length = bs.cal_bytes_length(4,(zoom-10))
            # # index_data_zoom = index_data[]
            # # print(x-(int(x>>(zoom-10)<<(zoom-10))),y-(int(y>>(zoom-10)<<(zoom-10))))
            # morton_code = pm.interleave(x-(int(x>>(zoom-10)<<(zoom-10))),y-(int(y>>(zoom-10)<<(zoom-10))))
            # # print(pm.interleave(x-(int(x>>(zoom-10)<<(zoom-10))),y-(int(y>>(zoom-10)<<(zoom-10)))))
            # # print(len(index_data))
            # # print(zoom_bits_length)
            # # print(before_zoom_length)
            # zoom_index_data = index_data[before_zoom_length:before_zoom_length+zoom_bits_length][math.ceil(morton_code/8)]
            # tile_bit = bin(zoom_index_data)[2:].zfill(8)[morton_code - int(morton_code/8)*8]
            # if tile_bit == '1':
            #     print("find tile:",tile_path)
            #     return tile_path
            # else:
            #     search_parent_tile = get_parent_tile(zoom,x,y)

            # print(bin(zoom_index_data)[2:].zfill(8)[morton_code - int(morton_code/8)*8])
            tile_path = search_partent_tile_recursively(zoom,x,y,tile_dir,index_dir,index_data)
            return tile_path
            
        else:
            x_parent = int(x>>(zoom-18))
            y_parent = int(y>>(zoom-18))
            zoom_parent = 18
            tile_path = search_partent_tile_recursively(zoom_parent,x_parent,y_parent,tile_dir,index_dir,index_data)
            return tile_path

        
if __name__ == '__main__':
    tile_dir = r"C:\Users\Administrator\Desktop\tar_test"
    index_dir = r"C:\Users\Administrator\Desktop\index\test"

    # # request_tile(14,12908,6426,tile_dir,index_dir)
    # tile_exist = request_tile(16,51643,25721,tile_dir,index_dir)
    # tile_path = request_tile(18,206545,102854,tile_dir,index_dir)
    tile_path = request_tile(18, 215517, 98789,tile_dir,index_dir)
    print(tile_path)
    # index_file = r"C:\Users\Administrator\Desktop\tile_index\satellite\index"