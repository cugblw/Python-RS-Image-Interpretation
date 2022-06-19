import math
import os
import re
import operator
from osgeo import gdal
from get_image_info import get_metadata


def get_image_size(img_path):
    metadata_dict = get_metadata(img_path)
    # print(metadata_dict['size'])
    size = metadata_dict['size']
    return size

def get_image_resolution(img_path):
    dataset = gdal.Open(img_path)

    xres, yres = operator.itemgetter(1,5)(dataset.GetGeoTransform())
    return [xres, yres]
    # print(xres,yres)

def convert_resolution_wgs84(resolution_xy):
    """wgs84"""
    xres, yres = resolution_xy[0], resolution_xy[1]
    if xres < 0:
        xres = -xres
    if yres < 0:
        yres = -yres
    R = 6371000
    L = 2 * math.pi * R
    xres = xres * L / 360.0
    yres = yres * L / 360.0
    return [round(xres,1), round(yres,1)]

if __name__ == '__main__':

    size = get_image_size(r"E:\Data\test\lanzhou_2m.tif")
    resolution_xy = get_image_resolution(r"E:\Data\test\lanzhou_2m.tif")
    print(size)
    print(resolution_xy)
    resolution_xy = convert_resolution_wgs84(resolution_xy)
    print(resolution_xy)
