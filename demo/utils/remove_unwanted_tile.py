# -*- encoding: utf-8 -*-

'''
@File    :   remove_unwanted_tile.py
@Time    :   2022/07/08 09:20:52
@Author  :   Lee
@Version :   1.0
@License :   (C)Copyright Cennavi, Li Wei
@Desc    :   None
'''


import os
import io
import time
import tarfile

import pandas as pd


def get_tile_id_list(excel_path):
    df = pd.read_excel(excel_path,sheet_name='Sheet1',header=None)
    tile_id_list = df[0].tolist()
    return tile_id_list


def remove_tile(tar_path,new_tar_path,tile_id_list):
    for root, dirs, files in os.walk(tar_path):
        for file in files:
            if file.endswith(".tar"):
                print("Remove tile from: %s. "%(file))
                tar_file = tarfile.open(os.path.join(root, file))
                members = tar_file.getmembers()
                with tarfile.open(os.path.join(new_tar_path, file.split(".")[0]+".tar"), 'w') as tar:
                    for member in members:
                        tile_id = (member.name.split("/")[-1]).split(".")[0]
                        if tile_id in tile_id_list:
                            print("  --remove tile: %s "%(tile_id))
                        else:
                            image = tar_file.extractfile(member)
                            image = image.read()
                            tarinfo = tarfile.TarInfo(name=member.name)
                            tarinfo.size = len(image)
                            tar.addfile(tarinfo=tarinfo, fileobj=io.BytesIO(image)) 
                tar.close()
    del root, dirs, files

if __name__ == '__main__':
    # 需要剔除的瓦片id列表
    excel_path = r'E:\Coding\Python\Python-RS-Image-Interpretation\demo\utils\tileslist.xlsx'
    # tar包路径
    tar_path = r'C:\Users\Administrator\Desktop\hefei'
    # 新的tar包路径
    new_tar_path = r'C:\Users\Administrator\Desktop\new'

    start_time = time.time()
    tile_id_list = get_tile_id_list(excel_path)
    remove_tile(tar_path,new_tar_path,tile_id_list)
    end_time = time.time()
    print("Time used: " + str(round((end_time - start_time), 2)) + " seconds")