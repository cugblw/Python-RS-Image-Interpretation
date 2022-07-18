


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

from utils.verify_image import check_image
from utils.create_database import create_connection,create_table, insert_or_update_data,insert_or_update_error_data
from utils.get_image_metadata import get_image_info, get_invalid_image_info


def main(image_dir, db_file):
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
    image_dir = r"E:\Data\tiff\11"
    db_file = r"demo\image_source\database\image_source_infomation.db"
    main(image_dir, db_file)