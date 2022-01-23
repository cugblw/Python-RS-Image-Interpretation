import glob
import shutil
import site
import subprocess
import urllib.request
import os
from osgeo import gdal
from tile_convert import bbox_to_xyz
from tile_convert import tile_edges
import osgeo_utils.gdal_merge as gm

for item in site.getsitepackages():
    if "/lib/site-packages" in item.replace("\\", "/"):
        os.environ['PROJ_LIB'] = os.path.join(item, 'pyproj/proj_dir/share/proj')

#---------- CONFIGURATION -----------#
tile_source  = "https://api.mapbox.com/v4/mapbox.satellite/{z}/{x}/{y}.png?access_token=" + "pk.eyJ1Ijoid2VpbC1sZWUiLCJhIjoiY2trbDVkNG9qMmRoazJ2bW5odndpMTE1MyJ9.eSayc9_uGQsOkLtIFVBWNA"
temp_dir = os.path.join(os.path.dirname(__file__), 'temp')
output_dir = os.path.join(os.path.dirname(__file__), 'output')
zoom = 16
lon_min = 21.49147
lon_max = 21.5
lat_min = 65.31016
lat_max = 65.31688
#-----------------------------------#


def fetch_tile(x, y, z, tile_source):
    url = tile_source.replace(
        "{x}", str(x)).replace(
        "{y}", str(y)).replace(
        "{z}", str(z))
    path = f'{temp_dir}/{x}_{y}_{z}.png'
    urllib.request.urlretrieve(url, path)
    return(path)

def merge_tiles(input_pattern, output_path):
    merge_command = ['', '-o', output_path]

    for name in glob.glob(input_pattern):
        merge_command.append(name)
        print(name)

    gm.main(merge_command)

def georeference_raster_tile(x, y, z, path):
    bounds = tile_edges(x, y, z)
    filename, extension = os.path.splitext(path)
    gdal.Translate(filename + '.tif',
                   path,
                   outputSRS='EPSG:4326',
                   outputBounds=bounds)

x_min, x_max, y_min, y_max = bbox_to_xyz(
    lon_min, lon_max, lat_min, lat_max, zoom)

print(f"Fetching {(x_max - x_min + 1) * (y_max - y_min + 1)} tiles")

for x in range(x_min, x_max + 1):
    for y in range(y_min, y_max + 1):
        try:
            png_path = fetch_tile(x, y, zoom, tile_source)
            print(f"{x},{y} fetched")
            georeference_raster_tile(x, y, zoom, png_path)
        except OSError:
            print(f"{x},{y} missing")
            pass

print("Fetching of tiles complete")

print("Merging tiles")
merge_tiles(temp_dir + '/*.tif', output_dir + '/merged.tif')
print("Merge complete")

shutil.rmtree(temp_dir)
os.makedirs(temp_dir)