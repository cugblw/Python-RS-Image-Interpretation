import os
import sys
from osgeo import gdal

import osgeo_utils.gdal_merge as gm
import osgeo_utils.gdal_pansharpen as gp
import site


# 处理python3下proj错误
# GDAL version:3.3.1
# pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ pyproj

for item in site.getsitepackages():
    if "/lib/site-packages" in item.replace("\\", "/"):
        os.environ['PROJ_LIB'] = os.path.join(item, 'pyproj/proj_dir/share/proj')

r_band = "E:/Data/Raster/Landsat/Landsat8/BJ/LC81230322021250LGN00/LC08_L1TP_123032_20210907_20210907_01_RT_B4.TIF"
g_band = "E:/Data/Raster/Landsat/Landsat8/BJ/LC81230322021250LGN00/LC08_L1TP_123032_20210907_20210907_01_RT_B3.TIF"
b_band = "E:/Data/Raster/Landsat/Landsat8/BJ/LC81230322021250LGN00/LC08_L1TP_123032_20210907_20210907_01_RT_B2.TIF"
pan_band = "E:/Data/Raster/Landsat/Landsat8/BJ/LC81230322021250LGN00/LC08_L1TP_123032_20210907_20210907_01_RT_B8.TIF"

rgb_tif = "E:/Data/Raster/Landsat/Landsat8/BJ/LC81230322021250LGN00/LC08_L1TP_123032_20210907_20210907_01_RT_rgb.TIF"
fusion_tif = "E:/Data/Raster/Landsat/Landsat8/BJ/LC81230322021250LGN00/LC08_L1TP_123032_20210907_20210907_01_RT_fusion.TIF"

# RGB 波段合成
rgb_composite = ['', '-o', '%s'%(rgb_tif), '-separate', '-co', 'PHOTOMETRIC=RGB', '-co', 'COMPRESS=DEFLATE', '%s'%(r_band), '%s'%(g_band), '%s'%(b_band)]
gm.main(rgb_composite)

# 第二种方式，不推荐，无法压缩数据量
# rgb_command = "gdalbuildvrt -separate RGB.vrt " + r_band + " " + g_band + " " + b_band
# translate_command = "gdal_translate RGB.vrt " + new_tif
# os.system(rgb_command)
# os.system(translate_command)

# 多光谱与全色融合

# gdal_pansharpen.py RT_LC08_L1TP_137042_20190920_20190926_01_T1_2019-09-20_B8.TIF rgb.tif pansharpened.tif -r bilinear -co COMPRESS=DEFLATE -co PHOTOMETRIC=RGB
fusion_command = ['', '-r', 'bilinear', '-co', 'COMPRESS=DEFLATE', '-co', 'PHOTOMETRIC=RGB', '%s'%(pan_band), '%s'%(rgb_tif), '%s'%(fusion_tif)]
gp.main(fusion_command)