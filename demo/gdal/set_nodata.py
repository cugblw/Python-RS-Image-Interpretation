from distutils import command
import os
from osgeo import gdal
from osgeo_utils import gdal_edit as ge

input_tif = r"C:\Users\Administrator\Desktop\Image_Src\2m\DZGYYQ.tif"
output_vrt = r"C:\Users\Administrator\Desktop\Image_Src\2m\DZGYYQ.vrt"
output_tif = r"C:\Users\Administrator\Desktop\Image_Src\2m\DZGYYQ_res.tif"

command = "gdal_translate -of GTiff -a_nodata ${na} " + input_tif + " " + output_tif
command1 = "gdalbuildvrt -of GTIFF -srcnodata 0 " + input_tif + output_vrt
command2 = "gdal_translate -of GTIFF -scale -a_nodata 0 " + output_vrt + output_tif
command4 = ['', '-unsetnodata', input_tif]

# os.system(command)
# os.system(command1)
# os.system(command2)
ge.main(command4)