import os
import tarfile

import tile_lon_lat_convert as tc


def get_tile_id_from_ruleless_tar(tar_path):
    """
    获取无规则tar包瓦片编号
    """
    # get all tar_id list
    tar_list = []
    tile_id_list = []
    for file_name in os.listdir(tar_path):
        if file_name.endswith('.tar'):
            tar_list.append(os.path.join(tar_path,file_name))

    zoom_list = []
    tile_id_dict = {}
    for tar_file in tar_list:
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
                            tile_id_dict[tile_id] = tar_file
                except:
                    continue
        tar.close()
    return tile_id_dict

def get_tar_list_from_tile_id_dict(tile_id_dict):
    """
    获取tar包列表
    """
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
                tar_list_dict[tile_id_target].append(tile_id_dict[tile_id])
            else:
                tar_list_dict[tile_id_target].append(tile_id_dict[tile_id])
        else:
            pass

    for tar_id in tar_list_dict.keys():
        tar_list_dict[tar_id] = list(set(tar_list_dict[tar_id]))
    
    print(tar_list_dict)
    print(len(tar_list_dict))
    return tar_list_dict

        



if __name__ == '__main__':
    tar_path = r"C:\Users\Administrator\Desktop\tar_test"
    tile_id_dict = get_tile_id_from_ruleless_tar(tar_path)
    get_tar_list_from_tile_id_dict(tile_id_dict)