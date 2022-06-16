# -*- encoding: utf-8 -*-

'''
@File    :   tile_index_parser.py
@Time    :   2022/06/15 16:02:56
@Author  :   Lee
@Version :   1.0
@License :   (C)Copyright Cennavi, Li Wei
@Desc    :   None
'''

import os
import tile_lon_lat_convert as tc
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
        start_zoom = header_info[0]
        end_zoom = header_info[1]
        print("start_zoom:",start_zoom,"end_zoom:",end_zoom)
        if end_zoom == 14:
            print("there is no current tile, use its parent tile with zoom equal 14.")
            x_parent = int(x>>(zoom-14))
            y_parent = int(y>>(zoom-14))
            zoom_parent = 14
            tile_path = os.path.join(tile_dir,generate_file_name("satellite", zoom_parent, x_parent, y_parent))
        elif zoom >= start_zoom or zoom <= end_zoom:
            tile_path = os.path.join(tile_dir,generate_file_name("satellite", zoom, x, y))
            index_data = bs.read_index_data(index_file)
            # index_data_zoom = index_data[]
            print(len(index_data))
        else:
            pass

        
        
    #     elif zoom > end_zoom and end_zoom > 18:

    
    # tile_id_list = []
    # for i in range(zoom+1):
    #     for j in range(2**i):
    #         for k in range(2**i):
    #             tile_id_list.append(str(i)+'_'+str(j)+'_'+str(k))
    # return tile_id_list

if __name__ == '__main__':
    # tile_dir = r"C:\Users\Administrator\Desktop\tile_index"
    # index_dir = r"C:\Users\Administrator\Desktop\tile_index\satellite\index"

    # # request_tile(14,12908,6426,tile_dir,index_dir)
    # tile_exist = request_tile(15,25817,12853,tile_dir,index_dir)
    index_file = r"C:\Users\Administrator\Desktop\tile_index\satellite\index"