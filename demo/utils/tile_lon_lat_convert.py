from math import asinh, log, tan, radians, cos, pi, floor, degrees, atan, sinh

def sec(x):
    return(1/cos(x))

def lon_lat_to_xy(lon, lat, zoom):
    lat_rad = radians(lat)
    n = 2.0 ** zoom
    tile_x = int((lon + 180.0) / 360.0 * n)
    tile_y = int((1.0 - asinh(tan(lat_rad)) / pi) / 2.0 * n)
    return (tile_x, tile_y)

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

if __name__ == '__main__':
    print(tile_edges(48904, 28191, 16))
    print(bbox_to_xyz(88.6376953125, 88.6431884765625, 24.367113562651262, 24.3721173001113, 18))
    print(xyz_to_tile_list(195616, 195620, 112764, 112768, 18))