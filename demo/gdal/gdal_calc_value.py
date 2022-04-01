import os
import re
import site
from osgeo_utils import gdal_calc as gc
from osgeo_utils import gdal_merge as gm

for item in site.getsitepackages():
    if "/lib/site-packages" in item.replace("\\", "/"):
        os.environ['PROJ_LIB'] = os.path.join(item, 'pyproj/proj_dir/share/proj')

# 将(255,255,255)修改为(0,0,0)
def change_raster_value(img_dir):
    for root, dirs, files in os.walk(img_dir):
        for file in files:
            if file.endswith(".tif"):
                img_path = os.path.join(root, file)
                r_band_name = img_dir + "/" + file.split('.')[0] + "_R.tif"
                g_band_name = img_dir + "/" + file.split('.')[0] + "_G.tif"
                b_band_name = img_dir + "/" + file.split('.')[0] + "_B.tif"
                # print(r_band_name)
                # print(img_path)
                r_band_command = ['', '-A', img_path, '--A_band', '1', '--outfile', r_band_name, '--calc', '(A*(A<255))']
                g_band_command = ['', '-A', img_path, '--A_band', '2', '--outfile', g_band_name, '--calc', '(A*(A<255))']
                b_band_command = ['', '-A', img_path, '--A_band', '3', '--outfile', b_band_name, '--calc', '(A*(A<255))']

                result_name = img_dir + "/" + file.split('.')[0] + "_result.tif"
                merge_command = ['', '-o', result_name,'-separate', '-co', 'PHOTOMETRIC=RGB', '-co', 'COMPRESS=DEFLATE', r_band_name, g_band_name, b_band_name]

                gc.main(r_band_command)
                gc.main(g_band_command)
                gc.main(b_band_command)

                gm.main(merge_command)
                os.remove(r_band_name)
                os.remove(g_band_name)
                os.remove(b_band_name)
                os.remove(img_path)

                os.rename(result_name,img_path)


if __name__ == '__main__':
    img_dir = "C:/Users/Administrator/Desktop/test_cal"
    change_raster_value(img_dir)
