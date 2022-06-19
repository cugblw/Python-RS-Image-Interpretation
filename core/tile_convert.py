
from math import log, tan, radians, cos, pi, floor, degrees, atan, sinh,exp

TILE_SIZE = 256


def tile_x_to_longitude(tile_x, zoom):
    return pixel_x_to_longitude(int(tile_x) * TILE_SIZE, zoom)


def pixel_x_to_longitude(pixel_x, zoom):
    return 360 * ((float(pixel_x) / (TILE_SIZE << zoom)) - 0.5)


def pixel_y_to_latitude(pixel_y, zoom):
    y = 0.5 - float(pixel_y) / (TILE_SIZE << zoom)
    return 90 - 360 * atan(exp(-y * 2 * pi)) / pi


def tile_y_to_latitude(tile_y, zoom):
    return pixel_y_to_latitude(int(tile_y) * TILE_SIZE, zoom)


def sec(x):
    return(1/cos(x))


def latlon_to_xyz(lat, lon, z):
    tile_count = pow(2, z)
    x = (lon + 180) / 360
    y = (1 - log(tan(radians(lat)) + sec(radians(lat))) / pi) / 2
    return(tile_count*x, tile_count*y)


def bbox_to_xyz(lon_min, lon_max, lat_min, lat_max, z):
    x_min, y_max = latlon_to_xyz(lat_min, lon_min, z)
    x_max, y_min = latlon_to_xyz(lat_max, lon_max, z)
    return(floor(x_min), floor(x_max),
           floor(y_min), floor(y_max))


def mercatorToLat(mercatorY):
    return(degrees(atan(sinh(mercatorY))))


def y_to_lat_edges(y, z):
    tile_count = pow(2, z)
    unit = 1 / tile_count
    relative_y1 = y * unit
    relative_y2 = relative_y1 + unit
    lat1 = mercatorToLat(pi * (1 - 2 * relative_y1))
    lat2 = mercatorToLat(pi * (1 - 2 * relative_y2))
    return(lat1, lat2)


def x_to_lon_edges(x, z):
    tile_count = pow(2, z)
    unit = 360 / tile_count
    lon1 = -180 + x * unit
    lon2 = lon1 + unit
    return(lon1, lon2)


def tile_edges(x, y, z):
    lat1, lat2 = y_to_lat_edges(y, z)
    lon1, lon2 = x_to_lon_edges(x, z)
    return[lon1, lat1, lon2, lat2]

def tile2boundary(zoom, x, y):
    lon_min = tile_x_to_longitude(x, zoom)
    lat_max = tile_y_to_latitude(y, zoom)
    lon_max = tile_x_to_longitude(x + 1, zoom)
    lat_min = tile_y_to_latitude(y + 1, zoom)

    extent = [lon_min, lat_min, lon_max, lat_max]
    return extent