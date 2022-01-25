import os
import site
from osgeo import gdal
from osgeo_utils import gdal_edit as ge

for item in site.getsitepackages():
    if "/lib/site-packages" in item.replace("\\", "/"):
        os.environ['PROJ_LIB'] = os.path.join(item, 'pyproj/proj_dir/share/proj')

input_tif = r"C:\Users\Administrator\Desktop\Image_Src\2m\DZGYYQ.tif"
img = gdal.Open(input_tif)

for i in range(3):
    band = img.GetRasterBand(i + 1)
    band.SetColorInterpretation(i + 3)
    del band
del img

# unset nodata
command1 = ['', '-unsetnodata', input_tif]
ge.main(command1)

# set white(255,255,255) to nodata and unset nodata
command2 = ['', '-mo', "NODATA_VALUES=255 255 255", '-unsetnodata',input_tif]
ge.main(command2)