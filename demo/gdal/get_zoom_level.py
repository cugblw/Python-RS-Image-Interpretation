import math
from osgeo import gdal
from get_image_info import get_metadata

# 获取最优显示zoom，影像的坐标系是WGS84，如果是投影坐标系，需要转换
def get_optimal_zoom_level(geotiff_path,tile_size):
    dataset = gdal.Open(geotiff_path)
    geo_transform = dataset.GetGeoTransform()
    degrees_per_pixel = geo_transform[1]
    radius = 6378137
    equator = 2 * math.pi * radius
    meters_per_degree = equator / 360
    resolution = degrees_per_pixel * meters_per_degree
    pixels_per_tile = tile_size
    zoom_level = math.log((equator/pixels_per_tile)/resolution, 2)
    MAX_ZOOM_LEVEL = 21
    optimal_zoom_level = min(math.floor(zoom_level), MAX_ZOOM_LEVEL)
    return optimal_zoom_level

# 获取适合屏幕的显示级别
def get_display_zoom_level(geotiff_path,tile_size):
    dataset = gdal.Open(geotiff_path)
    geo_transform = dataset.GetGeoTransform()
    size = get_metadata(geotiff_path)['size']
    degrees_per_pixel = geo_transform[1]
    radius = 6378137
    equator = 2 * math.pi * radius
    meters_per_degree = equator / 360
    resolution = degrees_per_pixel * meters_per_degree
    tile_size = tile_size
    optimal_zoom_level = math.floor(math.log((equator/tile_size)/resolution, 2))

    tile_number =  size[1]/tile_size

    power_reduce = math.floor(math.log(tile_number,math.floor(1080/tile_size))) # 这里的2是屏幕高度（1080）显示两个瓦片（512）,更加瓦片size调整

    display_zoom_level = optimal_zoom_level - power_reduce
    return display_zoom_level


if __name__ == "__main__":
    # center_coordinate = get_multi_geotiff_center_coordinate(r"C:\Users\Administrator\Desktop\Image_Src\2m")
    # extent_boundary = get_multi_geotiff_extent(r"C:\Users\Administrator\Desktop\Image_Src\2m")
    # print(center_coordinate)
    # print(extent_boundary)
    optimal_zoom_level = get_optimal_zoom_level(r"C:\Users\Administrator\Desktop\Image\hechi_2m7_4.tif",256)
    print(optimal_zoom_level)
    display_zoom_level = get_display_zoom_level(r"C:\Users\Administrator\Desktop\Image\hechi_2m7_4.tif",256)
    print(display_zoom_level)