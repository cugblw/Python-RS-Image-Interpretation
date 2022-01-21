import os
from unicodedata import name
from osgeo import gdal


# Get metadata of an image file.
def __get_metadata(img_path):
    command = "gdalinfo -json " + img_path
    metadata = os.popen(command).read()
    # print(metadata)
    metadata_dict = eval(metadata)
    return metadata_dict


# Convert image to 8 bit
def convert_image_to_8bit(img_path):
    metadata = __get_metadata(img_path)
    band_type = metadata['bands'][0]['type']
    image_src = os.path.dirname(img_path)
    filename = os.path.basename(img_path)
    filename_new = filename.split(".")[0] + "_8bit" + ".tif"
    command = "gdal_translate -ot Byte -of GTiff " + img_path + " " + os.path.join(image_src,filename_new)
    
    if band_type == "Byte":
        pass
    else:
        print("Band Type: " + band_type + ". " + "Convert image to 8 bit.")
        os.system(command)
        os.remove(img_path)
        os.rename(os.path.join(image_src,filename_new),os.path.join(image_src,filename))

if __name__ == "__main__":
    img_path = r"C:\Users\Administrator\Desktop\Image_Src\2m\LC08_L2SP_231062_20201026_20201106_02_T1_ST_B10.TIF"
    convert_image_to_8bit(img_path)