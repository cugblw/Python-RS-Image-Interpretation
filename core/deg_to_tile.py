from math import floor, log, tan, radians, cos, pi

""" def deg2tile(lat_deg, lon_deg, zoom):
  lat_rad = math.radians(lat_deg)
  n = 2.0 ** zoom
  xtile = int((lon_deg + 180.0) / 360.0 * n)
  ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
  return (xtile, ytile)

print(deg2tile(39,116,5))


def tile2deg(xtile, ytile, zoom):
  n = 2.0 ** zoom
  lon_deg = xtile / n * 360.0 - 180.0
  lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
  lat_deg = math.degrees(lat_rad)
  return (lat_deg, lon_deg)

print(tile2deg(26342,14222,5)) """

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



print(latlon_to_xyz(10,20,2))
print(bbox_to_xyz(115,118,36,41,12))
