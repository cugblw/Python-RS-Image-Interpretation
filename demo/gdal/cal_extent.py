import os
import site
import shapefile
from osgeo import gdal,ogr
from shapely.geometry import shape

for item in site.getsitepackages():
    if "/lib/site-packages" in item.replace("\\", "/"):
        os.environ['PROJ_LIB'] = os.path.join(item, 'pyproj/proj_dir/share/proj')


def get_raster_extent(raster_path):
    ds = gdal.Open(raster_path)
    width = ds.RasterXSize
    height = ds.RasterYSize
    gt = ds.GetGeoTransform()
    lon_min = gt[0]
    lat_min = gt[3] + width*gt[4] + height*gt[5] 
    lon_max = gt[0] + width*gt[1] + height*gt[2]
    lat_max = gt[3]
    del ds
    return [lon_min, lon_max, lat_min, lat_max]

def get_vector_extent(vector_path):
    shapefile = ogr.Open(vector_path)
    layer = shapefile.GetLayer()
    extent = layer.GetExtent()
    lon_min = extent[0]
    lon_max = extent[1]
    lat_min = extent[2]
    lat_max = extent[3]
    del shapefile
    return [lon_min, lon_max, lat_min, lat_max]


if __name__ == '__main__':
    print(get_raster_extent("core/output/merged.tif"))
    print(get_vector_extent(r"E:\Data\Vector\新型冠状病毒肺炎疫情地图\各省通报数据.shp"))
    # print(get_vector_extent2(r"E:\Data\Vector\新型冠状病毒肺炎疫情地图\各省通报数据.shp"))