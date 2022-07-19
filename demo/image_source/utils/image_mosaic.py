#!/usr/bin/python3
# -*- encoding: utf-8 -*-

'''
@File    :   image_mosaic.py
@Time    :   2022/07/19 13:56:58
@Author  :   Weil Lee
@Version :   1.0
@Email   :   cugblw2014@outlook.com
@Desc    :   None
'''


from osgeo import gdal
from osgeo_utils import gdal_merge as gm

from utils.image_geometry import get_intersecting_images


def create_mosaic_image(update_image_path, db_file, output):
    intersecting_image_list = get_intersecting_images(update_image_path, db_file)
    print(intersecting_image_list)
    # files_list = [r"C:\Users\Administrator\Desktop\local_update\1_A2包_5_10_preview.tif",r"C:\Users\Administrator\Desktop\local_update\1_A2包_5_9_preview.tif",r"C:\Users\Administrator\Desktop\local_update\1_A2包_5_5_preview.tif",r"C:\Users\Administrator\Desktop\local_update\1_A2包_5_6_preview.tif"]
    intersecting_image_list.append(update_image_path)
    print(intersecting_image_list)
    gm.main(['', '-o', output, '-of', 'GTiff', '-n', '0', '-a_nodata', 
             '0', '-co','BIGTIFF=YES', '-co', 'TILED=YES', '-co', 'NUM_THREADS=8', 
             '-co', 'INTERLEAVE=PIXEL', '-co', 'PHOTOMETRIC=rgb'] + intersecting_image_list)


if __name__ == "__main__":
    db_file = r"demo\image_source\database\image_source_infomation.db"
    output = r"C:\Users\Administrator\Desktop\local_update\mosaic.tif"
    update_image_path = r"C:\Users\Administrator\Desktop\2_贵阳替云_preview.tif"
    # intersecting_image_list = get_intersecting_images(update_image_path, db_file, output)
    create_mosaic_image(update_image_path, db_file, output)
