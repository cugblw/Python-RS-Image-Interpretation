import math
import urllib.request
import os

#---------- CONFIGURATION -----------#
tile_server = "https://api.mapbox.com/v4/mapbox.satellite/{z}/{x}/{y}.png?access_token=" + "pk.eyJ1Ijoid2VpbC1sZWUiLCJhIjoiY2trbDVkNG9qMmRoazJ2bW5odndpMTE1MyJ9.eSayc9_uGQsOkLtIFVBWNA"
temp_dir = os.path.join(os.path.dirname(__file__), 'temp')
output_dir = os.path.join(os.path.dirname(__file__), 'output')
zoom = 16
lon_min = 21.49147
lon_max = 21.5
lat_min = 65.31016
lat_max = 65.31688
#-----------------------------------#


def download_tile(x, y, z, tile_server):
    url = tile_server.replace(
        "{x}", str(x)).replace(
        "{y}", str(y)).replace(
        "{z}", str(z))
    path = f'{temp_dir}/{x}_{y}_{z}.png'
    urllib.request.urlretrieve(url, path)
    return(path)

download_tile(0, 0, 0, tile_server)