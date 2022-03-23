import glob
import os
import site
from osgeo import gdal

for item in site.getsitepackages():
    if "/lib/site-packages" in item.replace("\\", "/"):
        os.environ['PROJ_LIB'] = os.path.join(item, 'pyproj/proj_dir/share/proj')

in_directory = r'C:\Users\Administrator\Desktop\dem_tile'
files_to_process = glob.glob(os.path.join(in_directory, '*.tif'))
# file_list = []
for data_path in files_to_process:

    raster_dataset = gdal.Open(data_path, gdal.GA_ReadOnly)
    del raster_dataset
    #do your processing on the raster dataset here
# vrt_options = gdal.BuildVRTOptions(resampleAlg='cubic', addAlpha=True)
vrt_options = gdal.BuildVRTOptions(resampleAlg='cubic')
mosaicvrt = gdal.BuildVRT(r"C:\Users\Administrator\Desktop\dem_tile\merge.vrt",files_to_process,options=vrt_options)
# dataset = gdal.Open(mosaicvrt)
data = mosaicvrt.ReadAsArray()
gdal.Translate(r"C:\Users\Administrator\Desktop\dem_tile\merge.tif",mosaicvrt,format='gtiff' )



print(type(data))
print(data.shape)
del data

dataset = gdal.Open(r"C:\Users\Administrator\Desktop\dem_tile\ASTGTMV003_N40E116_dem_1_1.tif")
data = dataset.ReadAsArray()
print(data.shape)