from distutils import command
import os
from osgeo import gdal
from osgeo_utils import gdal_polygonize as gp
from setuptools import Command

input_tif = r"C:\Users\Administrator\Desktop\Image_Src\2m\DZGYYQ.tif"
output_tif = r"C:\Users\Administrator\Desktop\Image_Src\2m\DZGYYQ1.tif"
input_mask = r"C:\Users\Administrator\Desktop\Image_Src\2m\DZGYYQ.vrt"
output_shp = r"C:\Users\Administrator\Desktop\Image_Src\2m\DZGYYQ.shp"

# command = "gdaltindex  " + output_shp + " " + input_tif

# os.system(command)

# set no data
command1 = "gdalwarp -dstnodata 0 " + input_tif + " " + output_tif
os.system(command1)



command2 = "gdal_translate -b mask -of vrt -a_nodata 0 " + input_tif + " " + input_mask
os.system(command2)

# gdal_translate -scale 1 255 1 1 -ot Byte -of vrt -a_nodata 0 input_ortho.tif input_ortho_mask.vrt
command3 = ['', '-8', input_mask, '-f', "ESRI Shapefile", output_shp, 'mask_footprint', 'DN']
gp.main(command3)