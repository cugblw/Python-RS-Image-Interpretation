import os
import re
import operator
from osgeo import gdal
from obtain_metadata import get_metadata


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

if __name__ == '__main__':

    size = get_image_size(r"C:\Users\Administrator\Desktop\Image_Src\2m\mjl_C2_ljsx.tif")
    resolution = get_image_resolution(r"C:\Users\Administrator\Desktop\Image_Src\2m\mjl_C2_ljsx.tif")
    print(size)
    print(resolution)