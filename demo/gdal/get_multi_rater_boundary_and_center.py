import math
import os
import sys
from osgeo import gdal, ogr


def get_file_path(geotiff_dir):
    for root, dirs, files in os.walk(geotiff_dir):
        for file in files:
            geotiff_path = os.path.join(geotiff_dir,file)
            print(geotiff_path)


def get_geotiff_extent(geotiff_path):
    dataset = gdal.Open(geotiff_path)
    lon_min, xpixel, _, lat_max, _, ypixel = dataset.GetGeoTransform()
    width, height = dataset.RasterXSize, dataset.RasterYSize
    lon_max = lon_min + width * xpixel
    lat_min = lat_max + height * ypixel
    extent = [lon_min,lat_min,lon_max,lat_max]
    del dataset
    return extent

def get_center_coordinate(extent):
    # center = []
    lon_mean = (extent[0] + extent[2])/2
    lat_mean = (extent[1] + extent[3])/2
    center = [lon_mean,lat_mean]
    return center

def get_multi_geotiff_center_coordinate(geotiff_dir):
    lon_center_list = []
    lat_center_list = []
    for root, dirs, files in os.walk(geotiff_dir):
        for file in files:
            geotiff_path = os.path.join(geotiff_dir,file)
            extent = get_geotiff_extent(geotiff_path)
            center = get_center_coordinate(extent)
            lon_center_list.append(center[0])
            lat_center_list.append(center[1])
    lon_mean = (min(lon_center_list) + max(lon_center_list))/2
    lat_mean = (min(lat_center_list) + max(lat_center_list))/2
    center_coordinate = [lon_mean, lat_mean]
    return center_coordinate

def get_multi_geotiff_extent(geotiff_dir):
    lon_min_list = []
    lon_max_list = []
    lat_min_list = []
    lat_max_list = []

    for root, dirs, files in os.walk(geotiff_dir):
        for file in files:
            geotiff_path = os.path.join(geotiff_dir,file)
            extent = get_geotiff_extent(geotiff_path)
            lon_min_list.append(extent[0])
            lat_min_list.append(extent[1])
            lon_max_list.append(extent[2])
            lat_max_list.append(extent[3])
    lon_min = min(lon_min_list)
    lat_min = min(lat_min_list)
    lon_max = max(lon_max_list)
    lat_max = max(lat_max_list)
    extent = [lon_min,lat_min,lon_max,lat_max]
    return extent

center_coordinate = get_multi_geotiff_center_coordinate(r"C:\Users\Administrator\Desktop\Image_Src\2m")
extent_boundary = get_multi_geotiff_extent(r"C:\Users\Administrator\Desktop\Image_Src\2m")
print(center_coordinate)
print(extent_boundary)