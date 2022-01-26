from genericpath import exists
import os
import site
from osgeo import gdal
from osgeo_utils import gdal_edit as ge

from obtain_metadata import get_metadata

for item in site.getsitepackages():
    if "/lib/site-packages" in item.replace("\\", "/"):
        os.environ['PROJ_LIB'] = os.path.join(item, 'pyproj/proj_dir/share/proj')

def set_Color_Interpretation(image_path):
    metadata_dict = get_metadata(image_path)
    bands_info = metadata_dict['bands']

    if (len(bands_info) != 3):
        return
    colorInterpretation_List = []
    for band in bands_info:
        colorInterpretation = band['colorInterpretation']
        colorInterpretation_List.append(colorInterpretation)
    if "Gray" in colorInterpretation_List or "Undefined" in colorInterpretation_List:
        print("Set Color Interpretation to be right.")
        print(colorInterpretation_List)
        img = gdal.Open(image_path)
        for i in range(3):
            band = img.GetRasterBand(i + 1)
            band.SetColorInterpretation(i + 3)
            del band
        del img
    else:
        pass

def set_Nodata(image_path):
    metadata_dict = get_metadata(image_path)
    bands_info = metadata_dict['bands']

    if (len(bands_info) != 3):
        return
    for band in bands_info:
        if 'noDataValue' in band :
            noDataValue = band['noDataValue']
            print('Set Nodata to be right.')
            # nodataValue_List.append(nodataValue)
            if noDataValue != 0.0:
                # unset nodata
                command1 = ['', '-unsetnodata', image_path]
                ge.main(command1)
                # set white(255,255,255) to nodata and unset nodata
                command2 = ['', '-mo', "NODATA_VALUES=255 255 255", '-unsetnodata',image_path]
                ge.main(command2)
                break
            else:
                pass
        else:
            break


if __name__ == '__main__':
    input_tif = r"C:\Users\Administrator\Desktop\Image_Src\2m\DZGYYQ.tif"
    set_Color_Interpretation(input_tif)
    set_Nodata(input_tif)
