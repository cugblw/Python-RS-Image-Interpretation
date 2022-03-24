import numpy as np
from PIL import Image
from osgeo import gdal,gdalconst
import raster_arr_test as arr
from tile_convert import tile2boundary

# Path to a tiff file covering the globe
# http://visibleearth.nasa.gov/view.php?id=57752
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

tile_size = 256

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
# bbox = [101.66748046875, 3.1405161039832308, 101.689453125, 3.1624555302378496] # 14, 12819, 8048
# bbox = [101.25, 2.8113711933311265, 101.953125, 3.5134210456400297] # 9, 400, 251
# bbox = [101.77734375, 3.0746950723696784, 101.865234375, 3.1624555302378496] # 12,3206,2012
# bbox = [101.6015625, 3.1624555302378496, 101.689453125, 3.2502085616531673] # 任意
# bbox = tile2boundary(14,12822,8048)
bbox = tile2boundary(9,421,192)

# Convert lon/lat degrees to x/y pixel for the dataset
_x0, _y0 = gdal.ApplyGeoTransform(inv_geotransform, bbox[0], bbox[1])
_x1, _y1 = gdal.ApplyGeoTransform(inv_geotransform, bbox[2], bbox[3])
x0, y0 = int(min(_x0, _x1)), int(min(_y0, _y1))
x1, y1 = int(max(_x0, _x1)), int(max(_y0, _y1))
print(x0,y0,x1,y1)

# Get subset of the raster as a numpy array
# data = band.ReadAsArray(int(x0), int(y0), int(x1-x0), int(y1-y0))
""" band1_data = ds.GetRasterBand(1).ReadAsArray(int(x0), int(y0), int(x1-x0), int(y1-y0))
band2_data = ds.GetRasterBand(2).ReadAsArray(int(x0), int(y0), int(x1-x0), int(y1-y0))
band3_data = ds.GetRasterBand(3).ReadAsArray(int(x0), int(y0), int(x1-x0), int(y1-y0)) """

# band1_data = ds.GetRasterBand(1).ReadAsArray(width-1, height-1, 1, 1)
# band2_data = ds.GetRasterBand(2).ReadAsArray(width-1, height-1, 1, 1)
# band3_data = ds.GetRasterBand(3).ReadAsArray(width-1, height-1, 1, 1)


# 通过瓦片位置，对应查找影像区域，进行切取
if x0 >= 0 and y0 >= 0 and x1 < width and y1 < height:  # 请求瓦片完全在影像内部
    band1_data = ds.GetRasterBand(1).ReadAsArray(int(x0), int(y0), int(x1-x0), int(y1-y0))
    band2_data = ds.GetRasterBand(2).ReadAsArray(int(x0), int(y0), int(x1-x0), int(y1-y0))
    band3_data = ds.GetRasterBand(3).ReadAsArray(int(x0), int(y0), int(x1-x0), int(y1-y0))

elif x1 < 0 or y1 < 0 or x0 >= width or y0 >= height: # 请求瓦片完全在影像外部
    band1_data = np.zeros((tile_size,tile_size))
    band2_data = np.zeros((tile_size,tile_size))
    band3_data = np.zeros((tile_size,tile_size))

elif x0 <= 0 and y0 <= 0 and x1 >= width and y1 >= height: # 请求瓦片完全包裹影像
    if ((x1-x0)/tile_size) > 5 or ((y1-y0)/tile_size) > 5: # 请求层级太小，内存溢出处理
        times = arr.get_resize_times((x1-x0),(y1-y0),tile_size) # 缩放倍数

        band1_part_data = ds.GetRasterBand(1).ReadAsArray(0, 0, width, height, int(width/times), int(height/times))
        band2_part_data = ds.GetRasterBand(2).ReadAsArray(0, 0, width, height, int(width/times), int(height/times))
        band3_part_data = ds.GetRasterBand(3).ReadAsArray(0, 0, width, height, int(width/times), int(height/times))

        band1_data = np.zeros((int((y1-y0)/times),int((x1-x0)/times)))
        band2_data = np.zeros((int((y1-y0)/times),int((x1-x0)/times)))
        band3_data = np.zeros((int((y1-y0)/times),int((x1-x0)/times)))

        band1_data[int((0-y0)/times):int(height/times) - int(y0/times),int((0-x0)/times):int(width/times)-int(x0/times)] = band1_part_data
        band2_data[int((0-y0)/times):int(height/times) - int(y0/times),int((0-x0)/times):int(width/times)-int(x0/times)] = band2_part_data
        band3_data[int((0-y0)/times):int(height/times) - int(y0/times),int((0-x0)/times):int(width/times)-int(x0/times)] = band3_part_data

    else:
        band1_part_data = ds.GetRasterBand(1).ReadAsArray(0, 0, width, height)
        band2_part_data = ds.GetRasterBand(2).ReadAsArray(0, 0, width, height)
        band3_part_data = ds.GetRasterBand(3).ReadAsArray(0, 0, width, height)

        band1_data = np.zeros((y1-y0,x1-x0))
        band2_data = np.zeros((y1-y0,x1-x0))
        band3_data = np.zeros((y1-y0,x1-x0))

        band1_data[(0-y0):(height-y0),(0-x0):(width-x0)] = band1_part_data
        band2_data[(0-y0):(height-y0),(0-x0):(width-x0)] = band2_part_data
        band3_data[(0-y0):(height-y0),(0-x0):(width-x0)] = band3_part_data

else: # 请求瓦片部分包含影像
    if ((x1-x0)/tile_size) > 5 or ((y1-y0)/tile_size) > 5: # 请求层级太小，内存溢出处理
        times = arr.get_resize_times((x1-x0),(y1-y0),tile_size) # 缩放倍数
        
        if x0 < 0 and 0 <= x1 < width and y0 < 0  and y1 < height: # situation 1'
            band1_part_data =  ds.GetRasterBand(1).ReadAsArray(0, 0, x1, y1, int(x1/times), int(y1/times))
            band2_part_data =  ds.GetRasterBand(2).ReadAsArray(0, 0, x1, y1, int(x1/times), int(y1/times))
            band3_part_data =  ds.GetRasterBand(3).ReadAsArray(0, 0, x1, y1, int(x1/times), int(y1/times))

            band1_data = np.zeros(((int(y1/times)-int(y0/times)),(int(x1/times)-int(x0/times))))
            band2_data = np.zeros(((int(y1/times)-int(y0/times)),(int(x1/times)-int(x0/times))))
            band3_data = np.zeros(((int(y1/times)-int(y0/times)),(int(x1/times)-int(x0/times))))

            band1_data[int((0-y0)/times):(int(y1/times)-int(y0/times)),int((0-x0)/times):(int(x1/times)-int(x0/times))] = band1_part_data
            band2_data[int((0-y0)/times):(int(y1/times)-int(y0/times)),int((0-x0)/times):(int(x1/times)-int(x0/times))] = band2_part_data
            band3_data[int((0-y0)/times):(int(y1/times)-int(y0/times)),int((0-x0)/times):(int(x1/times)-int(x0/times))] = band3_part_data

        elif x0 < 0 and 0 <= x1 < width and 0 <= y0 < height and y1 >= height:# situation 2'
            band1_part_data =  ds.GetRasterBand(1).ReadAsArray(0, y0, x1, (height-y0), int(x1/times), (int(height/times)-int(y0/times)))
            band2_part_data =  ds.GetRasterBand(2).ReadAsArray(0, y0, x1, (height-y0), int(x1/times), (int(height/times)-int(y0/times)))
            band3_part_data =  ds.GetRasterBand(3).ReadAsArray(0, y0, x1, (height-y0), int(x1/times), (int(height/times)-int(y0/times)))

            band1_data = np.zeros(((int(y1/times)-int(y0/times)),(int(x1/times)-int(x0/times))))
            band2_data = np.zeros(((int(y1/times)-int(y0/times)),(int(x1/times)-int(x0/times))))
            band3_data = np.zeros(((int(y1/times)-int(y0/times)),(int(x1/times)-int(x0/times))))

            band1_data[0:(int(height/times)-int(y0/times)),int((0-x0)/times):(int(x1/times)-int(x0/times))] = band1_part_data
            band2_data[0:(int(height/times)-int(y0/times)),int((0-x0)/times):(int(x1/times)-int(x0/times))] = band2_part_data
            band3_data[0:(int(height/times)-int(y0/times)),int((0-x0)/times):(int(x1/times)-int(x0/times))] = band3_part_data
        
        elif 0 <= x0 < width and x1 >= width and y0 < 0 and 0 <= y1 < height: # situation 3'
            band1_part_data =  ds.GetRasterBand(1).ReadAsArray(x0, 0, (width-x0), y1, int((width-x0)/times), int(y1/times))
            band2_part_data =  ds.GetRasterBand(2).ReadAsArray(x0, 0, (width-x0), y1, int((width-x0)/times), int(y1/times))
            band3_part_data =  ds.GetRasterBand(3).ReadAsArray(x0, 0, (width-x0), y1, int((width-x0)/times), int(y1/times))
            
            band1_data = np.zeros(((int(y1/times)-int(y0/times)),(int(x1/times)-int(x0/times))))
            band2_data = np.zeros(((int(y1/times)-int(y0/times)),(int(x1/times)-int(x0/times))))
            band3_data = np.zeros(((int(y1/times)-int(y0/times)),(int(x1/times)-int(x0/times))))

            band1_data[int((0-y0)/times):(int(y1/times)-int(y0/times)),0:(int(width/times)-int(x0/times))] = band1_part_data
            band2_data[int((0-y0)/times):(int(y1/times)-int(y0/times)),0:(int(width/times)-int(x0/times))] = band2_part_data
            band3_data[int((0-y0)/times):(int(y1/times)-int(y0/times)),0:(int(width/times)-int(x0/times))] = band3_part_data

        elif 0 <= x0 < width and x1 >= width and 0 <= y0 < height and y1 >= height: # situation 4'
            band1_part_data =  ds.GetRasterBand(1).ReadAsArray(x0, y0, (width-x0), (height-y0), int((width-x0)/times),int((height-y0)/times))
            band2_part_data =  ds.GetRasterBand(2).ReadAsArray(x0, y0, (width-x0), (height-y0), int((width-x0)/times),int((height-y0)/times))
            band3_part_data =  ds.GetRasterBand(3).ReadAsArray(x0, y0, (width-x0), (height-y0), int((width-x0)/times),int((height-y0)/times))
            
            band1_data = np.zeros(((int(y1/times)-int(y0/times)),(int(x1/times)-int(x0/times))))
            band2_data = np.zeros(((int(y1/times)-int(y0/times)),(int(x1/times)-int(x0/times))))
            band3_data = np.zeros(((int(y1/times)-int(y0/times)),(int(x1/times)-int(x0/times))))

            band1_data[0:(int(height/times)-int(y0/times)),0:(int(width/times)-int(x0/times))] = band1_part_data
            band2_data[0:(int(height/times)-int(y0/times)),0:(int(width/times)-int(x0/times))] = band2_part_data
            band3_data[0:(int(height/times)-int(y0/times)),0:(int(width/times)-int(x0/times))] = band3_part_data

        elif x0 < 0 and 0 <= x1 < width and y0 >= 0 and y1 < height: # situation 5'
            band1_part_data =  ds.GetRasterBand(1).ReadAsArray(0, y0, x1, (y1-y0), int(x1/times),int((y1-y0)/times))
            band2_part_data =  ds.GetRasterBand(2).ReadAsArray(0, y0, x1, (y1-y0), int(x1/times),int((y1-y0)/times))
            band3_part_data =  ds.GetRasterBand(3).ReadAsArray(0, y0, x1, (y1-y0), int(x1/times),int((y1-y0)/times))
            
            band1_data = np.zeros(((int(y1/times)-int(y0/times)),(int(x1/times)-int(x0/times))))
            band2_data = np.zeros(((int(y1/times)-int(y0/times)),(int(x1/times)-int(x0/times))))
            band3_data = np.zeros(((int(y1/times)-int(y0/times)),(int(x1/times)-int(x0/times))))

            band1_data[0:(int(y1/times)-int(y0/times)),int((0-x0)/times):(int(x1/times)-int(x0/times))] = band1_part_data
            band2_data[0:(int(y1/times)-int(y0/times)),int((0-x0)/times):(int(x1/times)-int(x0/times))] = band2_part_data
            band3_data[0:(int(y1/times)-int(y0/times)),int((0-x0)/times):(int(x1/times)-int(x0/times))] = band3_part_data

        elif x0 < 0 and 0 <= x1 < width and y0 < 0 and y1 >= height: # situation 6'
            band1_part_data =  ds.GetRasterBand(1).ReadAsArray(0, 0, x1, height, int(x1/times), int(height/times))
            band2_part_data =  ds.GetRasterBand(2).ReadAsArray(0, 0, x1, height, int(x1/times), int(height/times))
            band3_part_data =  ds.GetRasterBand(3).ReadAsArray(0, 0, x1, height, int(x1/times), int(height/times))
            
            band1_data = np.zeros(((int(y1/times)-int(y0/times)),(int(x1/times)-int(x0/times))))
            band2_data = np.zeros(((int(y1/times)-int(y0/times)),(int(x1/times)-int(x0/times))))
            band3_data = np.zeros(((int(y1/times)-int(y0/times)),(int(x1/times)-int(x0/times))))

            band1_data[int((0-y0)/times):(int(height/times)-int(y0/times)),int((0-x0)/times):(int(x1/times)-int(x0/times))] = band1_part_data
            band2_data[int((0-y0)/times):(int(height/times)-int(y0/times)),int((0-x0)/times):(int(x1/times)-int(x0/times))] = band2_part_data
            band3_data[int((0-y0)/times):(int(height/times)-int(y0/times)),int((0-x0)/times):(int(x1/times)-int(x0/times))] = band3_part_data
        elif 0 <= x0 < width and x1 < width and y0 < 0 and 0 <= y1 <height: # situation 7'
            band1_part_data =  ds.GetRasterBand(1).ReadAsArray(x0, 0, (x1-x0), y1, int((x1-x0)/times), int(y1/times))
            band2_part_data =  ds.GetRasterBand(2).ReadAsArray(x0, 0, (x1-x0), y1, int((x1-x0)/times), int(y1/times))
            band3_part_data =  ds.GetRasterBand(3).ReadAsArray(x0, 0, (x1-x0), y1, int((x1-x0)/times), int(y1/times))
            
            band1_data = np.zeros(((int(y1/times)-int(y0/times)),(int(x1/times)-int(x0/times))))
            band2_data = np.zeros(((int(y1/times)-int(y0/times)),(int(x1/times)-int(x0/times))))
            band3_data = np.zeros(((int(y1/times)-int(y0/times)),(int(x1/times)-int(x0/times))))

            band1_data[int((0-y0)/times):(int(y1/times)-int(y0/times)),0:(int(x1/times)-int(x0/times))] = band1_part_data
            band2_data[int((0-y0)/times):(int(y1/times)-int(y0/times)),0:(int(x1/times)-int(x0/times))] = band2_part_data
            band3_data[int((0-y0)/times):(int(y1/times)-int(y0/times)),0:(int(x1/times)-int(x0/times))] = band3_part_data

        elif x0 < 0 and x1 >= width and y0 < 0 and 0 <= y1 < height: # situation 8'
            band1_part_data =  ds.GetRasterBand(1).ReadAsArray(0, 0, width, y1, int(width/times), int(y1/times))
            band2_part_data =  ds.GetRasterBand(2).ReadAsArray(0, 0, width, y1, int(width/times), int(y1/times))
            band3_part_data =  ds.GetRasterBand(3).ReadAsArray(0, 0, width, y1, int(width/times), int(y1/times))
            
            band1_data = np.zeros(((int(y1/times)-int(y0/times)),(int(x1/times)-int(x0/times))))
            band2_data = np.zeros(((int(y1/times)-int(y0/times)),(int(x1/times)-int(x0/times))))
            band3_data = np.zeros(((int(y1/times)-int(y0/times)),(int(x1/times)-int(x0/times))))

            band1_data[int((0-y0)/times):(int(y1/times)-int(y0/times)),int((0-x0)/times):(int(width/times)-int(x0/times))] = band1_part_data
            band2_data[int((0-y0)/times):(int(y1/times)-int(y0/times)),int((0-x0)/times):(int(width/times)-int(x0/times))] = band2_part_data
            band3_data[int((0-y0)/times):(int(y1/times)-int(y0/times)),int((0-x0)/times):(int(width/times)-int(x0/times))] = band3_part_data

        elif 0 <= x0 < width and x1 >= width and y0 >= 0 and y1 < height: # situation 9'
            band1_part_data =  ds.GetRasterBand(1).ReadAsArray(x0, y0, (width-x0), (y1-y0), (int(width/times)-int(x0/times)), (int(y1/times)-int(y0/times)))
            band2_part_data =  ds.GetRasterBand(2).ReadAsArray(x0, y0, (width-x0), (y1-y0), (int(width/times)-int(x0/times)), (int(y1/times)-int(y0/times)))
            band3_part_data =  ds.GetRasterBand(3).ReadAsArray(x0, y0, (width-x0), (y1-y0), (int(width/times)-int(x0/times)), (int(y1/times)-int(y0/times)))
            print("-----------------------")
            print(band1_part_data.shape)
            print(int(y1/times)-int(y0/times))
            
            band1_data = np.zeros(((int(y1/times)-int(y0/times)),(int(x1/times)-int(x0/times))))
            band2_data = np.zeros(((int(y1/times)-int(y0/times)),(int(x1/times)-int(x0/times))))
            band3_data = np.zeros(((int(y1/times)-int(y0/times)),(int(x1/times)-int(x0/times))))
            

            print("======================")
            print((int(y1/times)-int(y0/times)))
            print(int(width/times)-int(x0/times))
            print((band1_data[0:(int(y1/times)-int(y0/times)),0:(int(width/times)-int(x0/times))]).shape)

            band1_data[0:(int(y1/times)-int(y0/times)),0:(int(width/times)-int(x0/times))] = band1_part_data
            band2_data[0:(int(y1/times)-int(y0/times)),0:(int(width/times)-int(x0/times))] = band2_part_data
            band3_data[0:(int(y1/times)-int(y0/times)),0:(int(width/times)-int(x0/times))] = band3_part_data

        elif 0 <= x0 < width and x1 >= width and y0 < 0 and y1 >= height: # situation 10'
            band1_part_data =  ds.GetRasterBand(1).ReadAsArray(x0, 0, (width-x0), height, int((width-x0)/times), int(height/times))
            band2_part_data =  ds.GetRasterBand(2).ReadAsArray(x0, 0, (width-x0), height, int((width-x0)/times), int(height/times))
            band3_part_data =  ds.GetRasterBand(3).ReadAsArray(x0, 0, (width-x0), height, int((width-x0)/times), int(height/times))
            
            band1_data = np.zeros(((int(y1/times)-int(y0/times)),(int(x1/times)-int(x0/times))))
            band2_data = np.zeros(((int(y1/times)-int(y0/times)),(int(x1/times)-int(x0/times))))
            band3_data = np.zeros(((int(y1/times)-int(y0/times)),(int(x1/times)-int(x0/times))))

            band1_data[int((0-y0)/times):(int(height/times)-int(y0/times)),0:(int(width/times)-int(x0/times))] = band1_part_data
            band2_data[int((0-y0)/times):(int(height/times)-int(y0/times)),0:(int(width/times)-int(x0/times))] = band2_part_data
            band3_data[int((0-y0)/times):(int(height/times)-int(y0/times)),0:(int(width/times)-int(x0/times))] = band3_part_data


        elif 0 <= x0 <width and x1 < width and 0 <= y0 < height and y1 >= height: # situation 11'
            band1_part_data =  ds.GetRasterBand(1).ReadAsArray(x0, y0, (x1-x0), (height-y0), int((x1-x0)/times), int((height-y0)/times))
            band2_part_data =  ds.GetRasterBand(2).ReadAsArray(x0, y0, (x1-x0), (height-y0), int((x1-x0)/times), int((height-y0)/times))
            band3_part_data =  ds.GetRasterBand(3).ReadAsArray(x0, y0, (x1-x0), (height-y0), int((x1-x0)/times), int((height-y0)/times))
            
            band1_data = np.zeros(((int(y1/times)-int(y0/times)),(int(x1/times)-int(x0/times))))
            band2_data = np.zeros(((int(y1/times)-int(y0/times)),(int(x1/times)-int(x0/times))))
            band3_data = np.zeros(((int(y1/times)-int(y0/times)),(int(x1/times)-int(x0/times))))

            band1_data[0:(int(height/times)-int(y0/times)),0:(int(x1/times)-int(x0/times))] = band1_part_data
            band2_data[0:(int(height/times)-int(y0/times)),0:(int(x1/times)-int(x0/times))] = band2_part_data
            band3_data[0:(int(height/times)-int(y0/times)),0:(int(x1/times)-int(x0/times))] = band3_part_data

        elif x0 < 0 and x1 >= width and 0 <= y0 < height  and y1 >= height: # situation 12'
            band1_part_data =  ds.GetRasterBand(1).ReadAsArray(0, y0, width, (height-y0), int(width/times), int((height-y0)/times))
            band2_part_data =  ds.GetRasterBand(2).ReadAsArray(0, y0, width, (height-y0), int(width/times), int((height-y0)/times))
            band3_part_data =  ds.GetRasterBand(3).ReadAsArray(0, y0, width, (height-y0), int(width/times), int((height-y0)/times))
            
            band1_data = np.zeros(((int(y1/times)-int(y0/times)),(int(x1/times)-int(x0/times))))
            band2_data = np.zeros(((int(y1/times)-int(y0/times)),(int(x1/times)-int(x0/times))))
            band3_data = np.zeros(((int(y1/times)-int(y0/times)),(int(x1/times)-int(x0/times))))

            band1_data[0:(int(height/times)-int(y0/times)),int((0-x0)/times):(int(width/times)-int(x0/times))] = band1_part_data
            band2_data[0:(int(height/times)-int(y0/times)),int((0-x0)/times):(int(width/times)-int(x0/times))] = band2_part_data
            band3_data[0:(int(height/times)-int(y0/times)),int((0-x0)/times):(int(width/times)-int(x0/times))] = band3_part_data
            
        else: #可能还包含一些没想到的特殊情况，遇到了再做进一步判断和处理
            band1_data = np.zeros((tile_size,tile_size))
            band2_data = np.zeros((tile_size,tile_size))
            band3_data = np.zeros((tile_size,tile_size))

    else:
        if x0 < 0 and 0 <= x1 < width and y0 < 0  and y1 < height: # situation 1
            band1_part_data =  ds.GetRasterBand(1).ReadAsArray(0, 0, x1, y1)
            band2_part_data =  ds.GetRasterBand(2).ReadAsArray(0, 0, x1, y1)
            band3_part_data =  ds.GetRasterBand(3).ReadAsArray(0, 0, x1, y1)

            band1_data = np.zeros((y1-y0,x1-x0))
            band2_data = np.zeros((y1-y0,x1-x0))
            band3_data = np.zeros((y1-y0,x1-x0))

            band1_data[(0-y0):(y1-y0),(0-x0):(x1-x0)] = band1_part_data
            band2_data[(0-y0):(y1-y0),(0-x0):(x1-x0)] = band2_part_data
            band3_data[(0-y0):(y1-y0),(0-x0):(x1-x0)] = band3_part_data

        elif x0 < 0 and 0 <= x1 < width and 0 <= y0 < height and y1 >= height:# situation 2
            band1_part_data =  ds.GetRasterBand(1).ReadAsArray(0, y0, x1, (height-y0))
            band2_part_data =  ds.GetRasterBand(2).ReadAsArray(0, y0, x1, (height-y0))
            band3_part_data =  ds.GetRasterBand(3).ReadAsArray(0, y0, x1, (height-y0))

            band1_data = np.zeros((y1-y0,x1-x0))
            band2_data = np.zeros((y1-y0,x1-x0))
            band3_data = np.zeros((y1-y0,x1-x0))

            band1_data[0:(height-y0),(0-x0):(x1-x0)] = band1_part_data
            band2_data[0:(height-y0),(0-x0):(x1-x0)] = band2_part_data
            band3_data[0:(height-y0),(0-x0):(x1-x0)] = band3_part_data
        
        elif 0 <= x0 < width and x1 >= width and y0 < 0 and 0 <= y1 < height: # situation 3
            band1_part_data =  ds.GetRasterBand(1).ReadAsArray(x0, 0, (width-x0), y1)
            band2_part_data =  ds.GetRasterBand(2).ReadAsArray(x0, 0, (width-x0), y1)
            band3_part_data =  ds.GetRasterBand(3).ReadAsArray(x0, 0, (width-x0), y1)
            
            band1_data = np.zeros((y1-y0,x1-x0))
            band2_data = np.zeros((y1-y0,x1-x0))
            band3_data = np.zeros((y1-y0,x1-x0))

            band1_data[(0-y0):(y1-y0),0:(width-x0)] = band1_part_data
            band2_data[(0-y0):(y1-y0),0:(width-x0)] = band2_part_data
            band3_data[(0-y0):(y1-y0),0:(width-x0)] = band3_part_data

        elif 0 <= x0 < width and x1 >= width and 0 <= y0 < height and y1 >= height: # situation 4
            band1_part_data =  ds.GetRasterBand(1).ReadAsArray(x0,y0,(width-x0),(height-y0))
            band2_part_data =  ds.GetRasterBand(2).ReadAsArray(x0,y0,(width-x0),(height-y0))
            band3_part_data =  ds.GetRasterBand(3).ReadAsArray(x0,y0,(width-x0),(height-y0))
            
            band1_data = np.zeros((y1-y0,x1-x0))
            band2_data = np.zeros((y1-y0,x1-x0))
            band3_data = np.zeros((y1-y0,x1-x0))

            band1_data[0:(height-y0),0:(width-x0)] = band1_part_data
            band2_data[0:(height-y0),0:(width-x0)] = band2_part_data
            band3_data[0:(height-y0),0:(width-x0)] = band3_part_data

        elif x0 < 0 and 0 <= x1 < width and y0 >= 0 and y1 < height: # situation 5
            band1_part_data =  ds.GetRasterBand(1).ReadAsArray(0,y0,x1,(y1-y0))
            band2_part_data =  ds.GetRasterBand(2).ReadAsArray(0,y0,x1,(y1-y0))
            band3_part_data =  ds.GetRasterBand(3).ReadAsArray(0,y0,x1,(y1-y0))
            
            band1_data = np.zeros((y1-y0,x1-x0))
            band2_data = np.zeros((y1-y0,x1-x0))
            band3_data = np.zeros((y1-y0,x1-x0))

            band1_data[0:(y1-y0),(0-x0):(x1-x0)] = band1_part_data
            band2_data[0:(y1-y0),(0-x0):(x1-x0)] = band2_part_data
            band3_data[0:(y1-y0),(0-x0):(x1-x0)] = band3_part_data

        elif x0 < 0 and 0 <= x1 < width and y0 < 0 and y1 >= height: # situation 6
            band1_part_data =  ds.GetRasterBand(1).ReadAsArray(0,0,x1,height)
            band2_part_data =  ds.GetRasterBand(2).ReadAsArray(0,0,x1,height)
            band3_part_data =  ds.GetRasterBand(3).ReadAsArray(0,0,x1,height)
            
            band1_data = np.zeros((y1-y0,x1-x0))
            band2_data = np.zeros((y1-y0,x1-x0))
            band3_data = np.zeros((y1-y0,x1-x0))

            band1_data[(0-y0):(height-y0),(0-x0):(x1-x0)] = band1_part_data
            band2_data[(0-y0):(height-y0),(0-x0):(x1-x0)] = band2_part_data
            band3_data[(0-y0):(height-y0),(0-x0):(x1-x0)] = band3_part_data
        elif 0 <= x0 < width and x1 < width and y0 < 0 and 0 <= y1 <height: # situation 7
            band1_part_data =  ds.GetRasterBand(1).ReadAsArray(x0,0,(x1-x0),y1)
            band2_part_data =  ds.GetRasterBand(2).ReadAsArray(x0,0,(x1-x0),y1)
            band3_part_data =  ds.GetRasterBand(3).ReadAsArray(x0,0,(x1-x0),y1)
            
            band1_data = np.zeros((y1-y0,x1-x0))
            band2_data = np.zeros((y1-y0,x1-x0))
            band3_data = np.zeros((y1-y0,x1-x0))

            band1_data[(0-y0):(y1-y0),0:(x1-x0)] = band1_part_data
            band2_data[(0-y0):(y1-y0),0:(x1-x0)] = band2_part_data
            band3_data[(0-y0):(y1-y0),0:(x1-x0)] = band3_part_data

        elif x0 < 0 and x1 >= width and y0 < 0 and 0 <= y1 < height: # situation 8
            band1_part_data =  ds.GetRasterBand(1).ReadAsArray(0,0,width,y1)
            band2_part_data =  ds.GetRasterBand(2).ReadAsArray(0,0,width,y1)
            band3_part_data =  ds.GetRasterBand(3).ReadAsArray(0,0,width,y1)
            
            band1_data = np.zeros((y1-y0,x1-x0))
            band2_data = np.zeros((y1-y0,x1-x0))
            band3_data = np.zeros((y1-y0,x1-x0))

            band1_data[(0-y0):(y1-y0),(0-x0):(width-x0)] = band1_part_data
            band2_data[(0-y0):(y1-y0),(0-x0):(width-x0)] = band2_part_data
            band3_data[(0-y0):(y1-y0),(0-x0):(width-x0)] = band3_part_data

        elif 0 <= x0 < width and x1 >= width and y0 >= 0 and y1  <height: # situation 9
            band1_part_data =  ds.GetRasterBand(1).ReadAsArray(x0,y0,(width-x0),(y1-y0))
            band2_part_data =  ds.GetRasterBand(2).ReadAsArray(x0,y0,(width-x0),(y1-y0))
            band3_part_data =  ds.GetRasterBand(3).ReadAsArray(x0,y0,(width-x0),(y1-y0))
            
            band1_data = np.zeros((y1-y0,x1-x0))
            band2_data = np.zeros((y1-y0,x1-x0))
            band3_data = np.zeros((y1-y0,x1-x0))

            band1_data[0:(y1-y0),0:(width-x0)] = band1_part_data
            band2_data[0:(y1-y0),0:(width-x0)] = band2_part_data
            band3_data[0:(y1-y0),0:(width-x0)] = band3_part_data

        elif 0 <= x0 < width and x1 >= width and y0 < 0 and y1 >= height: # situation 10
            band1_part_data =  ds.GetRasterBand(1).ReadAsArray(x0,0,(width-x0),height)
            band2_part_data =  ds.GetRasterBand(2).ReadAsArray(x0,0,(width-x0),height)
            band3_part_data =  ds.GetRasterBand(3).ReadAsArray(x0,0,(width-x0),height)
            
            band1_data = np.zeros((y1-y0,x1-x0))
            band2_data = np.zeros((y1-y0,x1-x0))
            band3_data = np.zeros((y1-y0,x1-x0))

            band1_data[(0-y0):(height-y0),0:(width-x0)] = band1_part_data
            band2_data[(0-y0):(height-y0),0:(width-x0)] = band2_part_data
            band3_data[(0-y0):(height-y0),0:(width-x0)] = band3_part_data


        elif 0 <= x0 <width and x1 < width and 0 <= y0 < height and y1 >= height: # situation 11
            band1_part_data =  ds.GetRasterBand(1).ReadAsArray(x0,y0,(x1-x0),(height-y0))
            band2_part_data =  ds.GetRasterBand(2).ReadAsArray(x0,y0,(x1-x0),(height-y0))
            band3_part_data =  ds.GetRasterBand(3).ReadAsArray(x0,y0,(x1-x0),(height-y0))
            
            band1_data = np.zeros((y1-y0,x1-x0))
            band2_data = np.zeros((y1-y0,x1-x0))
            band3_data = np.zeros((y1-y0,x1-x0))

            band1_data[0:(height-y0),0:(x1-x0)] = band1_part_data
            band2_data[0:(height-y0),0:(x1-x0)] = band2_part_data
            band3_data[0:(height-y0),0:(x1-x0)] = band3_part_data

        elif x0 < 0 and x1 >= width and 0 <= y0 < height  and y1 >= height: # situation 12
            band1_part_data =  ds.GetRasterBand(1).ReadAsArray(0,y0,width,(height-y0))
            band2_part_data =  ds.GetRasterBand(2).ReadAsArray(0,y0,width,(height-y0))
            band3_part_data =  ds.GetRasterBand(3).ReadAsArray(0,y0,width,(height-y0))
            
            band1_data = np.zeros((y1-y0,x1-x0))
            band2_data = np.zeros((y1-y0,x1-x0))
            band3_data = np.zeros((y1-y0,x1-x0))

            band1_data[0:(height-y0),(0-x0):(width-x0)] = band1_part_data
            band2_data[0:(height-y0),(0-x0):(width-x0)] = band2_part_data
            band3_data[0:(height-y0),(0-x0):(width-x0)] = band3_part_data

        else: #可能还包含一些没想到的特殊情况，遇到了再做进一步判断和处理
            band1_data = np.zeros((tile_size,tile_size))
            band2_data = np.zeros((tile_size,tile_size))
            band3_data = np.zeros((tile_size,tile_size))
        

        # band1_part_data =  ds.GetRasterBand(1).ReadAsArray()
        # band2_part_data =  ds.GetRasterBand(2).ReadAsArray()
        # band3_part_data =  ds.GetRasterBand(3).ReadAsArray()
        
        # band1_data = np.zeros((y1-y0,x1-x0))
        # band2_data = np.zeros((y1-y0,x1-x0))
        # band3_data = np.zeros((y1-y0,x1-x0))

        # band1_data[] = band1_part_data
        # band2_data[] = band2_part_data
        # band3_data[] = band3_part_data

            
        # band1_data = None 
        # band2_data = None
        # band3_data = None





del ds

rgb_data = np.dstack([band1_data,band2_data,band3_data])
print(type(rgb_data))
# convert a NumPy array to PIL image
img = Image.fromarray(np.uint8(rgb_data)).convert('RGB')
img.save("test.jpg","JPEG")
print(type(img))
img_new = img.resize((256,256))

img_new.save("test_resize.jpg","JPEG")

print(img.size)
print(img_new.size)