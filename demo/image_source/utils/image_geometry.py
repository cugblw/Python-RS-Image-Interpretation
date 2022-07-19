# -*- encoding: utf-8 -*-

'''
@File    :   image_geometry.py
@Time    :   2022/07/19 16:05:26
@Author  :   Lee
@Version :   1.0
@License :   (C)Copyright Cennavi, Li Wei
@Desc    :   None
'''


import os

from osgeo import gdal
from osgeo import ogr
from shapely import wkt
from shapely.geometry import Polygon
import geopandas as gpd

from database_manipulation import select_data
# from utils.database_manipulation import select_data


def get_image_geometry(image_path):
    """
    get image geometry
    :param image_path:
    :return: geometry
    """
    image_info_dict = gdal.Info(image_path, format='json')
    coordinates = image_info_dict['wgs84Extent']['coordinates'][0]
    geometry = str(Polygon(coordinates))
    return geometry


def clip_image_by_geometry(image_path, clip_geometry):
    """
    clip image by geometry
    :param image_path:
    :param clip_geometry:
    :return:
    """
    image_info_dict = gdal.Info(image_path, format='json')
    coordinates = image_info_dict['wgs84Extent']['coordinates'][0]
    geometry = str(Polygon(coordinates))
    intersection = ogr.CreateGeometryFromWkt(clip_geometry).Intersection(ogr.CreateGeometryFromWkt(geometry))
    if intersection.GetArea() > 0:
        return True
    else:
        return False


def get_intersecting_images(update_image_path, db_file):
    """
    geometry intersect
    :param geometry1:
    :param geometry2:
    :return:
    """
    update_image_geometry = get_image_geometry(update_image_path)
    print(type(update_image_geometry))
    image_infomation_list = select_data(db_file)
    intersecting_image_list = []
    for image_infomation in image_infomation_list:
        image_geometry = image_infomation[2]
        intersection = ogr.CreateGeometryFromWkt(update_image_geometry).Intersection(ogr.CreateGeometryFromWkt(image_geometry))
        if intersection.GetArea() > 0:
            intersecting_image_list.append(image_infomation[1])
        else:
            continue
    return intersecting_image_list

    
def geometry_to_bounding_box(geometry):
    """
    geometry to bounding box
    :param geometry:
    :return: bounding box
    """
    geometry = wkt.loads(geometry)
    bbox = geometry.bounds
    return bbox


def get_clipped_image(image_path, clip_bbox):
    """
    clip image
    :param image_path:
    :param clip_geometry:
    :return:
    """
    image_path = r"C:\Users\Administrator\Desktop\local_update\1_A2包_5_9_preview.tif"
    output_path = image_path.replace('.tif', '_clipped.tif')
    # bbox = (106.0038133, 26.4052118, 107.1301093, 27.3620738)
    gdal.Translate(output_path, image_path, format='GTiff', outputBounds=clip_bbox, options=['-co', 'BIGTIFF=YES'])


def calculate_buffer_distance(zoom_level):
    """
    calculate buffer distance
    :param image_path:
    :return: buffer distance
    """
    image_info_dict = gdal.Info(image_path, format='json')
    coordinates = image_info_dict['wgs84Extent']['coordinates'][0]
    geometry = str(Polygon(coordinates))
    geometry = wkt.loads(geometry)
    buffer_distance = geometry.area / 100
    return buffer_distance


def generate_geometry_buffer(geometry, buffer_distance):
    """
    generate geometry buffer
    :param geometry:
    :param buffer_distance:
    :return: buffer geometry
    """
    geometry = wkt.loads(geometry)
    buffer_geometry = geometry.buffer(buffer_distance, join_style=2)
    return buffer_geometry


if __name__ == "__main__":
    image_path = r"C:\Users\Administrator\Desktop\2_贵阳替云_preview.tif"
    db_file = r"demo\image_source\database\image_source_infomation.db"
    image_geometry = get_image_geometry(image_path)
    intersecting_image_list = get_intersecting_images(image_path, db_file)
    print(intersecting_image_list)
    bbox = geometry_to_bounding_box(image_geometry)
    get_clipped_image(image_path, bbox)
    print(image_geometry)
    geometry_buffer = generate_geometry_buffer(image_geometry, 1)
    print(geometry_buffer)