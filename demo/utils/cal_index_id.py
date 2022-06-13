import os
import re
import tarfile

from numpy import tile
import tile_lon_lat_convert as tc


def get_tile_id_from_tar(tar_path):
    """
    获取tar包瓦片编号
    """
    tile_id_list = []
    for file_name in os.listdir(tar_path):
        if file_name.endswith('.tar'):
            tileId = file_name.split('.')[0]
            tile_id_list.append(tileId)
    # tar = tarfile.open(tar_path)
    # tar_list = tar.getmembers()
    return tile_id_list

def convert_tile_id(tile_id_list,target_zoom = 10):
    """
    转换瓦片编号
    """
    tile_id_list_convert = []
    for tile_id in tile_id_list:
        tile_xyz = tile_id.split('_')

        if int(tile_xyz[0]) == 10:
            tile_id_list_convert.append(tile_id)
            print(tile_id)
        
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
    tile_list = get_tile_id_from_tar(r'C:\Users\Administrator\Desktop\2m')
    tile_list_convert = convert_tile_id(tile_list)
    # print(tile_list)
    print(tile_list_convert)