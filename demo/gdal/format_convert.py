import os
import site
from osgeo_utils import gdal_calc as gc
from osgeo_utils import gdal_merge as gm
from osgeo import gdal

for item in site.getsitepackages():
    if "/lib/site-packages" in item.replace("\\", "/"):
        os.environ['PROJ_LIB'] = os.path.join(item, 'pyproj/proj_dir/share/proj')

def convert_dem_format(dem_dir):
    for root, dirs, files in os.walk(dem_dir):
        for file in files:
            band_list = []
            if file.endswith(".hgt"):
                file_path = os.path.join(root, file)
                new_file_path = dem_dir + "/" + file.split('.')[0] + ".tif"
                command = ['', '-A', file_path, '--A_band', '1', '--outfile', new_file_path, '--calc', '(A*(A<65535))']
                gdal.Translate(new_file_path, file_path, format='GTiff')

if __name__ == '__main__':
    img_dir = r"C:\Users\Administrator\Desktop\NASA SRTM1 v3.0 jilin\NASA SRTM1 v3.0 吉林"
    convert_dem_format(img_dir)