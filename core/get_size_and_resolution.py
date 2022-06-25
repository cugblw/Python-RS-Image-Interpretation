import os
import math
import operator

from osgeo import gdal

from get_image_info import get_metadata,get_geotiff_epsg


def get_image_size(img_path):
    metadata_dict = get_metadata(img_path)
    # print(metadata_dict['size'])
    size = metadata_dict['size']
    return size

def get_image_resolution(img_path):
    dataset = gdal.Open(img_path)
    epsg = get_geotiff_epsg(img_path)
    if epsg != '4326':
        xres, yres = operator.itemgetter(1,5)(dataset.GetGeoTransform())
        if xres < 0:
            xres = -xres
        if yres < 0:
            yres = -yres
        return [xres, yres]
    else:
        xres, yres = operator.itemgetter(1,5)(dataset.GetGeoTransform())

        return convert_resolution_wgs84([xres, yres])
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

    size = get_image_size(r"C:\Users\Administrator\Desktop\data\beijing_clip.tif")
    resolution_xy = get_image_resolution(r"C:\Users\Administrator\Desktop\data\beijing_clip.tif")
    print(size)
    print(resolution_xy)
    # resolution_xy = convert_resolution_wgs84(resolution_xy)
    # print(resolution_xy)
