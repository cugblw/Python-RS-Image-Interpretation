import os
import shutil
import tarfile
from numpy import tile
import shapefile as shp
import sys

sys.path.append('././')

from core import tile_lon_lat_convert as tc

# import core.tile_lon_lat_convert

def get_boundary_from_shapefile(shapefile_path):
    """
    获取shapefile的边界范围
    """
    sf = shp.Reader(shapefile_path)
    shapes = sf.shapes()
    bbox = shapes[0].bbox
    return bbox

def boundary_to_tile_list(boundary, zoom):
    """
    将转换边界到tile列表
    """
    # tc.bbox_to_xyz(boundary[0], boundary[2], boundary[1], boundary[3], zoom)
    tile_range = tc.bbox_to_xyz(boundary[0], boundary[2], boundary[1], boundary[3], zoom)
    print(tile_range)
    tile_list = []
    for x in range(tile_range[0], tile_range[1]+1):
        for y in range(tile_range[2], tile_range[3]+1):
            tile_number = str(zoom) + "_" + str(x) + "_" + str(y)
            tile_list.append(tile_number)
    return tile_list

def boundary_zoom_range_to_tile_list(boundary, zoom_range):
    """
    将边界和缩放级别范围转换为tile列表
    """
    tile_list = []
    if zoom_range[0] > zoom_range[1]:
        print("zoom range error")
        return
    for zoom in range(zoom_range[0], zoom_range[1]+1):
        tile_list.extend(boundary_to_tile_list(boundary, zoom))
    return tile_list

def generate_file_name(datasource, z, x, y):
    """通过瓦片编号计算瓦片存储路径"""
    if z > 6:
        dir_ = 1 << (z - 5)
        row = int(y / dir_)
        col = int(x / dir_)
        file_name = os.path.join(datasource, str(z), "R" + str(row), "C" + str(col),
                                 str(z) + "_" + str(x) + "_" + str(y) + ".jpg")
    else:
        file_name = os.path.join(datasource, str(z), str(z) + "_" + str(x) + "_" + str(y) + ".jpg")
    return file_name

def search_tile_from_repository(tile_list, repository, output_path):
    """
    搜索tile仓库，并将tile导出到指定目录,并保持路径结构
    """
    for tile in tile_list:
        z = int(tile.split("_")[0])
        x = int(tile.split("_")[1])
        y = int(tile.split("_")[2])
        file_name = generate_file_name("satellite", z, x, y)
        tile_path = os.path.join(repository, file_name)
        if os.path.exists(tile_path):
            tile_output_path = os.path.join(output_path, file_name)
            if not os.path.exists(os.path.dirname(tile_output_path)):
                os.makedirs(os.path.dirname(tile_output_path))
            shutil.copy(tile_path, tile_output_path)
    return

def tar_tile_folders(path):
    """
    将文件夹打包成tar文件
    """
    return

def remove_tile_folders(path):
    """
    删除文件夹
    """
    return

if __name__ == '__main__':
    shapefile_path = r'res\vector\Lanzhou.shp'
    target_path = r"C:\Users\Administrator\Desktop\tile_export"
    repository = r'C:\Users\Administrator\Desktop\tar_list'
    boundary = get_boundary_from_shapefile(shapefile_path)
    # tile_list = boundary_to_tile_list(boundary, zoom=12)
    tile_list = boundary_zoom_range_to_tile_list(boundary, zoom_range=(1, 16))
    search_tile_from_repository(tile_list, repository, target_path)

    print(boundary)
    # print(tile_list)