# -*- encoding: utf-8 -*-

'''
@File    :   get_image_metadata.py
@Time    :   2022/07/18 13:43:02
@Author  :   Lee
@Version :   1.0
@License :   (C)Copyright Cennavi, Li Wei
@Desc    :   None
'''


import math
import operator
import os

from osgeo import gdal
from osgeo import ogr
from osgeo import osr
from shapely.geometry import Polygon


def get_image_info(image_path):
    """
    get image information
    :param image_path: image path
    :return: image information
    """
    image_info_dict = gdal.Info(image_path, format='json')

    name = os.path.basename(image_info_dict['description'])
    path = image_info_dict['files'][0]
    coordinates = image_info_dict['wgs84Extent']['coordinates'][0]
    geometry = str(Polygon(coordinates))
    lowerLeft = list(image_info_dict['cornerCoordinates']['lowerLeft'])
    upperRight = list(image_info_dict['cornerCoordinates']['upperRight'])
    extent = "[{0}, {1}, {2}, {3}]".format(lowerLeft[0], lowerLeft[1], upperRight[0], upperRight[1])
    image_structure = image_info_dict['metadata']['IMAGE_STRUCTURE']['INTERLEAVE']
    width = image_info_dict['size'][0]
    height = image_info_dict['size'][1]
    crs = image_info_dict['coordinateSystem']['wkt'].split('\n')[-1].\
                                                     replace('ID["','').\
                                                     replace(']]','').\
                                                     replace('",',':').strip()
    bands = len(image_info_dict['bands'])
    resolution = str(__get_image_resolution(image_path)[0]) + 'm'
    format = image_info_dict['driverLongName']
    size = str(round(__get_file_size(image_path)/1024/1024,2)) + ' MB'
    pixel_depth = image_info_dict['bands'][0]['type']

    image_info = {'name': name,
                  'image_path': path,
                  'geometry': geometry,
                  'extent': extent,
                  'image_structure': image_structure,
                  'width': width,
                  'height': height,
                  'CRS': crs,
                  'band': bands,
                  'resolution': resolution,
                  'format': format,
                  'size': size,
                  'pixel_depth': pixel_depth}

    return image_info


def get_invalid_image_info(image_path, description):
    """
    :param image_path:
    :param description:
    :return: invalid image info
    """
    invalid_image_info = {}
    name = os.path.basename(image_path)
    path = image_path
    description = description
    invalid_image_info['name'] = name
    invalid_image_info['image_path'] = path
    invalid_image_info['description'] = description
    return invalid_image_info


def __get_file_size(file_path):
    file_size = os.path.getsize(file_path)
    return file_size


def __get_geotiff_epsg(img_path):
    dataset = gdal.Open(img_path)
    img_proj_info = osr.SpatialReference(dataset.GetProjection())
    epsg = img_proj_info.GetAttrValue('AUTHORITY', 1)
    return epsg


def __get_image_resolution(img_path):
    dataset = gdal.Open(img_path)
    epsg = __get_geotiff_epsg(img_path)
    if epsg != '4326':
        xres, yres = operator.itemgetter(1,5)(dataset.GetGeoTransform())
        if xres < 0:
            xres = -xres
        if yres < 0:
            yres = -yres
        return [xres, yres]
    else:
        xres, yres = operator.itemgetter(1,5)(dataset.GetGeoTransform())

        return __convert_resolution_wgs84([xres, yres])


def __convert_resolution_wgs84(resolution_xy):
    """wgs84"""
    xres, yres = resolution_xy[0], resolution_xy[1]
    if xres < 0:
        xres = -xres
    if yres < 0:
        yres = -yres
    R = 6371393
    L = 2 * math.pi * R
    xres = xres * L / 360.0
    yres = yres * L / 360.0
    return [round(xres,2), round(yres,2)]


if __name__ == "__main__":
    geotiff = r"D:\lanzhou_2m.tif"
    image_info_dict = get_image_info(geotiff)
    print(image_info_dict)