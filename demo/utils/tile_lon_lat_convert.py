import math
from math import asinh, log, tan, radians, cos, pi, floor, degrees, atan, sinh

TILE_SIZE = 256

def sec(x):
    return(1/cos(x))

def lon_to_pixel_x(lon, zoom):
    pixel_x = (lon + 180.0) / 360.0 * (TILE_SIZE << zoom)
    return pixel_x

def lat_to_pixel_y(lat, zoom):
    sin_lat = math.sin(lat * math.pi / 180)
    return (0.5 - math.log((1.0 + sin_lat) / (1.0 - sin_lat)) / (4 * math.pi)) * (TILE_SIZE << zoom)

def lon_to_tile_x(lon, zoom):
    pixel_x = lon_to_pixel_x(lon, zoom)
    return pixel_x_to_tile_x(pixel_x, zoom)

def lat_to_tile_y(lat, zoom):
    pixel_y = lat_to_pixel_y(lat, zoom)
    return pixel_y_to_tile_y(pixel_y, zoom)

def pixel_x_to_tile_x(pixel_x, zoom):
    mx = max(float(pixel_x) / TILE_SIZE, 0.0)
    mp = math.pow(2.0, float(zoom)) - 1.0
    return int(min(mx, mp))


def pixel_y_to_tile_y(pixel_y, zoom):
    mx = max(float(pixel_y) / TILE_SIZE, 0.0)
    mp = math.pow(2.0, float(zoom)) - 1.0
    return int(min(mx, mp))

def lon_lat_to_tilexyz(lon, lat, zoom):
    tile_x = lon_to_tile_x(lon, zoom)
    tile_y = lat_to_tile_y(lat, zoom)
    return [tile_x, tile_y, zoom]

def tile_to_lon_lat(x, y, zoom):
    n = 2.0 ** zoom
    lon = x / n * 360.0 - 180.0
    lat = atan(sinh(pi * (1 - 2 * y / n)))
    lat = degrees(lat)
    return (lon, lat)
    
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

def latlon_to_xyz(lat, lon, z):
    tile_count = pow(2, z)
    x = (lon + 180) / 360
    y = (1 - log(tan(radians(lat)) + sec(radians(lat))) / pi) / 2
    return(tile_count*x, tile_count*y)

def tile_edges(x, y, z):
    lat1, lat2 = y_to_lat_edges(y, z)
    lon1, lon2 = x_to_lon_edges(x, z)
    return[lon1, lat1, lon2, lat2]

# 此方法似乎还有些问题，需要进一步验证
def bbox_to_xyz(lon_min, lon_max, lat_min, lat_max, z):
    x_min, y_max = latlon_to_xyz(lat_min, lon_min, z)
    x_max, y_min = latlon_to_xyz(lat_max, lon_max, z)
    return(floor(x_min), floor(x_max),
           floor(y_min), floor(y_max))

def xyz_to_tile_list(x_min, x_max, y_min, y_max,z):
    tile_list = []
    for x in range(x_min, x_max):
        for y in range(y_min, y_max):
            tile_number = str(z) + "_" + str(x) + "_" + str(y)
            tile_list.append(tile_number)
    return tile_list

def boundary_to_xyz(lon_min, lon_max, lat_min, lat_max, z):
    x_min, y_min, z = lon_lat_to_tilexyz(lon_min, lat_max, z)
    x_max, y_max, z = lon_lat_to_tilexyz(lon_max, lat_min, z)
    return(x_min, x_max, y_min, y_max)

def low_room_tile_to_high_room_tile(tile_x,tile_y,z_low,z_high):
    boundary = tile_edges(tile_x, tile_y, z_low)
    x_min,x_max,y_min,y_max = boundary_to_xyz(boundary[0], boundary[2], boundary[3], boundary[1], z_high)
    return (x_min, x_max, y_min, y_max, z_high)

def high_room_tile_to_low_room_tile(tile_x,tile_y,z_low,z_high):
    boundary = tile_edges(tile_x, tile_y, z_high)
    x_min,x_max,y_min,y_max = boundary_to_xyz(boundary[0], boundary[2], boundary[3], boundary[1], z_low)
    return (x_min, x_max, y_min, y_max, z_low)
    

if __name__ == '__main__':

    # print(tile_edges(48904, 28191, 16))
    # print(bbox_to_xyz(88.6376953125, 88.6431884765625, 24.367113562651262, 24.3721173001113, 18))
    # print(xyz_to_tile_list(195616, 195620, 112764, 112768, 18))
    # print(lon_lat_to_tilexyz(-180, 85, 1))
    # print(bbox_to_xyz(-180.0, 180.0, -85.0511287798066, 20))

    print(boundary_to_xyz(-180, 180, -85.05112878, 85.05112878, 4))
    print(tile_edges(6, 1, 3))
    print(low_room_tile_to_high_room_tile(0,0,0,10))
    print(high_room_tile_to_low_room_tile(7,5,1,3))
