import glob
from operator import contains
import os
import site
from osgeo import gdal

for item in site.getsitepackages():
    if "/lib/site-packages" in item.replace("\\", "/"):
        os.environ['PROJ_LIB'] = os.path.join(item, 'pyproj/proj_dir/share/proj')

in_directory = r'C:\Users\Administrator\Desktop\dem_tile'
# files_to_process = glob.glob(os.path.join(in_directory, '*.tif'))
files_to_process = []
for root,dirs,files in os.walk(in_directory):
    for file in files:
        print(type(os.path.join(root,file)))
        if "merge" in os.path.join(root,file):
            del file
        else:
            files_to_process.append(os.path.join(root,file))
# vrt_options = gdal.BuildVRTOptions(resampleAlg='cubic', addAlpha=True)
vrt_options = gdal.BuildVRTOptions(resampleAlg='cubic')
mosaicvrt = gdal.BuildVRT(r"C:\Users\Administrator\Desktop\dem_tile\merge.vrt",files_to_process,options=vrt_options)
# dataset = gdal.Open(mosaicvrt)
data = mosaicvrt.ReadAsArray()
del files_to_process
if os.path.exists(r"C:\Users\Administrator\Desktop\dem_tile\merge.tif"):
    os.remove(r"C:\Users\Administrator\Desktop\dem_tile\merge.tif")

    
gdal.Translate(r"C:\Users\Administrator\Desktop\dem_tile\merge.tif",mosaicvrt,format='gtiff' )

print(type(data))
print(data.shape)
del data

tif_path = r"C:\Users\Administrator\Desktop\Image\beijing_clip_4326.tif"
vrt_options = gdal.BuildVRTOptions(resampleAlg='cubic')
temp_vrt = gdal.BuildVRT("temp.vrt",tif_path,options=vrt_options)

dataset = temp_vrt.GetRasterBand(1).ReadAsArray()
print(type(dataset))
print(dataset.shape)

del dataset