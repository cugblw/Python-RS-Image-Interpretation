# -*- encoding: utf-8 -*-

'''
@File    :   cal_tile_range.py
@Time    :   2022/06/15 05:57:23
@Author  :   Lee
@Version :   1.0
@License :   (C)Copyright Cennavi, Li Wei
@Desc    :   None
'''


import os
import math
import time
import pymorton as pm
from itertools import chain

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

def check_tile_exist(zoom, x, y, tile_dir):
    """检查瓦片是否存在"""
    tile_name = generate_file_name("satellite", zoom, x, y)
    if os.path.exists(os.path.join(tile_dir, tile_name)):
        return True
    else:
        return False

def calculate_tile_xyz_recusively(zoom, x, y,zoom_max,tile_dir,morton_dict):
    """递归计算瓦片编号,查询瓦片是否存在"""
    if zoom > zoom_max:
        return
    
    bit_code = ''
    if check_tile_exist(zoom, x, y, tile_dir):
        bit_code = '1'
    else:
        bit_code = '0'
    # tile_id = str(zoom)+"_"+str(x)+"_"+str(y)
    # with open(tile_index, "a+") as f:
    #     f.write(tile_name + "\n")
    if zoom > 8:
        k = zoom-10
        i = x -int(x/2**k)*(2**k)
        j = y -int(y/2**k)*(2**k)        
        morton_code = pm.interleave3(i,j,k)
        morton_dict[morton_code] = bit_code
    else:
        morton_code = pm.interleave3(x,y,zoom)
    #  morton_dict[str(morton_code)].append(tile_name)
        morton_dict[morton_code] = bit_code
    
    calculate_tile_xyz_recusively(zoom + 1, x * 2, y * 2, zoom_max,tile_dir,morton_dict)
    calculate_tile_xyz_recusively(zoom + 1, x * 2 + 1, y * 2, zoom_max,tile_dir,morton_dict)
    calculate_tile_xyz_recusively(zoom + 1, x * 2, y * 2 + 1, zoom_max,tile_dir,morton_dict)
    calculate_tile_xyz_recusively(zoom + 1, x * 2 + 1, y * 2 + 1, zoom_max,tile_dir,morton_dict)




if __name__ == "__main__":
    start_time = time.time()
    if os.path.exists("tile_index.txt"):
        os.remove("tile_index.txt")
    # pool = Pool(processes=8)
    # pool.apply(calculate_tile_xyz, (0, 0, 0, 8, "tile_index.txt"))
    # pool.close()
    start_zoom = 0
    end_zoom = 3
    morton_dict = {}
    tile_dir = r"C:\Users\Administrator\Desktop\tile_index"
    calculate_tile_xyz_recusively(start_zoom, 0, 0, end_zoom,tile_dir,morton_dict)
    morton_dict = dict(sorted(morton_dict.items(), key=lambda x: x[0]))
    print(morton_dict)
    # print(len(morton_dict))
    bits_chain = list(chain(*morton_dict.values()))
    # calculate_tile_xyz(0,0,0,8,'tile_index.txt')
    # with open('tile_index.txt','r') as f:
    #     print(len(f.read()))

    print(len("".join(bits_chain)))
    # with open('tile_index.txt','w') as f:
    #     for item in morton_dict:
    #         f.write(item[1]+"\n")
    with open('tile_index.txt','w') as f:
        for item in bits_chain:
            f.write(item)
    end_time = time.time()
    print("time:",str((end_time - start_time)) + "s")
