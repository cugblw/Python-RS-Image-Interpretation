# -*- encoding: utf-8 -*-

'''
@File    :   parse_bil_to_geotiff.py
@Time    :   2022/03/21 07:31:11
@Author  :   Li Wei
@Version :   1.0
@Email   :   liwei@cennavi.com.cn
@Desc    :   Parses the compressed binary dem '.bil' file into a '.tif' file.
'''


import os
import site
import struct
import numpy as np
from osgeo import gdal, osr


# 处理gdal运行错误
for item in site.getsitepackages():
    if "/lib/site-packages" in item.replace("\\", "/"):
        os.environ['PROJ_LIB'] = os.path.join(item, 'pyproj/proj_dir/share/proj')

def parse_bil_file(bil_path, width, height):
    # 读取bil文件
    file = open(bil_path, "rb")
    contents = file.read()
    file.close()

    # 将高程数据解压到元组
    s = "<%dH" % (int(width*height))
    z = struct.unpack(s, contents)

    heights = [[None for x in range(height)] for y in range(width)]

    for r in range(0,height):
        for c in range(0,width):
            elevation = z[(width*r)+c]
            #处理高程异常值
            if (elevation==65535 or elevation<0 or elevation>20000):
                elevation=0.0

            heights[r][c]=float(elevation)
    return np.array(heights)

#获取瓦片zoom,x,y
def get_zoom_x_y(file_path):
    tile_number = (file_path.split('.')[0]).split('_')
    zoom = int(tile_number[0])
    x = int(tile_number[1])
    y = int(tile_number[2])
    return zoom, x, y

#瓦片号转换成经纬度
def tile2lonlat(zoom, px, py):
    #计算每个瓦片的经差和纬差
    angPerTile = float(360) / (2**zoom)
    #左上 角
    ulx = px * angPerTile -180 
    uly = (2**zoom - py ) * angPerTile -180
    #右下角
    lrx = ulx + angPerTile 
    lry = uly - angPerTile
    return [ulx, uly, lrx, lry]

#获取仿射变换参数
def get_geotransform_from_boundary(boundary,size):
    geotransform = []
    
    geotransform.append(boundary[0])
    geotransform.append((boundary[2]-boundary[0])/size)
    geotransform.append(0.0)
    geotransform.append(boundary[1])
    geotransform.append(0.0)
    geotransform.append((boundary[3]-boundary[1])/size)
    
    return tuple(geotransform)


def save_array_to_tiff(tif_file_path,array_data,size,geotransform):
    driver = gdal.GetDriverByName("GTiff")
    wkt = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,\
           AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0],\
           UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AXIS["Latitude",\
           NORTH],AXIS["Longitude",EAST],AUTHORITY["EPSG","4326"]]'

    dst_ds = driver.Create(tif_file_path,
                        size,
                        size,
                        1,
                        gdal.GDT_Int16)

    #写入栅格数据
    dst_ds.GetRasterBand(1).WriteArray( array_data )
    #设置0值
    dst_ds.GetRasterBand(1).SetNoDataValue(-999)
    #设置仿射变换参数
    dst_ds.SetGeoTransform(geotransform)
    # 设置空间参考
    srs = osr.SpatialReference()
    srs.ImportFromWkt(wkt)
    dst_ds.SetProjection( srs.ExportToWkt() )
    
    #关闭数据集
    ds = None
    dst_ds = None

if __name__ == '__main__':
    # dem瓦片文件大小
    size = 129
    # bil文件路径
    bil_path = r"C:\Users\Administrator\Desktop\bil\bil_zoom3"
    # tif文件保存路径
    tif_path = r"C:\Users\Administrator\Desktop\bil_to_tif"

    if not os.path.exists(tif_path):
        os.makedirs(tif_path)

    for root,dirs,files in os.walk(bil_path):
        for file in files:
            print("start to parse '{}';".format(file))
            file_name = file.split('.')[0] + '.tif'
            tif_file_name = os.path.join(tif_path,file_name)
            zoom, x, y = get_zoom_x_y(file)
            geo_boundary = tile2lonlat(zoom, x ,y)
            geotransform =get_geotransform_from_boundary(geo_boundary,size)
            array_data = parse_bil_file(os.path.join(root,file),size,size)
            save_array_to_tiff(tif_file_name,array_data,size,geotransform)
            print("convert '{}' to '{}';".format(file,file_name))

    print ("Convert bil to geotiff  completed!")