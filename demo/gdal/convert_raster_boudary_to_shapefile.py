from itertools import count
import os
from osgeo import gdal
from osgeo_utils import gdal_polygonize as gp
from osgeo import ogr

input_tif = r"C:\Users\Administrator\Desktop\Image_Src\2m\Lanzhou.tif"
output_tif = r"C:\Users\Administrator\Desktop\Image_Src\2m\Lanzhou1.tif"
input_mask = r"C:\Users\Administrator\Desktop\Image_Src\2m\Lanzhou.vrt"
output_edge = r"C:\Users\Administrator\Desktop\Image_Src\2m\Lanzhou_edge.shp"
output_boundary = r"C:\Users\Administrator\Desktop\Image_Src\2m\Lanzhou_boundary.shp"

""" # command = "gdaltindex  " + output_edge + " " + input_tif

# os.system(command)

# set no data
command1 = "gdalwarp -dstnodata 0 " + input_tif + " " + output_tif
os.system(command1)



command2 = "gdal_translate -b mask -of vrt -a_nodata 0 " + output_tif + " " + input_mask
os.system(command2)

# gdal_translate -scale 1 255 1 1 -ot Byte -of vrt -a_nodata 0 input_ortho.tif input_ortho_mask.vrt
command3 = ['', '-8', input_mask, '-f', "ESRI Shapefile", output_edge, 'mask_footprint', 'DN']
gp.main(command3)

shapefile = ogr.Open(output_edge,1)
layer = shapefile.GetLayerByIndex(0)
count = layer.GetFeatureCount()
for feature in layer:
    print(feature.GetField('DN'))
    if feature.GetField('DN') == 0:
        layer.DeleteFeature(feature.GetFID()) """

def convert_raster_edge_to_shapefile(raster_path, shapefile_path):
    output_tif = 'temp.tif'
    mask = 'temp.vrt'
    # set no data
    command_nodata = "gdalwarp -dstnodata 0 " + raster_path + " " + output_tif
    os.system(command_nodata)

    # convert to mvt
    command_vrt = "gdal_translate -b mask -of vrt -a_nodata 0 " + output_tif + " " + mask
    os.system(command_vrt)

    # polygonize
    command_polygonize = ['', '-8', mask, '-f', "ESRI Shapefile", shapefile_path, 'mask_footprint', 'DN']
    gp.main(command_polygonize)

    # delete unvalid shapefile feature
    shapefile = ogr.Open(shapefile_path,1)
    layer = shapefile.GetLayerByIndex(0)
    for feature in layer:
        if feature.GetField('DN') == 0:
            layer.DeleteFeature(feature.GetFID())

    # delete temp files
    os.remove(output_tif)
    os.remove(mask)

def convert_raster_boundary_to_shapefile(raster_path, shapefile_path):
    command = "gdaltindex  " + output_boundary + " " + raster_path
    os.system(command)


if __name__ == '__main__':
    convert_raster_edge_to_shapefile(input_tif, output_edge)
    convert_raster_boundary_to_shapefile(input_tif, output_boundary)