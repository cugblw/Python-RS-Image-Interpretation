# -*- encoding: utf-8 -*-

"""
@File    :   acquire_image_subset.py
@Time    :   2022/03/24 16:56:51
@Author  :   Lee
@Version :   1.0
@License :   (C)Copyright Cennavi, Li Wei
@Desc    :   None
"""

import base64
from io import BytesIO

import numpy as np
from osgeo import gdal
from PIL import Image

from core.image_util import get_resize_times, convert_image_from_array, convert_image_to_bytes, \
    convert_image_transparency, resize_image
from core.tile_convert import tile2boundary
# from tile_convert import tile2boundary

# 按14级进行请求


def get_geotiff_subset(dataset, zoom, x, y):
    """
    获取影像的子集
    """
    lon_min, lat_min, lon_max, lat_max = tile2boundary(zoom, x, y)
    projwin = (lon_min, lat_max, lon_max, lat_min)
    ds_subset = gdal.Translate('/vsimem/' + str(zoom) + '_' +
                               str(x) + '_' + str(y) + '.tif', dataset, projWin=projwin)
    # ds = gdal.Open('/vsimem/' + str(zoom) + '_' + str(x) + '_' + str(y) + '.tif')
    return ds_subset

    gdal.Translate(str(zoom) + '_' + str(x) + '_' +
                   str(y) + '.tif', dataset, projWin=projwin)


# http://visibleearth.nasa.gov/view.php?id=57752
def read_image_data_by_tile(zoom, x, y, tile_size, ds):
    # tif_path = r"C:\Users\Administrator\Desktop\Image_Src\2m\mlxy_C1_jlp.tif"

    # tif_path = r"C:\Users\Administrator\Desktop\Image\beijing_clip_4326.tif"
    # tif_path = r"C:\Users\Administrator\Desktop\Image_Src\2m\DZGYYQ.tif"
    # vrt_options = gdal.BuildVRTOptions(resampleAlg='cubic')
    # ds = gdal.BuildVRT("temp.vrt",tif_path,options=vrt_options)
    # ds.FlushCache()

    # tif_path = data_list[0]
    # # Open raster in read only mode
    # ds = gdal.Open(tif_path, gdal.GA_ReadOnly)

    # Get the first raster band, width, height
    band = ds.GetRasterBand(1)
    width = band.XSize
    height = band.YSize
    # del band
    # band_count = ds.RasterCount
    # print(band_count)

    # Define the geotransform used to convert x/y pixel to lon/lat degree
    geotransform = ds.GetGeoTransform()

    # The inverse geotransform is used to convert lon/lat degrees to x/y pixel index
    inv_geotransform = gdal.InvGeoTransform(geotransform)

    # Define a longitude/latitude bounding box in degrees
    bbox = tile2boundary(zoom, x, y)

    # Convert lon/lat degrees to x/y pixel for the dataset
    _x0, _y0 = gdal.ApplyGeoTransform(inv_geotransform, bbox[0], bbox[1])
    _x1, _y1 = gdal.ApplyGeoTransform(inv_geotransform, bbox[2], bbox[3])
    x0, y0 = int(min(_x0, _x1)), int(min(_y0, _y1))
    x1, y1 = int(max(_x0, _x1)), int(max(_y0, _y1))
    # print(x0, y0, x1, y1)

    # Get subset of the raster as a numpy array
    # 通过瓦片位置，对应查找影像区域，读取数据
    if x0 >= 0 and y0 >= 0 and x1 < width and y1 < height:  # 请求瓦片完全在影像内部
        rgb_data = np.dstack([ds.GetRasterBand(n + 1).ReadAsArray(int(x0), int(y0), int(x1 - x0), int(y1 - y0)) for n in
                              range(ds.RasterCount)])

        if np.all(rgb_data == 0):
            return None

        img = convert_image_from_array(rgb_data)
        img_resize = resize_image(img, tile_size)
        img_transparency = convert_image_transparency(img_resize)
        del ds
        # return convert_image_to_bytes(img_transparency)
        return img_transparency

    elif x1 < 0 or y1 < 0 or x0 >= width or y0 >= height:  # 请求瓦片完全在影像外部
        print("blank tile data!")
        blank = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR4nGP4//8/AwAI/AL+p5qgoAAAAABJRU5ErkJggg=="
        img = base64.b64decode(blank)
        img = Image.open(BytesIO(img))
        return None

    elif x0 <= 0 and y0 <= 0 and x1 >= width and y1 >= height:  # 请求瓦片完全包裹影像
        if ((x1 - x0) / tile_size) > 5 or ((y1 - y0) / tile_size) > 5:  # 请求层级太小，内存溢出处理
            times = get_resize_times((x1 - x0), (y1 - y0), tile_size)  # 缩放倍数

            rgb_data = np.zeros(
                (int((y1 - y0) / times), int((x1 - x0) / times), 3), dtype=np.uint8)
            band_part_data = np.dstack(
                [ds.GetRasterBand(n + 1).ReadAsArray(0, 0, width, height, int(width / times), int(height / times)) for n
                 in range(ds.RasterCount)])
            rgb_data[int((0 - y0) / times):int(height / times) - int(y0 / times),
                     int((0 - x0) / times):int(width / times) - int(x0 / times), :] = band_part_data

            # band1_part_data = ds.GetRasterBand(1).ReadAsArray(0, 0, width, height, int(width/times), int(height/times))
            # band2_part_data = ds.GetRasterBand(2).ReadAsArray(0, 0, width, height, int(width/times), int(height/times))
            # band3_part_data = ds.GetRasterBand(3).ReadAsArray(0, 0, width, height, int(width/times), int(height/times))

            # band1_data = np.zeros((int((y1-y0)/times),int((x1-x0)/times)))
            # band2_data = np.zeros((int((y1-y0)/times),int((x1-x0)/times)))
            # band3_data = np.zeros((int((y1-y0)/times),int((x1-x0)/times)))

            # band1_data[int((0-y0)/times):int(height/times) - int(y0/times),int((0-x0)/times):int(width/times)-int(x0/times)] = band1_part_data
            # band2_data[int((0-y0)/times):int(height/times) - int(y0/times),int((0-x0)/times):int(width/times)-int(x0/times)] = band2_part_data
            # band3_data[int((0-y0)/times):int(height/times) - int(y0/times),int((0-x0)/times):int(width/times)-int(x0/times)] = band3_part_data

            # rgb_data = np.dstack([band1_data,band2_data,band3_data])

            if np.all(rgb_data == 0):
                return None

            img = convert_image_from_array(rgb_data)
            img_resize = resize_image(img, tile_size)
            img_transparency = convert_image_transparency(img_resize)
            del ds
            # return convert_image_to_bytes(img_transparency)
            return img_transparency

        else:
            rgb_data = np.zeros((y1 - y0, x1 - x0, 3), dtype=np.uint8)
            band_part_data = np.dstack(
                [ds.GetRasterBand(n + 1).ReadAsArray(0, 0, width, height) for n in range(ds.RasterCount)])
            rgb_data[(0 - y0):(height - y0), (0 - x0):(width - x0), :] = band_part_data

            if np.all(rgb_data == 0):
                return None

            img = convert_image_from_array(rgb_data)
            img_resize = resize_image(img, tile_size)
            img_transparency = convert_image_transparency(img_resize)
            del ds
            # return convert_image_to_bytes(img_transparency)
            return img_transparency

    else:  # 请求瓦片部分包含影像
        if ((x1 - x0) / tile_size) > 5 or ((y1 - y0) / tile_size) > 5:  # 请求层级太小，内存溢出处理
            times = get_resize_times((x1 - x0), (y1 - y0), tile_size)  # 缩放倍数

            if x0 < 0 and 0 <= x1 < width and y0 < 0 and y1 < height:  # situation 1'
                rgb_data = np.zeros(((int(y1 / times) - int(y0 / times)), (int(x1 / times) - int(x0 / times)), 3),
                                    dtype=np.uint8)
                band_part_data = np.dstack(
                    [ds.GetRasterBand(n + 1).ReadAsArray(0, 0, x1, y1, int(x1 / times), int(y1 / times)) for n in
                     range(ds.RasterCount)])
                rgb_data[int((0 - y0) / times):(int(y1 / times) - int(y0 / times)),
                         int((0 - x0) / times):(int(x1 / times) - int(x0 / times)), :] = band_part_data

                if np.all(rgb_data == 0):
                    return None

                img = convert_image_from_array(rgb_data)
                img_resize = resize_image(img, tile_size)
                img_transparency = convert_image_transparency(img_resize)
                del ds
                # return convert_image_to_bytes(img_transparency)
                return img_transparency

            elif x0 < 0 and 0 <= x1 < width and 0 <= y0 < height and y1 >= height:  # situation 2'
                rgb_data = np.zeros(((int(y1 / times) - int(y0 / times)), (int(x1 / times) - int(x0 / times)), 3),
                                    dtype=np.uint8)
                band_part_data = np.dstack([ds.GetRasterBand(n + 1).ReadAsArray(0, y0, x1, (height - y0),
                                                                                int(x1 /
                                                                                    times),
                                                                                (int(height / times) - int(y0 / times)))
                                            for n in range(ds.RasterCount)])
                rgb_data[0:(int(height / times) - int(y0 / times)),
                         int((0 - x0) / times):(int(x1 / times) - int(x0 / times)), :] = band_part_data

                if np.all(rgb_data == 0):
                    return None

                img = convert_image_from_array(rgb_data)
                img_resize = resize_image(img, tile_size)
                img_transparency = convert_image_transparency(img_resize)
                del ds
                # return convert_image_to_bytes(img_transparency)
                return img_transparency

            elif 0 <= x0 < width and x1 >= width and y0 < 0 and 0 <= y1 < height:  # situation 3'
                rgb_data = np.zeros(((int(y1 / times) - int(y0 / times)), (int(x1 / times) - int(x0 / times)), 3),
                                    dtype=np.uint8)
                band_part_data = np.dstack([ds.GetRasterBand(n + 1).ReadAsArray(x0, 0, (width - x0), y1,
                                                                                (int(
                                                                                    width / times) - int(x0 / times)),
                                                                                int(y1 / times)) for n in
                                            range(ds.RasterCount)])
                rgb_data[int((0 - y0) / times):(int(y1 / times) - int(y0 / times)),
                         0:(int(width / times) - int(x0 / times)), :] = band_part_data

                if np.all(rgb_data == 0):
                    return None

                img = convert_image_from_array(rgb_data)
                img_resize = resize_image(img, tile_size)
                img_transparency = convert_image_transparency(img_resize)
                del ds
                # return convert_image_to_bytes(img_transparency)
                return img_transparency

            elif 0 <= x0 < width and x1 >= width and 0 <= y0 < height and y1 >= height:  # situation 4'
                rgb_data = np.zeros(((int(y1 / times) - int(y0 / times)), (int(x1 / times) - int(x0 / times)), 3),
                                    dtype=np.uint8)
                band_part_data = np.dstack([ds.GetRasterBand(n + 1).ReadAsArray(x0, y0, (width - x0), (height - y0),
                                                                                (int(
                                                                                    width / times) - int(x0 / times)),
                                                                                (int(height / times) - int(y0 / times)))
                                            for n in range(ds.RasterCount)])
                rgb_data[0:(int(height / times) - int(y0 / times)), 0:(int(width / times) - int(x0 / times)),
                         :] = band_part_data

                if np.all(rgb_data == 0):
                    return None

                img = convert_image_from_array(rgb_data)
                img_resize = resize_image(img, tile_size)
                img_transparency = convert_image_transparency(img_resize)
                del ds
                # return convert_image_to_bytes(img_transparency)
                return img_transparency

            elif x0 < 0 and 0 <= x1 < width and y0 >= 0 and y1 < height:  # situation 5'
                rgb_data = np.zeros(((int(y1 / times) - int(y0 / times)), (int(x1 / times) - int(x0 / times)), 3),
                                    dtype=np.uint8)
                band_part_data = np.dstack([ds.GetRasterBand(n + 1).ReadAsArray(0, y0, x1, (y1 - y0), int(x1 / times),
                                                                                (int(y1 / times) - int(y0 / times))) for
                                            n in range(ds.RasterCount)])
                rgb_data[0:(int(y1 / times) - int(y0 / times)),
                         int((0 - x0) / times):(int(x1 / times) - int(x0 / times)), :] = band_part_data

                if np.all(rgb_data == 0):
                    return None

                img = convert_image_from_array(rgb_data)
                img_resize = resize_image(img, tile_size)
                img_transparency = convert_image_transparency(img_resize)
                del ds
                # return convert_image_to_bytes(img_transparency)
                return img_transparency

            elif x0 < 0 and 0 <= x1 < width and y0 < 0 and y1 >= height:  # situation 6'
                rgb_data = np.zeros(((int(y1 / times) - int(y0 / times)), (int(x1 / times) - int(x0 / times)), 3),
                                    dtype=np.uint8)
                band_part_data = np.dstack(
                    [ds.GetRasterBand(n + 1).ReadAsArray(0, 0, x1, height, int(x1 / times), int(height / times)) for n
                     in range(ds.RasterCount)])
                rgb_data[int((0 - y0) / times):(int(height / times) - int(y0 / times)),
                         int((0 - x0) / times):(int(x1 / times) - int(x0 / times)), :] = band_part_data

                if np.all(rgb_data == 0):
                    return None

                img = convert_image_from_array(rgb_data)
                img_resize = resize_image(img, tile_size)
                img_transparency = convert_image_transparency(img_resize)
                del ds
                # return convert_image_to_bytes(img_transparency)
                return img_transparency

            elif 0 <= x0 < width and x1 < width and y0 < 0 and 0 <= y1 < height:  # situation 7'
                rgb_data = np.zeros(((int(y1 / times) - int(y0 / times)), (int(x1 / times) - int(x0 / times)), 3),
                                    dtype=np.uint8)
                band_part_data = np.dstack(
                    [ds.GetRasterBand(n + 1).ReadAsArray(x0, 0, (x1 - x0), y1, int((x1 - x0) / times), int(y1 / times))
                     for n in range(ds.RasterCount)])
                rgb_data[int((0 - y0) / times):(int(y1 / times) - int(y0 / times)),
                         0:(int(x1 / times) - int(x0 / times)), :] = band_part_data

                if np.all(rgb_data == 0):
                    return None

                img = convert_image_from_array(rgb_data)
                img_resize = resize_image(img, tile_size)
                img_transparency = convert_image_transparency(img_resize)
                del ds
                # return convert_image_to_bytes(img_transparency)
                return img_transparency

            elif x0 < 0 and x1 >= width and y0 < 0 and 0 <= y1 < height:  # situation 8'
                rgb_data = np.zeros(((int(y1 / times) - int(y0 / times)), (int(x1 / times) - int(x0 / times)), 3),
                                    dtype=np.uint8)
                band_part_data = np.dstack(
                    [ds.GetRasterBand(n + 1).ReadAsArray(0, 0, width, y1, int(width / times), int(y1 / times)) for n in
                     range(ds.RasterCount)])
                rgb_data[int((0 - y0) / times):(int(y1 / times) - int(y0 / times)),
                         int((0 - x0) / times):(int(width / times) - int(x0 / times)), :] = band_part_data

                if np.all(rgb_data == 0):
                    return None

                img = convert_image_from_array(rgb_data)
                img_resize = resize_image(img, tile_size)
                img_transparency = convert_image_transparency(img_resize)
                del ds
                # return convert_image_to_bytes(img_transparency)
                return img_transparency

            elif 0 <= x0 < width and width <= x1 and y0 >= 0 and y1 < height:  # situation 9'
                rgb_data = np.zeros(((int(y1 / times) - int(y0 / times)), (int(x1 / times) - int(x0 / times)), 3),
                                    dtype=np.uint8)
                band_part_data = np.dstack([ds.GetRasterBand(n + 1).ReadAsArray(x0, y0, (width - x0), (y1 - y0),
                                                                                (int(
                                                                                    width / times) - int(x0 / times)),
                                                                                (int(y1 / times) - int(y0 / times))) for
                                            n in range(ds.RasterCount)])
                rgb_data[0:(int(y1 / times) - int(y0 / times)), 0:(int(width / times) - int(x0 / times)),
                         :] = band_part_data

                if np.all(rgb_data == 0):
                    return None

                img = convert_image_from_array(rgb_data)
                img_resize = resize_image(img, tile_size)
                img_transparency = convert_image_transparency(img_resize)
                del ds
                # return convert_image_to_bytes(img_transparency)
                return img_transparency

            elif 0 <= x0 < width and x1 >= width and y0 < 0 and y1 >= height:  # situation 10'
                rgb_data = np.zeros(((int(y1 / times) - int(y0 / times)), (int(x1 / times) - int(x0 / times)), 3),
                                    dtype=np.uint8)
                band_part_data = np.dstack([ds.GetRasterBand(n + 1).ReadAsArray(x0, 0, (width - x0), height,
                                                                                (int(
                                                                                    width / times) - int(x0 / times)),
                                                                                int(height / times)) for n in
                                            range(ds.RasterCount)])
                rgb_data[int((0 - y0) / times):(int(height / times) - int(y0 / times)),
                         0:(int(width / times) - int(x0 / times)), :] = band_part_data

                if np.all(rgb_data == 0):
                    return None

                img = convert_image_from_array(rgb_data)
                img_resize = resize_image(img, tile_size)
                img_transparency = convert_image_transparency(img_resize)
                del ds
                # return convert_image_to_bytes(img_transparency)
                return img_transparency

            elif 0 <= x0 < width and x1 < width and 0 <= y0 < height and y1 >= height:  # situation 11'
                rgb_data = np.zeros(((int(y1 / times) - int(y0 / times)), (int(x1 / times) - int(x0 / times)), 3),
                                    dtype=np.uint8)
                band_part_data = np.dstack([ds.GetRasterBand(n + 1).ReadAsArray(x0, y0, (x1 - x0), (height - y0),
                                                                                (int(
                                                                                    x1 / times) - int(x0 / times)),
                                                                                (int(height / times) - int(y0 / times)))
                                            for n in range(ds.RasterCount)])
                rgb_data[0:(int(height / times) - int(y0 / times)), 0:(int(x1 / times) - int(x0 / times)),
                         :] = band_part_data

                if np.all(rgb_data == 0):
                    return None

                img = convert_image_from_array(rgb_data)
                img_resize = resize_image(img, tile_size)
                img_transparency = convert_image_transparency(img_resize)
                del ds
                # return convert_image_to_bytes(img_transparency)
                return img_transparency

            elif x0 < 0 and x1 >= width and 0 <= y0 < height and y1 >= height:  # situation 12'
                rgb_data = np.zeros(((int(y1 / times) - int(y0 / times)), (int(x1 / times) - int(x0 / times)), 3),
                                    dtype=np.uint8)
                band_part_data = np.dstack([ds.GetRasterBand(n + 1).ReadAsArray(0, y0, width, (height - y0),
                                                                                int(width /
                                                                                    times),
                                                                                (int(height / times) - int(y0 / times)))
                                            for n in range(ds.RasterCount)])
                rgb_data[0:(int(height / times) - int(y0 / times)),
                         int((0 - x0) / times):(int(width / times) - int(x0 / times)), :] = band_part_data

                if np.all(rgb_data == 0):
                    return None

                img = convert_image_from_array(rgb_data)
                img_resize = resize_image(img, tile_size)
                img_transparency = convert_image_transparency(img_resize)
                del ds
                # return convert_image_to_bytes(img_transparency)
                return img_transparency

            else:  # 可能还包含一些没想到的特殊情况，遇到了再做进一步判断和处理
                print("blank tile data!")
                blank = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR4nGP4//8/AwAI/AL+p5qgoAAAAABJRU5ErkJggg=="
                img = base64.b64decode(blank)
                img = Image.open(BytesIO(img))
                return None

        else:
            if x0 < 0 and 0 <= x1 < width and y0 < 0 and y1 < height:  # situation 1
                rgb_data = np.zeros((y1 - y0, x1 - x0, 3), dtype=np.uint8)
                band_part_data = np.dstack(
                    [ds.GetRasterBand(n + 1).ReadAsArray(0, 0, x1, y1) for n in range(ds.RasterCount)])
                rgb_data[(0 - y0):(y1 - y0), (0 - x0):(x1 - x0), :] = band_part_data

                if np.all(rgb_data == 0):
                    return None

                img = convert_image_from_array(rgb_data)
                img_resize = resize_image(img, tile_size)
                img_transparency = convert_image_transparency(img_resize)
                del ds
                # return convert_image_to_bytes(img_transparency)
                return img_transparency

            elif x0 < 0 and 0 <= x1 < width and 0 <= y0 < height and y1 >= height:  # situation 2
                rgb_data = np.zeros((y1 - y0, x1 - x0, 3), dtype=np.uint8)
                band_part_data = np.dstack(
                    [ds.GetRasterBand(n + 1).ReadAsArray(0, y0, x1, (height - y0)) for n in range(ds.RasterCount)])
                rgb_data[0:(height - y0), (0 - x0):(x1 - x0), :] = band_part_data

                if np.all(rgb_data == 0):
                    return None

                img = convert_image_from_array(rgb_data)
                img_resize = resize_image(img, tile_size)
                img_transparency = convert_image_transparency(img_resize)
                del ds
                # return convert_image_to_bytes(img_transparency)
                return img_transparency

            elif 0 <= x0 < width and x1 >= width and y0 < 0 and 0 <= y1 < height:  # situation 3
                rgb_data = np.zeros((y1 - y0, x1 - x0, 3), dtype=np.uint8)
                band_part_data = np.dstack(
                    [ds.GetRasterBand(n + 1).ReadAsArray(x0, 0, (width - x0), y1) for n in range(ds.RasterCount)])
                rgb_data[(0 - y0):(y1 - y0), 0:(width - x0),
                         :] = band_part_data

                if np.all(rgb_data == 0):
                    return None

                img = convert_image_from_array(rgb_data)
                img_resize = resize_image(img, tile_size)
                img_transparency = convert_image_transparency(img_resize)
                del ds
                # return convert_image_to_bytes(img_transparency)
                return img_transparency

            elif 0 <= x0 < width and x1 >= width and 0 <= y0 < height and y1 >= height:  # situation 4
                rgb_data = np.zeros((y1 - y0, x1 - x0, 3), dtype=np.uint8)
                band_part_data = np.dstack(
                    [ds.GetRasterBand(n + 1).ReadAsArray(x0, y0, (width - x0), (height - y0)) for n in
                     range(ds.RasterCount)])
                rgb_data[0:(height - y0), 0:(width - x0), :] = band_part_data

                if np.all(rgb_data == 0):
                    return None

                img = convert_image_from_array(rgb_data)
                img_resize = resize_image(img, tile_size)
                img_transparency = convert_image_transparency(img_resize)
                del ds
                # return convert_image_to_bytes(img_transparency)
                return img_transparency

            elif x0 < 0 and 0 <= x1 < width and y0 >= 0 and y1 < height:  # situation 5
                rgb_data = np.zeros((y1 - y0, x1 - x0, 3), dtype=np.uint8)
                band_part_data = np.dstack(
                    [ds.GetRasterBand(n + 1).ReadAsArray(0, y0, x1, (y1 - y0)) for n in range(ds.RasterCount)])
                rgb_data[0:(y1 - y0), (0 - x0):(x1 - x0), :] = band_part_data

                if np.all(rgb_data == 0):
                    return None

                img = convert_image_from_array(rgb_data)
                img_resize = resize_image(img, tile_size)
                img_transparency = convert_image_transparency(img_resize)
                del ds
                # return convert_image_to_bytes(img_transparency)
                return img_transparency

            elif x0 < 0 and 0 <= x1 < width and y0 < 0 and y1 >= height:  # situation 6
                rgb_data = np.zeros((y1 - y0, x1 - x0, 3), dtype=np.uint8)
                band_part_data = np.dstack(
                    [ds.GetRasterBand(n + 1).ReadAsArray(0, 0, x1, height) for n in range(ds.RasterCount)])
                rgb_data[(0 - y0):(height - y0), (0 - x0):(x1 - x0), :] = band_part_data

                if np.all(rgb_data == 0):
                    return None

                img = convert_image_from_array(rgb_data)
                img_resize = resize_image(img, tile_size)
                img_transparency = convert_image_transparency(img_resize)
                del ds
                # return convert_image_to_bytes(img_transparency)
                return img_transparency

            elif 0 <= x0 < width and x1 < width and y0 < 0 and 0 <= y1 < height:  # situation 7
                rgb_data = np.zeros((y1 - y0, x1 - x0, 3), dtype=np.uint8)
                band_part_data = np.dstack(
                    [ds.GetRasterBand(n + 1).ReadAsArray(x0, 0, (x1 - x0), y1) for n in range(ds.RasterCount)])
                rgb_data[(0 - y0):(y1 - y0), 0:(x1 - x0), :] = band_part_data

                if np.all(rgb_data == 0):
                    return None

                img = convert_image_from_array(rgb_data)
                img_resize = resize_image(img, tile_size)
                img_transparency = convert_image_transparency(img_resize)
                del ds
                # return convert_image_to_bytes(img_transparency)
                return img_transparency

            elif x0 < 0 and x1 >= width and y0 < 0 and 0 <= y1 < height:  # situation 8
                rgb_data = np.zeros((y1 - y0, x1 - x0, 3), dtype=np.uint8)
                band_part_data = np.dstack(
                    [ds.GetRasterBand(n + 1).ReadAsArray(0, 0, width, y1) for n in range(ds.RasterCount)])
                rgb_data[(0 - y0):(y1 - y0), (0 - x0):(width - x0), :] = band_part_data

                if np.all(rgb_data == 0):
                    return None

                img = convert_image_from_array(rgb_data)
                img_resize = resize_image(img, tile_size)
                img_transparency = convert_image_transparency(img_resize)
                del ds
                # return convert_image_to_bytes(img_transparency)
                return img_transparency

            elif 0 <= x0 < width and width <= x1 and y0 >= 0 and y1 < height:  # situation 9
                rgb_data = np.zeros((y1 - y0, x1 - x0, 3), dtype=np.uint8)
                band_part_data = np.dstack(
                    [ds.GetRasterBand(n + 1).ReadAsArray(x0, y0, (width - x0), (y1 - y0)) for n in
                     range(ds.RasterCount)])
                rgb_data[0:(y1 - y0), 0:(width - x0), :] = band_part_data

                if np.all(rgb_data == 0):
                    return None

                img = convert_image_from_array(rgb_data)
                img_resize = resize_image(img, tile_size)
                img_transparency = convert_image_transparency(img_resize)
                del ds
                # return convert_image_to_bytes(img_transparency)
                return img_transparency

            elif 0 <= x0 < width and x1 >= width and y0 < 0 and y1 >= height:  # situation 10
                rgb_data = np.zeros((y1 - y0, x1 - x0, 3), dtype=np.uint8)
                band_part_data = np.dstack(
                    [ds.GetRasterBand(n + 1).ReadAsArray(x0, 0, (width - x0), height) for n in range(ds.RasterCount)])
                rgb_data[(0 - y0):(height - y0),
                         0:(width - x0), :] = band_part_data

                if np.all(rgb_data == 0):
                    return None

                img = convert_image_from_array(rgb_data)
                img_resize = resize_image(img, tile_size)
                img_transparency = convert_image_transparency(img_resize)
                del ds
                # return convert_image_to_bytes(img_transparency)
                return img_transparency

            elif 0 <= x0 < width and x1 < width and 0 <= y0 < height and y1 >= height:  # situation 11
                rgb_data = np.zeros((y1 - y0, x1 - x0, 3), dtype=np.uint8)
                band_part_data = np.dstack(
                    [ds.GetRasterBand(n + 1).ReadAsArray(x0, y0, (x1 - x0), (height - y0)) for n in
                     range(ds.RasterCount)])
                rgb_data[0:(height - y0), 0:(x1 - x0), :] = band_part_data

                if np.all(rgb_data == 0):
                    return None

                img = convert_image_from_array(rgb_data)
                img_resize = resize_image(img, tile_size)
                img_transparency = convert_image_transparency(img_resize)
                del ds
                # return convert_image_to_bytes(img_transparency)
                return img_transparency

            elif x0 < 0 and x1 >= width and 0 <= y0 < height and y1 >= height:  # situation 12
                rgb_data = np.zeros((y1 - y0, x1 - x0, 3), dtype=np.uint8)
                band_part_data = np.dstack(
                    [ds.GetRasterBand(n + 1).ReadAsArray(0, y0, width, (height - y0)) for n in range(ds.RasterCount)])
                rgb_data[0:(height - y0), (0 - x0):(width - x0), :] = band_part_data

                if np.all(rgb_data == 0):
                    return None

                img = convert_image_from_array(rgb_data)
                img_resize = resize_image(img, tile_size)
                img_transparency = convert_image_transparency(img_resize)
                del ds
                # return convert_image_to_bytes(img_transparency)
                return img_transparency

            else:  # 可能还包含一些没想到的特殊情况，遇到了再做进一步判断和处理
                print("blank tile data!")
                blank = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR4nGP4//8/AwAI/AL+p5qgoAAAAABJRU5ErkJggg=="
                img = base64.b64decode(blank)
                img = Image.open(BytesIO(img))
                return None


def read_geotiff_by_tile(zoom, x, y, tile_size, dataset, zoom_divide):
    """
    获取影像的子集
    """
    # lon_min, lat_min, lon_max, lat_max = tile2boundary(zoom, x, y)
    # bbox = [lon_min, lat_min, lon_max, lat_max]
    # projwin = (lon_min, lat_max, lon_max, lat_min)
    ds = dataset
    # if zoom == int((end_zoom + start_zoom)/2):
    #     ds = dataset
    # else:
    #     ds = get_geotiff_subset(dataset, zoom, x, y)

    band = ds.GetRasterBand(1)
    width = band.XSize
    height = band.YSize
    # del band
    # band_count = ds.RasterCount
    # print(band_count)

    # Define the geotransform used to convert x/y pixel to lon/lat degree
    geotransform = ds.GetGeoTransform()

    # The inverse geotransform is used to convert lon/lat degrees to x/y pixel index
    inv_geotransform = gdal.InvGeoTransform(geotransform)

    # # Define a longitude/latitude bounding box in degrees
    bbox = tile2boundary(zoom, x, y)

    # Convert lon/lat degrees to x/y pixel for the dataset
    _x0, _y0 = gdal.ApplyGeoTransform(inv_geotransform, bbox[0], bbox[1])
    _x1, _y1 = gdal.ApplyGeoTransform(inv_geotransform, bbox[2], bbox[3])
    x0, y0 = int(min(_x0, _x1)), int(min(_y0, _y1))
    x1, y1 = int(max(_x0, _x1)), int(max(_y0, _y1))
    if zoom <= zoom_divide:
        if ((x1 - x0) / tile_size) > 5 or ((y1 - y0) / tile_size) > 5:  # 请求层级太小，内存溢出处理
            times = get_resize_times((x1 - x0), (y1 - y0), tile_size)  # 缩放倍数
            band_part_data = np.dstack(
                [ds.GetRasterBand(n + 1).ReadAsArray(0, 0, width, height, int(width / times), int(height / times)) for n
                 in range(ds.RasterCount)])
            # rgb_data[int((0 - y0) / times):int(height / times) - int(y0 / times),
            # int((0 - x0) / times):int(width / times) - int(x0 / times), :] = band_part_data

            # img = convert_image_from_array(rgb_data)

            if np.all(band_part_data == 0):
                return None
            img = convert_image_from_array(band_part_data)
            img_resize = resize_image(img, tile_size)
            img_transparency = convert_image_transparency(img_resize)
            del ds
            # return convert_image_to_bytes(img_transparency)
            return img_transparency
        else:
            band_part_data = np.dstack(
                [ds.GetRasterBand(n + 1).ReadAsArray(0, 0, width, height) for n
                 in range(ds.RasterCount)])
            # rgb_data[int((0 - y0) / times):int(height / times) - int(y0 / times),
            # int((0 - x0) / times):int(width / times) - int(x0 / times), :] = band_part_data

            # img = convert_image_from_array(rgb_data)
            if np.all(band_part_data == 0):
                return None
            img = convert_image_from_array(band_part_data)
            img_resize = resize_image(img, tile_size)
            img_transparency = convert_image_transparency(img_resize)
            del ds
            # return convert_image_to_bytes(img_transparency)
            return img_transparency
    else:
        rgb_data = np.dstack([ds.GetRasterBand(n + 1).ReadAsArray(int(x0), int(y0), int(x1 - x0), int(y1 - y0)) for n in
                              range(ds.RasterCount)])

        if np.all(rgb_data == 0):
            return None

        img = convert_image_from_array(rgb_data)
        img_resize = resize_image(img, tile_size)
        img_transparency = convert_image_transparency(img_resize)
        del ds
        # return convert_image_to_bytes(img_transparency)
        return img_transparency


if __name__ == '__main__':
    geotiff_path = r"D:\lanzhou_2m_test.tif"
    dataset = gdal.Open(geotiff_path)
    dataset_subset = get_geotiff_subset(dataset, 15, 6455, 3214)
    dset_tiff_out = gdal.GetDriverByName('GTiff')
    dset_tiff_out.CreateCopy('13_6455_3214.tif', dataset_subset, 1)
