# -*- encoding: utf-8 -*-

'''
@File    :   update_partial_image.py
@Time    :   2022/07/20 10:18:37
@Author  :   Lee
@Version :   1.0
@License :   (C)Copyright Cennavi, Li Wei
@Desc    :   None
'''


import os
import shutil
import time
import logging

import utils.image_geometry as geo
import utils.image_processing as pro

from scan_image_information import scan_and_record_image_information


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def generate_mosaic_image(update_image_dir, update_image_path, db_file, zoom_level):
    """
    update partial image
    :param update_image_dir:
    :param update_image_path:
    :param db_file:
    :param zoom_level:
    :return:
    """
    logging.info("find images intersect with {}.".format(update_image_path))
    update_image_geometry = geo.get_image_geometry(update_image_path)
    intersecting_image_list = geo.get_intersecting_images(update_image_path, db_file)
    update_image_zoom_level_bbox = geo.generate_zoom_level_geometry_bbox(update_image_geometry, zoom_level)
    update_image_zoom_level_geometry = geo.bbox_to_geometry(update_image_zoom_level_bbox)
    buffer_distance = geo.calculate_buffer_distance(zoom_level)
    update_image_zoom_level_geometry_buffer = geo.generate_geometry_buffer(update_image_zoom_level_geometry, buffer_distance)
    update_image_zoom_level_bbox_buffer = geo.geometry_to_bbox(update_image_zoom_level_geometry_buffer)
    
    # create temp dir
    temp_dir = os.path.join(update_image_dir, 'temp')
    os.makedirs(temp_dir, exist_ok=True)

    logging.info("clip images intersect with {} by zoom level extent.".format(update_image_path))
    for image_path in intersecting_image_list:
        clipped_output_path = os.path.join(temp_dir, os.path.basename(image_path.replace('.tif', '_clipped.tif')))
        pro.clip_image(image_path, clipped_output_path, update_image_zoom_level_bbox_buffer)
    
    clipped_image_list = []
    for clipped_image_path in os.listdir(temp_dir):
        # clipped_image_path = os.path.join(temp_dir, clipped_image_path)
        clipped_image_list.append(os.path.join(temp_dir, clipped_image_path))

    logging.info("moscaic images intersect with {}.".format(update_image_path))
    mosaic_image_path = update_image_path.replace('.tif', '_mosaic.tif')

    # make sure mosaic image does not exist
    if os.path.exists(mosaic_image_path):
        os.remove(mosaic_image_path)
        
    pro.create_mosaic_image(clipped_image_list, update_image_path, mosaic_image_path)
    
    # remove temp dir
    shutil.rmtree(temp_dir)


if __name__ == '__main__':
    # original image dir that contains original images
    original_image_repository = r'C:\Users\Administrator\Desktop\local_update'
    # db file path to store image source information
    db_file = r'demo\image_mosaic\database\image_source_infomation.db'
    # image dir to store update image
    update_image_dir = r'C:\Users\Administrator\Desktop\update'
    # image path to be updated
    update_image_path = r'C:\Users\Administrator\Desktop\update\2_贵阳替云_preview.tif'
    # extract source images by zoom level
    zoom_level = 10

    start_time = time.time()
    print("-----------------------------------------")
    logging.info("start to update images intersect with {}.".format(update_image_path))
    generate_mosaic_image(update_image_dir, update_image_path, db_file, zoom_level)
    end_time = time.time()
    logging.info("mosaic image has been generated.")
    print("-----------------------------------------")
    print("time used: " + str(round((end_time - start_time)/60,3)) + "min.")
    print("-----------------------------------------")
    print("\n")

    res = input("Update the Mosaic image to the original image repository (yes/no)? ")
    if res.lower() == 'yes':
        shutil.copy(update_image_path.replace('.tif', '_mosaic.tif'), original_image_repository)
        scan_and_record_image_information(original_image_repository, db_file)
        print("The mosaic image has been updated to original image repository.")
    else:
        print("You skip updating mosaic image to original image repository, please do it manually in the future.")
    print("-----------------------------------------")