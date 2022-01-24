import math
from math import floor, log, tan, radians, cos, pi
import os
import urllib.request
import multiprocessing as mp
import time

#---------- CONFIGURATION -----------#
tile_server = "https://api.mapbox.com/v4/mapbox.satellite/{z}/{x}/{y}.png?access_token=" + "pk.eyJ1Ijoid2VpbC1sZWUiLCJhIjoiY2trbDVkNG9qMmRoazJ2bW5odndpMTE1MyJ9.eSayc9_uGQsOkLtIFVBWNA"
temp_dir = os.path.join(os.path.dirname(__file__), 'temp')
output_dir = os.path.join(os.path.dirname(__file__), 'output')
zoom = 11
# lon_min = 21.49147
lon_min = 21
lon_max = 21.5
# lat_min = 65.31016
lat_min = 65
lat_max = 65.31688
# pool = mp.Pool(mp.cpu_count())
#-----------------------------------#


start_time = time.time()

def sec(x):
  return(1/cos(x))

def latlon_to_xyz(lat, lon, z):
  tile_count = pow(2, z)
  x = (lon + 180) /360
  y = (1 - log(tan(radians(lat)) + sec(radians(lat))) / pi) / 2
  return(tile_count * x, tile_count * y)

def bbox_to_xyz(lon_min, lon_max, lat_min, lat_max, z):
  x_min, y_max = latlon_to_xyz(lat_min, lon_min, z)
  x_max, y_min = latlon_to_xyz(lat_max, lon_max, z)
  return(floor(x_min), floor(x_max),
         floor(y_min), floor(y_max))


def download_tile(x, y, z, tile_server):
    url = tile_server.replace(
        "{x}", str(x)).replace(
        "{y}", str(y)).replace(
        "{z}", str(z))
    path = f'{temp_dir}/{x}_{y}_{z}.png'
    urllib.request.urlretrieve(url, path)
    return(path)


x_min, x_max, y_min, y_max = bbox_to_xyz(
    lon_min, lon_max, lat_min, lat_max, zoom)

print(f"Downloading {(x_max - x_min + 1) * (y_max - y_min + 1)} tiles")

for x in range(x_min, x_max + 1):
    for y in range(y_min, y_max + 1):
        print(f"{x},{y}")
        download_tile(x, y, zoom, tile_server)

print("Download complete!")

end_time = time.time()
print("Time used: " + str((end_time - start_time) / 60) + "min")


# print(latlon_to_xyz(10,20,2))
# print(bbox_to_xyz(115,118,36,41,12))
