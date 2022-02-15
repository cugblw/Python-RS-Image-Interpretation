import os
import site
from osgeo import gdal

for item in site.getsitepackages():
    if "/lib/site-packages" in item.replace("\\", "/"):
        os.environ['PROJ_LIB'] = os.path.join(item, 'pyproj/proj_dir/share/proj')

input_tif = "E:/Data/Raster/Landsat/Landsat8/BJ/LC81230322021250LGN00/LC08_L1TP_123032_20210907_20210907_01_RT_fusion.TIF"
temp_vrt = "E:/Data/Raster/Landsat/Landsat8/BJ/LC81230322021250LGN00/LC08_L1TP_123032_20210907_20210907_01_RT_vrt.vrt"
output_tif = "E:/Data/Raster/Landsat/Landsat8/BJ/LC81230322021250LGN00/LC08_L1TP_123032_20210907_20210907_01_RT_resample.TIF"

def resample_image(input_img, output_img, resolution):
    # Version 1: 数据量无法压缩
    # dataset = gdal.Open(input_img)
    # res_dataset = gdal.Warp(output_img, input_img, xRes=resolution, yRes=resolution, resampleAlg = "bilinear")

    # del dataset
    # del res_dataset
    
    
    # Version 2: 数据量可以压缩
    xres = resolution
    yres = resolution
    command = "gdalwarp -tr " + str(xres) + " " + str(yres) + " -r bilinear -of GTiff -co COMPRESS=DEFLATE " + input_img + " " + output_img
    
    os.remove(output_img)
    os.system(command)



if __name__ == '__main__':
    resample_image(input_tif, output_tif, 30)
