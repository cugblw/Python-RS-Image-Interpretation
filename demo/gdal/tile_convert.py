
# -*- encoding: utf-8 -*-

'''
@File    :   tile_convert.py
@Time    :   2022/03/22 11:09:54
@Author  :   Lee
@Version :   1.0
@License :   (C)Copyright Cennavi, Li Wei
@Desc    :   None
'''


import math
import numpy as np
from io import BytesIO
from PIL import Image
from osgeo import gdal

TILE_SIZE = 256


def tile_x_to_longitude(tile_x, zoom):
    return pixel_x_to_longitude(int(tile_x) * TILE_SIZE, zoom)
def pixel_x_to_longitude(pixel_x, zoom):
    return 360 * ((float(pixel_x) / (TILE_SIZE << zoom)) - 0.5)



def pixel_y_to_latitude(pixel_y, zoom):
    y = 0.5 - float(pixel_y) / (TILE_SIZE << zoom)
    return 90 - 360 * math.atan(math.exp(-y * 2 * math.pi)) / math.pi
def tile_y_to_latitude(tile_y, zoom):
    return pixel_y_to_latitude(int(tile_y) * TILE_SIZE, zoom)


# def tile2boundary(zoom, x, y):
#     lon_min = tile_x_to_longitude(x, zoom)
#     lat_max = tile_y_to_latitude(y, zoom)
#     lon_max = tile_x_to_longitude(x + 1, zoom)
#     lat_min = tile_y_to_latitude(y + 1, zoom)

#     # wkt = "POLYGON ((" + lng_left + " " + lat_up + ", "
#     # wkt += lng_right + " " + lat_up + ", "
#     # wkt += lng_right + " " + lat_down + ", "
#     # wkt += lng_left + " " + lat_down + ", "
#     # wkt += lng_left + " " + lat_up + "))"

#     # return wkt

# To do
def get_tile_number():
    zoom = 0
    x = 0
    y = 0
    return [zoom, x, y]

def tile2boundary(zoom, x, y):
    lon_min = tile_x_to_longitude(x, zoom)
    lat_max = tile_y_to_latitude(y, zoom)
    lon_max = tile_x_to_longitude(x + 1, zoom)
    lat_min = tile_y_to_latitude(y + 1, zoom)

    extent = [lon_min,lat_min,lon_max,lat_max]
    return extent

def get_raster_data_by_boundary(zoom, x, y, size):
    # extent = tile2boundary(zoom, x, y)
    extent = tile2boundary(14,12819,8048)
    # tif_path = r"C:\Users\Administrator\Desktop\Image_Src\2m\mlxy_C1_jlp.tif"
    tif_path = r"C:\Users\Administrator\Desktop\Image\beijing_clip_4326.tif"

    # Open raster in read only mode
    ds = gdal.Open(tif_path, gdal.GA_ReadOnly)

    # Get the first raster band
    band = ds.GetRasterBand(1)
    # raster_count = ds.RasterCount
    # print(raster_count)
    width = band.XSize
    height = band.YSize

    print(width)
    print(height)

    # Compute x/y resolution in degrees
    # resx = 360. / band.XSize
    # resy = 180. / band.YSize

    # print(resx)
    # print(resy)

    # Define the geotransform used to convert x/y pixel to lon/lat degree
    # [lon_topleft, lon_resolution, lat_skew, lat_topleft, lon_skew, lat_resolution]
    # geotransform = [-180, resx, 0.0,  90, 0.0, -1*resy]
    geotransform = ds.GetGeoTransform()

    # The inverse geotransform is used to convert lon/lat degrees to x/y pixel index
    inv_geotransform = gdal.InvGeoTransform(geotransform)

    # Define a longitude/latitude bounding box in degrees
    # [lonmin, latmin, lonmax, latmax]

    # bbox = [101.66748046875, 3.1405161039832308, 101.689453125, 3.1624555302378496]
    bbox = extent

    # Convert lon/lat degrees to x/y pixel for the dataset
    _x0, _y0 = gdal.ApplyGeoTransform(inv_geotransform, bbox[0], bbox[1])
    _x1, _y1 = gdal.ApplyGeoTransform(inv_geotransform, bbox[2], bbox[3])
    x0, y0 = min(_x0, _x1), min(_y0, _y1)
    x1, y1 = max(_x0, _x1), max(_y0, _y1)
    print(int(x0),int(y0),int(x1),int(y1))

    # Get subset of the raster as a numpy array
    # data = band.ReadAsArray(int(x0), int(y0), int(x1-x0), int(y1-y0))
    band1_data = ds.GetRasterBand(1).ReadAsArray(int(x0), int(y0), int(x1-x0), int(y1-y0))
    band2_data = ds.GetRasterBand(2).ReadAsArray(int(x0), int(y0), int(x1-x0), int(y1-y0))
    band3_data = ds.GetRasterBand(3).ReadAsArray(int(x0), int(y0), int(x1-x0), int(y1-y0))

    rgb_data = np.dstack([band1_data,band2_data,band3_data])

    print(type(rgb_data))
    # convert a NumPy array to PIL image
    img = Image.fromarray(np.uint8(rgb_data))
    # img.save("test.png")
    print(type(img))
    img_new = resize_image(img,size)

    img_new.save('test_resize.png')

    return convert_image_to_bytes(img_new)

def resize_image(img,size):
    img_new = img.resize((size,size))
    return img_new

def resize_image_by_times(img,times):
    img_new = None
    return img_new

def convert_image_to_bytes(img):
    # PIL Image to base64
    img_file = BytesIO()
    img.save(img_file,format = 'PNG')
    img_bytes = img_file.getvalue() # im_bytes: image in binary format.
    return img_bytes



if __name__ == '__main__':
   extent =  tile2boundary(12,3204,2011)
   print(extent)
   # [101.66748046875, 3.1405161039832308, 101.689453125, 3.1624555302378496]