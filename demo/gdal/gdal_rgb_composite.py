import os
import sys
import osgeo_utils.gdal_merge as gm
import site

from osgeo import gdal

# 处理python3下proj错误
# GDAL version:3.3.1
# pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ pyproj

for item in site.getsitepackages():
    if "/lib/site-packages" in item.replace("\\", "/"):
        os.environ['PROJ_LIB'] = os.path.join(item, 'pyproj/proj_dir/share/proj')
        # print(os.path.join(item,'pyproj/proj_dir/share/proj'))

r_band = "E:/Data/Raster/Landsat/Landsat8/BJ/LC81230322021250LGN00/LC08_L1TP_123032_20210907_20210907_01_RT_B4.TIF"
g_band = "E:/Data/Raster/Landsat/Landsat8/BJ/LC81230322021250LGN00/LC08_L1TP_123032_20210907_20210907_01_RT_B3.TIF"
b_band = "E:/Data/Raster/Landsat/Landsat8/BJ/LC81230322021250LGN00/LC08_L1TP_123032_20210907_20210907_01_RT_B2.TIF"

new_tif = "E:/Data/Raster/Landsat/Landsat8/BJ/LC81230322021250LGN00/LC08_L1TP_123032_20210907_20210907_01_RT_RGB.TIF"


# rgb_command = ['', '-separate', '-o', '%s'%(new_tif), '-co', 'PHOTOMETRIC=RGB', '%s'%(r_band), '%s'%(g_band), '%s'%(b_band)]
rgb_command = ['', '-o', '%s'%(new_tif), '-separate', '-co', 'PHOTOMETRIC=RGB', '-co', 'COMPRESS=DEFLATE', '%s'%(r_band), '%s'%(g_band), '%s'%(b_band)]
# -o rgb.tif -separate -co PHOTOMETRIC=RGB -co COMPRESS=DEFLATE
gm.main(rgb_command)

# rgb_command = "gdalbuildvrt -separate RGB.vrt " + r_band + " " + g_band + " " + b_band
# translate_command = "gdal_translate RGB.vrt " + new_tif

# os.system(rgb_command)
# os.system(translate_command)