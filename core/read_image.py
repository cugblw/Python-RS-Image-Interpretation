import os
import site

from osgeo import gdal

for item in site.getsitepackages():
    if "/lib/site-packages" in item.replace("\\", "/"):
        os.environ['PROJ_LIB'] = os.path.join(item, 'pyproj/proj_dir/share/proj')

def read_geotiff(geotiff_path):
    """读取geotiff文件"""
    src_ds = gdal.Open(geotiff_path)
    return src_ds

def get_geotiff_bands(dataset):
    """获取geotiff的波段"""
    rasterCount =  dataset.RasterCount
    bands = []
    for i in range(rasterCount):
        band = dataset.GetRasterBand(i+1)
        bands.append(band)
    return bands
    
def get_geotiff_extent(geotiff_path):
    dataset = read_geotiff(geotiff_path)
    lon_min, xpixel, _, lat_max, _, ypixel = dataset.GetGeoTransform()
    width, height = dataset.RasterXSize, dataset.RasterYSize
    lon_max = lon_min + width * xpixel
    lat_min = lat_max + height * ypixel
    extent = [lon_min,lat_min,lon_max,lat_max]
    del dataset
    return extent

def read_part_of_geotiff():
    """获取geotiff的一部分"""
    # gdal.AllRegister()
    pass