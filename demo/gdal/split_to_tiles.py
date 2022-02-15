import os
import site
from osgeo import gdal
from osgeo_utils import gdal_retile as gr

for item in site.getsitepackages():
    if "/lib/site-packages" in item.replace("\\", "/"):
        os.environ['PROJ_LIB'] = os.path.join(item, 'pyproj/proj_dir/share/proj')


img = "E:/Data/Raster/Landsat/Landsat8/BJ/LC81230322021250LGN00/LC08_L1TP_123032_20210907_20210907_01_RT_resample.TIF"
dset = gdal.Open(img)

width = dset.RasterXSize
height = dset.RasterYSize

print (width, 'x', height)

tilesize = 2000

# for i in range(0, width, tilesize):
#     for j in range(0, height, tilesize):
#         w = min(i+tilesize, width) - i
#         h = min(j+tilesize, height) - j
#         gdaltranString = "gdal_translate -of GTIFF -srcwin "+str(i)+", "+str(j)+", "+str(w)+", " \
#             +str(h)+" " + img + " " + "C:/Users/wsm/Desktop/dir/" + "_"+str(i)+"_"+str(j)+".tif"
#         os.system(gdaltranString)

# gdal_retile.py -ps 512 512 -targetDir C:\example\dir some_dem.tif
# cmd = 'gdal_retile.py -v -r bilinear -levels 4 -ps 2048 2048 -co "tiled=YES" -targetDir C:/Users/wsm/Desktop/dir/ --optfile files.txt'
# os.system(cmd)

command = ['-v', '-r', 'bilinear','-levels', str(6), '-ps', str(512), str(512), '-co' ,'tiled=YES','-targetDir','C:/Users/wsm/Desktop/dir/',img]
gr.main(command)