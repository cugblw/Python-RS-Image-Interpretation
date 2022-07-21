


# -*- encoding: utf-8 -*-

'''
@File    :   scan_image_source_information.py
@Time    :   2022/07/18 16:11:23
@Author  :   Lee
@Version :   1.0
@License :   (C)Copyright Cennavi, Li Wei
@Desc    :   None
'''


import os
import time

from utils.verify_image import check_image
from utils.database_manipulation import create_connection,create_table, insert_or_update_data,insert_or_update_error_data
from utils.get_image_metadata import get_image_info, get_invalid_image_info


def scan_and_record_image_information(image_dir, db_file):
    """
    main function to scan image source information
    :param image_dir:
    :param db_file:
    :return:
    """
    for root, dirs, files in os.walk(image_dir):
        for file in files:
            if file.endswith('.tif'):
                print("scan image source information: {}".format(file))
                image_path = os.path.join(root, file)
                image_validation,description = check_image(image_path)
                if image_validation:
                    try:
                        image_info = get_image_info(image_path)
                        create_connection(db_file)
                        create_table(db_file)
                        insert_or_update_data(db_file, image_info)
                    except:
                        invalid_image_info = get_invalid_image_info(image_path,description)
                        create_connection(db_file)
                        create_table(db_file)
                        insert_or_update_error_data(db_file, invalid_image_info)
                else:
                    invalid_image_info = get_invalid_image_info(image_path, description)
                    create_connection(db_file)
                    create_table(db_file)
                    insert_or_update_error_data(db_file, invalid_image_info)


if __name__ == "__main__":
    # image dir to scan
    original_image_repository = r"E:\Data\tiff\11"
    # db file path to store image source information
    db_file = r"demo\image_mosaic\database\image_source_infomation.db"

    start_time = time.time()
    scan_and_record_image_information(original_image_repository, db_file)
    end_time = time.time()
    print("time used: " + str(round((end_time - start_time),3)) + "s.")