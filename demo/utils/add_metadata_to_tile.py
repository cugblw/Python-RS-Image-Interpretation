# -*- encoding: utf-8 -*-

'''
@File    :   add_metadata_to_tile.py
@Time    :   2022/07/05 13:41:02
@Author  :   Lee
@Version :   1.0
@License :   (C)Copyright Cennavi, Li Wei
@Desc    :   Add metadata to tile in the tar file
'''


import os
import io
import tarfile
import time

import piexif
from PIL import Image
from PIL.PngImagePlugin import PngInfo


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

def add_metadata_to_tar(tar_path, new_tar_path, resolution):
    for root, dirs, files in os.walk(tar_path):
        for file in files:
            if file.endswith(".tar"):
                print("add metadata to: %s. "%(file))
                tar_file = tarfile.open(os.path.join(root, file))
                members = tar_file.getmembers()
                with tarfile.open(os.path.join(new_tar_path, file.split(".")[0]+".tar"), 'w') as tar:
                    for member in members:
                        image = tar_file.extractfile(member)
                        image = image.read()
                        img = Image.open(io.BytesIO(image))
                        # img_new = generate_watermark_by_image(img)

                        img_byte = io.BytesIO()
                        if img.mode == "RGB":
                            img_exif_bytes = insert_jpg_info(resolution)
                            img.save(img_byte, "JPEG", exif=img_exif_bytes)
                        else:
                            img_info = insert_png_info(resolution)
                            img.save(img_byte, "PNG", pnginfo=img_info)

                        data = img_byte.getvalue()
                        tarinfo = tarfile.TarInfo(name=member.name)
                        tarinfo.size = len(data)
                        tar.addfile(tarinfo=tarinfo, fileobj=io.BytesIO(data))
                tar.close()
    del root, dirs, files



if __name__ == '__main__':
    # 原始tar包存储路径
    tar_path = r'C:\Users\Administrator\Desktop\Image_Out'
    # 新的tar包存储路径
    new_tar_path = r'C:\Users\Administrator\Desktop\new'
    # 指定添加的分辨率信息
    resolution = '2m'

    start_time = time.time()
    add_metadata_to_tar(tar_path,new_tar_path,resolution)
    end_time = time.time()
    print("Time used: %s"% str(round((end_time - start_time),3)) + "s")