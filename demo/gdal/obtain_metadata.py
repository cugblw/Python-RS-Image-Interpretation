import os
from unicodedata import name
from osgeo import gdal


# Get metadata of an image file.
def get_metadata(img_path):
    command = "gdalinfo -json " + img_path
    metadata = os.popen(command).read()
    # print(metadata)
    metadata_dict = eval(metadata)
    return metadata_dict

if __name__ == "__main__":
    pass