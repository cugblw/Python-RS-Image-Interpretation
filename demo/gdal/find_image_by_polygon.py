import os
from matplotlib.pyplot import get
from osgeo import gdal, ogr

def get_geometry_intersection(raster_path,vector_path):
    raster = gdal.Open(raster_path)

    # Get raster geometry
    transform = raster.GetGeoTransform()
    pixelWidth = transform[1]
    pixelHeight = transform[5]
    cols = raster.RasterXSize
    rows = raster.RasterYSize

    xLeft = transform[0]
    yTop = transform[3]
    xRight = xLeft+cols*pixelWidth
    yBottom = yTop+rows*pixelHeight

    ring = ogr.Geometry(ogr.wkbLinearRing)
    ring.AddPoint(xLeft, yTop)
    ring.AddPoint(xLeft, yBottom)
    ring.AddPoint(xRight, yBottom)
    ring.AddPoint(xRight, yTop)
    ring.AddPoint(xLeft, yTop)
    rasterGeometry = ogr.Geometry(ogr.wkbPolygon)
    rasterGeometry.AddGeometry(ring)

    rasterGeometry.FlattenTo2D()
#     return rasterGeometry

# def get_vector_geometry(vector_path):
    # get vector geometry
    vector = ogr.Open(vector_path)
    layer = vector.GetLayer()
    feature = layer.GetFeature(0)
    vectorGeometry = feature.GetGeometryRef()
    vectorGeometry.FlattenTo2D()
#     return vectorGeometry


# def geometry_intersection(raster_geometry, vector_geometry):
    intersection = rasterGeometry.Intersection(vectorGeometry)
    return intersection

def search_raster_by_polygon(raster_dir, vector_path):
    raster_list = []
    for root, dirs, files in os.walk(raster_dir):
        for file in files:
            if file.endswith('.tif'):
                raster_path = os.path.join(raster_dir, file)
                # raster_extent = get_raster_geometry(raster_path)
                # vector_extent = get_vector_geometry(vector_path)
                # print(type(raster_extent))
                # print(type(vector_extent))
                intersection = get_geometry_intersection(raster_path, vector_path)
                # print(intersection.GetArea())
                if intersection.GetArea() > 0:
                    raster_list.append(file)
    # del root, dirs, files
    return raster_list

if __name__ == '__main__':
    raster_dir = r'C:\Users\Administrator\Desktop\Image_Src\2m'
    vector_path = r'E:\Coding\Python\Python-RS-Image-Interpretation\res\vector\eastern.shp'
    raster_list = search_raster_by_polygon(raster_dir, vector_path)
    print(raster_list)