#!/usr/bin/python3
# -*- encoding: utf-8 -*-

'''
@File    :   image_processing.py
@Time    :   2022/07/19 13:56:58
@Author  :   Weil Lee
@Version :   1.0
@Email   :   cugblw2014@outlook.com
@Desc    :   None
'''


import os
from osgeo import gdal
from osgeo_utils import gdal_merge as gm


def create_mosaic_image(intersecting_image_list, update_image_path, output_path):
    """
    create mosaic image
    :param intersecting_image_list:
    :param update_image_path:
    :param output_path:
    :return:
    """
    intersecting_image_list.append(update_image_path)
    # gm.main(['', '-o', output_path, '-of', 'GTiff', '-n', '0', '-a_nodata', 
    #          '0', '-co','BIGTIFF=YES', '-co', 'TILED=YES', '-co', 'NUM_THREADS=8', 
    #          '-co', 'INTERLEAVE=PIXEL', '-co', 'PHOTOMETRIC=rgb'] + intersecting_image_list)
    
    vrt_options = gdal.BuildVRTOptions(srcNodata=0,VRTNodata=0)
    gdal.BuildVRT("mosaic.vrt", intersecting_image_list, options = vrt_options)

    mosaic_command = 'gdal_translate -of GTiff -co NUM_THREADS=16 -co BIGTIFF=YES \
                      -co INTERLEAVE=PIXEL -co PHOTOMETRIC=rgb mosaic.vrt ' + output_path
    os.system(mosaic_command)
    os.remove('mosaic.vrt')


def clip_image(image_path, output_path, clip_bbox):
    """
    clip image
    :param image_path:
    :param clip_geometry:
    :return:
    """
    # projWin = [clip_bbox[0], clip_bbox[3], clip_bbox[2], clip_bbox[1]]
    # gdal.Translate(output_path, image_path, format='GTiff', projWin=projWin, 
    #                options=['-co', 'BIGTIFF=YES', '-co', 'TILED=YES', '-co', 'NUM_THREADS=8',
    #                         '-co', 'INTERLEAVE=PIXEL', '-co', 'PHOTOMETRIC=rgb'])

    clip_command = 'gdal_translate -of GTiff -projWin {} {} {} {} -co NUM_THREADS=16 -co BIGTIFF=YES \
                        -co INTERLEAVE=PIXEL -co PHOTOMETRIC=rgb '.format(clip_bbox[0], clip_bbox[3],
                        clip_bbox[2], clip_bbox[1]) + image_path + ' ' + output_path
    os.system(clip_command)