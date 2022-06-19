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

import pymorton as pm

import tile_lon_lat_convert as tc


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


def generate_tar_list_by_tileId(tile_id,tar_dir):
    """根据瓦片编号生成tar包列表"""
    zoom_index_list = [8, 10, 12]
    zoom = int(tile_id.split('_')[0])
    x = int(tile_id.split('_')[1])
    y = int(tile_id.split('_')[2])
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

def check_tile_exist_dir(zoom, x, y, tile_dir):
    """检查瓦片是否存在文件夹中"""
    tile_name = generate_file_name("satellite", zoom, x, y)
    
    if os.path.exists(os.path.join(tile_dir, tile_name)):
        return True
    else:
        return False


def check_tile_exist_tar(zoom, x, y, members_list):
    """检查瓦片是否存在tar包中"""
    tile_name = generate_file_name("satellite", zoom, x, y).replace("\\","/")
    
    if tile_name in members_list:
        return True
    else:
        return False


def search_tile_from_dir_recursively(zoom, x, y,zoom_max,tile_dir,morton_dict):
    """递归计算瓦片编号,查询瓦片是否存在"""
    if zoom > zoom_max:
        return

    bit_code = ''
    if check_tile_exist_dir(zoom, x, y, tile_dir):
        bit_code = '1'

    else:
        bit_code = '0'

    if zoom > 8:
        k = zoom-10
        i = x -int(x/2**k)*(2**k)
        j = y -int(y/2**k)*(2**k)      
        morton_code = pm.interleave(i,j)+4**k
        morton_dict[morton_code] = bit_code
        
    else:
        morton_code = pm.interleave(x,y) + 4**(zoom)
        morton_dict[morton_code] = bit_code
    
    search_tile_from_dir_recursively(zoom + 1, x * 2, y * 2, zoom_max,tile_dir,morton_dict)
    search_tile_from_dir_recursively(zoom + 1, x * 2 + 1, y * 2, zoom_max,tile_dir,morton_dict)
    search_tile_from_dir_recursively(zoom + 1, x * 2, y * 2 + 1, zoom_max,tile_dir,morton_dict)
    search_tile_from_dir_recursively(zoom + 1, x * 2 + 1, y * 2 + 1, zoom_max,tile_dir,morton_dict)


def search_tile_from_tar_recursively(zoom, x, y, zoom_max,members_list,morton_dict):
    """递归计算瓦片编号,查询瓦片是否存在"""
    if zoom > zoom_max:
        return

    bit_code = ''
    if check_tile_exist_tar(zoom, x, y, members_list):
        bit_code = '1'
        
    else:
        bit_code = '0'

    if zoom > 8:
        k = zoom-10
        i = x -int(x/2**k)*(2**k)
        j = y -int(y/2**k)*(2**k)        
        morton_code = pm.interleave(i,j)+4**k
        # if x == 206545 and y == 102859:
        #     print( "x:",x,"y:",y,"zoom:",zoom,"morton_code:",morton_code) 
        # tile_id = str(zoom)+"_"+str(x)+"_"+str(y)
        morton_dict[morton_code] = bit_code
        
    else:
        morton_code = pm.interleave(x,y) + 4**(zoom)
        morton_dict[morton_code] = bit_code
    
    search_tile_from_tar_recursively(zoom + 1, x * 2, y * 2, zoom_max,members_list,morton_dict)
    search_tile_from_tar_recursively(zoom + 1, x * 2 + 1, y * 2, zoom_max,members_list,morton_dict)
    search_tile_from_tar_recursively(zoom + 1, x * 2, y * 2 + 1, zoom_max,members_list,morton_dict)
    search_tile_from_tar_recursively(zoom + 1, x * 2 + 1, y * 2 + 1, zoom_max,members_list,morton_dict)


def calculate_global_tile_xyz_recursively(zoom, x, y, zoom_max,morton_dict):
    if zoom > zoom_max:
        return
    bit_code = '1'
    k = zoom-10
    i = x -int(x/2**k)*(2**k)
    j = y -int(y/2**k)*(2**k)
    morton_code = pm.interleave(i,j)+4**k
    morton_dict[morton_code] = bit_code

    calculate_global_tile_xyz_recursively(zoom + 1, x * 2, y * 2, zoom_max,morton_dict)
    calculate_global_tile_xyz_recursively(zoom + 1, x * 2 + 1, y * 2, zoom_max,morton_dict)
    calculate_global_tile_xyz_recursively(zoom + 1, x * 2, y * 2 + 1, zoom_max,morton_dict)
    calculate_global_tile_xyz_recursively(zoom + 1, x * 2 + 1, y * 2 + 1, zoom_max,morton_dict)



if __name__ == "__main__":
    # start_time = time.time()
    # if os.path.exists("tile_index.txt"):
    #     os.remove("tile_index.txt")
    # # pool = Pool(processes=8)
    # # pool.apply(calculate_tile_xyz, (0, 0, 0, 8, "tile_index.txt"))
    # # pool.close()
    # start_zoom = 0
    # end_zoom = 3
    # morton_dict = {}
    # tile_dir = r"C:\Users\Administrator\Desktop\tile_index"
    # search_tile_from_dir_recursively(start_zoom, 0, 0, end_zoom,tile_dir,morton_dict)
    # morton_dict = dict(sorted(morton_dict.items(), key=lambda x: x[0]))
    # print(morton_dict)
    # # print(len(morton_dict))
    # bits_chain = list(chain(*morton_dict.values()))
    # # calculate_tile_xyz(0,0,0,8,'tile_index.txt')
    # # with open('tile_index.txt','r') as f:
    # #     print(len(f.read()))

    # print(len("".join(bits_chain)))
    # # with open('tile_index.txt','w') as f:
    # #     for item in morton_dict:
    # #         f.write(item[1]+"\n")
    # with open('tile_index.txt','w') as f:
    #     for item in bits_chain:
    #         f.write(item)
    # end_time = time.time()
    # print("time:",str((end_time - start_time)) + "s")

    tile_id = "10_806_401"
    tar_dir = r"C:\Users\cugbl\Desktop\05m"
    tar_list = generate_tar_list_by_tileId(tile_id, tar_dir)
    print(tar_list)

    # tile_exist =check_tile_exist_tar(17,103296,51418,tar_list)
    tile_exist =check_tile_exist_tar(17,103273,51422,tar_list)
    print(tile_exist)
