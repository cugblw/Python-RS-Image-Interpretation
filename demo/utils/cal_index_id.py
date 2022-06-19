# -*- encoding: utf-8 -*-

'''
@File    :   cal_index_id.py
@Time    :   2022/06/15 05:55:20
@Author  :   Lee
@Version :   1.0
@License :   (C)Copyright Cennavi, Li Wei
@Desc    :   None
'''


import os

import tile_lon_lat_convert as tc


def get_tile_id_from_tar(tar_path):
    """
    获取tar包瓦片编号
    """
    # get all tar_id list
    tar_list = []
    tar_id_lower_list = []
    for file_name in os.listdir(tar_path):
        if file_name.endswith('.tar'):
            tar_id = file_name.split('.')[0]
            
            if "_" not in tar_id:
                pass
            
            else:
                if int(tar_id.split('_')[0]) >= 10:
                    tar_list.append(tar_id)
                    
                else:
                    tar_id_lower_list.append(tar_id)

    lower_zoom_list = []
    for tar_id in tar_id_lower_list:
        lower_zoom_list.append(int(tar_id.split('_')[0]))
    
    if len(lower_zoom_list) == 0:
        return tar_list

    max_zoom = max(lower_zoom_list)
    # get lower zoom tar_id list
    for tar_id in tar_id_lower_list:
        if tar_id.split('_')[0] != str(max_zoom):
            tar_id_lower_list.remove(tar_id)

    tar_list.extend(tar_id_lower_list)
    return tar_list


def convert_tile_id(tile_id_list,target_zoom = 10):
    """
    转换瓦片编号
    """
    tile_id_list_convert = []
    for tile_id in tile_id_list:
        if '_' not in tile_id:
            continue
        tile_xyz = tile_id.split('_')

        if int(tile_xyz[0]) == 10:
            tile_id_list_convert.append(tile_id)
        
        elif int(tile_xyz[0]) > 10:
            x_min,x_max,y_min,y_max,z = tc.high_room_tile_to_low_room_tile(int(tile_xyz[1]),int(tile_xyz[2]),int(tile_xyz[0]),target_zoom)
            for x in range(x_min,x_max):
                for y in range(y_min,y_max):
                    tile_id_list_convert.append(str(z)+'_'+str(x)+'_'+str(y))

        else:
            x_min,x_max,y_min,y_max,z = tc.low_room_tile_to_high_room_tile(int(tile_xyz[1]),int(tile_xyz[2]),int(tile_xyz[0]),target_zoom)
            for x in range(x_min,x_max):
                for y in range(y_min,y_max):
                    tile_id_list_convert.append(str(z)+'_'+str(x)+'_'+str(y))
    
    # remove repeat tile_id
    tile_id_list_convert = list(dict.fromkeys(tile_id_list_convert))
    return tile_id_list_convert


if __name__ == '__main__':
    tile_list = get_tile_id_from_tar(r'C:\Users\cugbl\Desktop\2m')
    tile_list_convert = convert_tile_id(tile_list)
    print(tile_list)
    print((tile_list_convert))

    # # list_test = ["8_23_45","8_45_87","6_45_32","6_23_32","6_23_45","3_21_32"]
    # list_test = ["1_0_0",'10_896_483', "12_0_0","13_0_0","14_0_0","15_0_0",'10_896_484',"16_0_0", "17_0_0",'10_896_485', '10_896_486', '10_896_487',"11_0_0"]
    # for tile_id in list_test:
    #     if int(tile_id.split('_')[0]) < 10:
    #         list_test.remove(tile_id)
    #     else:
    #         pass
    # print(list_test)