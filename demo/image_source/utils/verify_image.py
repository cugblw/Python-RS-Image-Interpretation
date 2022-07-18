# -*- encoding: utf-8 -*-

'''
@File    :   check_image.py
@Time    :   2022/07/18 16:18:22
@Author  :   Lee
@Version :   1.0
@License :   (C)Copyright Cennavi, Li Wei
@Desc    :   None
'''


from osgeo import gdal, osr


def check_image(img_path):
    """
    check if the image is valid
    :param img_path: image path
    :return: True or False
    """
    description = None
    if not img_path.endswith('tif'):
        description = "image file extension is not '.tif'."
        return False,description

    try:
        dataset = gdal.Open(img_path)
    except:
        description = "The source image can not be opened successfully."
        return  False,description

    try:
        proj_info = osr.SpatialReference(wkt=dataset.GetProjection())
        epsg = proj_info.GetAttrValue('AUTHORITY', 1)
        bands = dataset.RasterCount
    except:
        description = "The source image does not have CRS information."
        return False,description

    if epsg != "4326":
        description = "The source image EPSG is not 4326."
        return False,description

    if bands != 3:
        description = "The source image does not have the correct bands."
        return False,description

    del dataset, proj_info, epsg, bands
    return True,description