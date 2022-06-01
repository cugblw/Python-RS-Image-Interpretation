# -*- encoding: utf-8 -*-

'''
@File    :   image_metadata.py
@Time    :   2022/05/26 11:22:58
@Author  :   Lee
@Version :   1.0
@License :   (C)Copyright Cennavi, Li Wei
@Desc    :   瓦片增加头信息
'''


from io import BytesIO

import piexif
from PIL import Image
from PIL.PngImagePlugin import PngInfo


def add_png_metadata(img, resolution):
    metadata = PngInfo()
    metadata.add_text("resolution", resolution)
    io = BytesIO()
    img.save(io, "PNG", pnginfo=metadata)
    img_new = Image.open(io)
    return img_new

def get_png_metadata(img):
    if img.text is None:
        return None
    resolution = img.text['resolution']
    return resolution

def insert_jpg_info(resolution):
    zeroth_ifd = {
                piexif.ImageIFD.Make: u"{}".format(resolution),
                piexif.ImageIFD.XResolution: (96, 1),
                piexif.ImageIFD.YResolution: (96, 1),
                piexif.ImageIFD.Software: u"Cennavi"
                }
    exif_dict = {"0th":zeroth_ifd}
    exif_bytes = piexif.dump(exif_dict)
    return exif_bytes

def insert_png_info(resolution):
    metadata = PngInfo()
    metadata.add_text("resolution", resolution)
    # io = BytesIO()
    # img.save(io, "PNG", pnginfo=metadata)
    # img_new = Image.open(io)
    return metadata

def get_jpg_info(img):
    exif_dict = piexif.load(img.info['exif'])
    resolution = exif_dict['0th'][271].decode('utf-8')
    return resolution

def insert_img_info(img, resolution):
    if img.mode == "RGB":
        return insert_jpg_info(resolution)
    else:
        return insert_png_info(resolution)

def get_img_info(img):
    if img.mode == "RGB":
        return get_jpg_info(img)
    else:
        return get_png_metadata(img)

if __name__ == "__main__":
    resolution = "0.5m"
    # img_path = r"C:\Users\Administrator\Desktop\Image_Out\satellite\14\R12\C25\14_12908_6426.jpg"
    img_path = r"C:\Users\Administrator\Desktop\tar_list\2m\satellite\15\R12\C25\15_25818_12855.jpg"
    # img_path = r"C:\Users\Administrator\Desktop\tar_list\0.5m\satellite\15\R12\C25\15_25819_12856.jpg"

    img = Image.open(img_path)
    print("Satellite Image Resolution:", get_img_info(img))
