import os

from osgeo import osr
from osgeo import gdal


# Get metadata of an image file.
def get_metadata(img_path):
    command = "gdalinfo -json " + img_path
    metadata = os.popen(command).read()
    # print(metadata)
    metadata_dict = eval(metadata)
    return metadata_dict

def get_image_size(img_path):
    metadata_dict = get_metadata(img_path)
    size = metadata_dict['size']
    return size

def get_geotiff_epsg(img_path):
    dataset = gdal.Open(img_path)
    img_proj_info = osr.SpatialReference(dataset.GetProjection())
    epsg = img_proj_info.GetAttrValue('AUTHORITY', 1)
    return epsg

if __name__ == "__main__":
    pass