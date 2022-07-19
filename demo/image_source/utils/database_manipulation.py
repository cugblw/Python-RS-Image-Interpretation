# -*- encoding: utf-8 -*-

'''
@File    :   database_manipulation.py
@Time    :   2022/07/18 10:48:34
@Author  :   Lee
@Version :   1.0
@License :   (C)Copyright Cennavi, Li Wei
@Desc    :   None
'''


import os
import sqlite3
from sqlite3 import Error


def create_database(db_file):
    """
    create a new sqlite database if not exists
    specified by db_file
    """
    conn = None
    try:
        if not os.path.exists(db_file):
            conn = sqlite3.connect(db_file)
            print(sqlite3.version)
        else:
            print('database already exists')
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def create_connection(db_file):
    """
    create a database connection to the SQLite database
    specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn


def create_table(db_file):
    """
    create a table in the database
    :param db_file: database file
    :return:
    """
    conn = create_connection(db_file)
    if conn:
        cur = conn.cursor()
        sql_image_information = '''CREATE TABLE IF NOT EXISTS image_infomation (name TEXT, 
                                                            image_path TEXT PRIMARY KEY, 
                                                            geometry TEXT, 
                                                            extent TEXT, 
                                                            image_structure TEXT,
                                                            width INTEGER,
                                                            height INTEGER,
                                                            CRS TEXT, 
                                                            band INTEGER, 
                                                            resolution NUMERIC, 
                                                            format TEXT, 
                                                            size TEXT,
                                                            pixel_depth TEXT)'''
        cur.execute(sql_image_information)
        conn.commit()

        sql_invalid_image = '''CREATE TABLE IF NOT EXISTS invalid_image (name TEXT, image_path TEXT PRIMARY KEY, description TEXT)'''
        cur.execute(sql_invalid_image)
        conn.commit()

        conn.close()
    else:
        print('database not exists')


def insert_or_update_data(db_file, image_info):
    """
    insert data into the database
    :param db_file: database file
    :param image_info: image info
    :return:
    """

    conn = create_connection(db_file)
    if conn:
        cur = conn.cursor()
        sql = '''INSERT or REPLACE INTO image_infomation(name, image_path, geometry, extent, image_structure, width, 
                                                         height, CRS, band, resolution, format, size, pixel_depth)
                 VALUES(:name, :image_path, :geometry, :extent, :image_structure, :width, :height, :CRS, 
                        :band, :resolution, :format, :size, :pixel_depth);'''
        cur.execute(sql, image_info)
        conn.commit()
        conn.close()
    else:
        print('database not exists')


def insert_or_update_error_data(db_file,invalide_image_info):
    """
    insert data into the database
    :param db_file: database file
    :param invalide_image_info: image info
    :return:
    """

    conn = create_connection(db_file)
    if conn:
        cur = conn.cursor()
        sql = '''INSERT or REPLACE INTO invalid_image(name, image_path, description)
                 VALUES(:name, :image_path, :description);'''
        cur.execute(sql, invalide_image_info)
        conn.commit()
        conn.close()
    else:
        print('database not exists')


def select_data(db_file):
    """
    select data from the database
    :param db_file: database file
    :return:
    """
    conn = create_connection(db_file)
    if conn:
        cur = conn.cursor()
        sql = '''SELECT * FROM image_infomation'''
        cur.execute(sql)
        rows = cur.fetchall()
        conn.close()
        return rows
    else:
        print('database not exists')


if __name__ == '__main__':
    database_path = r'demo\image_source\database\image_source_infomation.db'
    image_path = r"D:\lanzhou_2m.tif"
    create_connection(database_path)
    create_table(database_path)
    rows = select_data(database_path)
    print(len(rows))