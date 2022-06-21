import os
from osgeo import gdal

def get_geotiff_by_boundary(dataset, zoom,x,y):
    
    ds = gdal.Translate('', dataset, projWin=bbox, format='MEM')
    return ds
