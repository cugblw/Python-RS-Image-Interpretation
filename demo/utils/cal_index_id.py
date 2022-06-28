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
import tarfile

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


def get_tile_id_dict_from_ruleless_tar(tar_path):
    """
    获取无规则tar包瓦片编号
    """
    # get all tar_id list
    tar_list = []
    tile_id_list = []
    for file_name in os.listdir(tar_path):
        if file_name.endswith('.tar'):
            tar_list.append(os.path.join(tar_path,file_name))

    tile_id_dict = {}
    for tar_file in tar_list:
        zoom_list = []
        with tarfile.open(tar_file,'r') as tar:
            members = tar.getnames()
            for member in members:
                try:
                    zoom = int(member.split('/')[1])
                    if zoom not in zoom_list and zoom >= 10:
                        zoom_list.append(zoom)
                except:
                    continue
            zoom_min = min(zoom_list)
            for member in members:
                try:
                    zoom = int(member.split('/')[1])
                    if zoom == zoom_min:
                        tile_id = member.split('/')[-1].split('.')[0]
                        if tile_id not in tile_id_list:
                            tile_id_list.append(tile_id)
                        if tile_id not in tile_id_dict.keys():
                            tile_id_dict[tile_id] = []
                            tile_id_dict[tile_id].append(tar_file)
                        else:
                            tile_id_dict[tile_id].append(tar_file)
                except:
                    continue
        tar.close()
    return tile_id_dict


def get_tar_list_dict_from_ruleless_tar(tar_path):
    """
    获取tar包列表
    """
    tile_id_dict = get_tile_id_dict_from_ruleless_tar(tar_path)
    tar_list_dict = {}
    for tile_id in tile_id_dict.keys():
        if '_' not in tile_id:
            continue
        tile_xyz = tile_id.split('_')

        if int(tile_xyz[0]) == 10:
            if tile_id not in tar_list_dict.keys():
                tar_list_dict[tile_id] = []
                tar_list_dict[tile_id].append(tile_id_dict[tile_id])
            else:
                tar_list_dict[tile_id].append(tile_id_dict[tile_id])
        
        elif int(tile_xyz[0]) > 10:
            x_min,x_max,y_min,y_max,z = tc.high_room_tile_to_low_room_tile(int(tile_xyz[1]),int(tile_xyz[2]),int(tile_xyz[0]),10)
            tile_id_target = str(z) + '_' + str(x_min) + '_' + str(y_min)

            if tile_id_target not in tar_list_dict.keys():
                tar_list_dict[tile_id_target] = []
                for tar_file in tile_id_dict[tile_id]:
                    tar_list_dict[tile_id_target].append(tar_file)
            else:
                for tar_file in tile_id_dict[tile_id]:
                    tar_list_dict[tile_id_target].append(tar_file)
        else:
            pass

    for tar_id in tar_list_dict.keys():
        tar_list_dict[tar_id] = list(set(tar_list_dict[tar_id]))
    
    return tar_list_dict


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
            for x in range(x_min,x_max+1):
                for y in range(y_min,y_max+1):
                    tile_id_list_convert.append(str(z)+'_'+str(x)+'_'+str(y))

        else:
            x_min,x_max,y_min,y_max,z = tc.low_room_tile_to_high_room_tile(int(tile_xyz[1]),int(tile_xyz[2]),int(tile_xyz[0]),target_zoom)
            for x in range(x_min,x_max+1):
                for y in range(y_min,y_max+1):
                    tile_id_list_convert.append(str(z)+'_'+str(x)+'_'+str(y))
    
    # remove repeat tile_id
    tile_id_list_convert = list(dict.fromkeys(tile_id_list_convert))
    return tile_id_list_convert


if __name__ == '__main__':
    tile_list = get_tile_id_from_tar(r'C:\Users\Administrator\Desktop\05m')
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