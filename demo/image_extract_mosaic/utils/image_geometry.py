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

from utils.database_manipulation import select_data
import utils.tile_lon_lat_convert as tc
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


# def clip_image_by_geometry(image_path, clip_geometry):
#     """
#     clip image by geometry
#     :param image_path:
#     :param clip_geometry:
#     :return:
#     """
#     image_info_dict = gdal.Info(image_path, format='json')
#     coordinates = image_info_dict['wgs84Extent']['coordinates'][0]
#     geometry = str(Polygon(coordinates))
#     intersection = ogr.CreateGeometryFromWkt(clip_geometry).Intersection(ogr.CreateGeometryFromWkt(geometry))
#     if intersection.GetArea() > 0:
#         return True
#     else:
#         return False


def get_intersecting_images(update_image_path, db_file):
    """
    geometry intersect
    :param geometry1:
    :param geometry2:
    :return:
    """
    update_image_geometry = get_image_geometry(update_image_path)
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

    
def geometry_to_bbox(geometry):
    """
    geometry to bbox
    :param geometry:
    :return: bbox
    """
    geometry = wkt.loads(geometry)
    bbox = geometry.bounds
    return bbox


def bbox_to_geometry(bbox):
    """
    bbox to geometry
    :param bbox:
    :return: geometry
    """
    geometry = Polygon([(bbox[0], bbox[1]), (bbox[0], bbox[3]), (bbox[2], bbox[3]), (bbox[2], bbox[1])])
    return str(geometry)


def calculate_buffer_distance(zoom_level):
    """
    calculate buffer distance
    :param image_path:
    :return: buffer distance
    """
    lon1, lon2 = tc.x_to_lon_edges(1, zoom_level)
    buffer_distance = (lon2 - lon1) / 2
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
    return str(buffer_geometry)


def generate_zoom_level_geometry_bbox(image_geometry, zoom_level):
    """
    generate zoom level geometry
    :param geometry:
    :param zoom_level:
    :return: zoom level geometry
    """
    bbox = geometry_to_bbox(image_geometry)
    x_min, x_max, y_min, y_max = tc.boundary_to_xyz(bbox[0], bbox[2], bbox[1], bbox[3], zoom_level)

    lng_left_min, lat_up_min, lng_right_min, lat_down_min = tc.xyz2boundary(x_min, y_min, zoom_level)
    lng_left_max, lat_up_max, lng_right_max, lat_down_max = tc.xyz2boundary(x_max, y_max, zoom_level)
    
    lon_min = min(lng_left_min, lng_right_min, lng_left_max, lng_right_max)
    lat_min = min(lat_up_min, lat_down_min, lat_up_max, lat_down_max)
    lon_max = max(lng_left_min, lng_right_min, lng_left_max, lng_right_max)
    lat_max = max(lat_up_min, lat_down_min, lat_up_max, lat_down_max)
    return (lon_min, lat_min, lon_max, lat_max)