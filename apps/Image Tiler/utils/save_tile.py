import os
import io
import sys
import string
import time
import tarfile

import PIL
from PIL import Image

from core.image_util import convert_image_transparency

def save_tile(tile_dir: string, zoom: int, x:int ,y:int ,img: PIL.Image):
    """保存瓦片"""
    tile_name = str(zoom) + "_" + str(x) + "_" + str(y) + ".png"
    tile_path = os.path.join(tile_dir, str(zoom), tile_name)
    try:
        img.save(tile_path)
    except:
        pass

def save_tile_to_tar(tile_dir: string, zoom: int, x:int ,y:int ,img: PIL.Image, tar_path: string):
    """保存瓦片"""
    if img is None:
        pass
    tile_name = str(zoom) + "_" + str(x) + "_" + str(y) + ".png"
    tile_path = os.path.join(tile_dir, str(zoom), tile_name)
    try:
        img.save(tile_path)
        tar_file = tarfile.open(tar_path, "a")
        tar_file.add(tile_path)
        tar_file.close()
    except:
        pass

def __image_composite(source_dict, z, x, y, extension, img_format):
    IMAGE_SIZE = 256  # 每张小图片的大小
    IMAGE_ROW = 2  # 图片间隔，也就是合并成一张图后，一共有几行
    IMAGE_COLUMN = 2  # 图片间隔，也就是合并成一张图后，一共有几列

    to_image = Image.new('RGBA', (IMAGE_COLUMN * IMAGE_SIZE, IMAGE_ROW * IMAGE_SIZE))  # 创建一个新图

    for y_delta in [0, 1]:
        for x_delta in [0, 1]:
            x_split = x * 2 + x_delta
            y_split = y * 2 + y_delta
            key = str(z + 1) + "_" + str(x_split) + "_" + str(y_split)
            if key not in source_dict:
                continue
            from_image = Image.open(io.BytesIO(source_dict[key])).resize((IMAGE_SIZE, IMAGE_SIZE), Image.Resampling.LANCZOS)
            if extension == "jpg":
                from_image.convert("RGBA")
            to_image.paste(from_image, (x_delta * IMAGE_SIZE, y_delta * IMAGE_SIZE))

    data_combined = io.BytesIO()
    to_image = to_image.resize((IMAGE_SIZE, IMAGE_SIZE), Image.Resampling.LANCZOS)
    img_out = convert_image_transparency(to_image)

    if img_out is None:
        # return
        img_out = Image.new("RGBA", (IMAGE_SIZE,IMAGE_SIZE),(255, 255, 255, 0))
    if img_out == "part-blank":
        extension = "PNG"
    else:
        to_image = img_out

    if extension == "jpg":
        to_image.convert("RGB").save(data_combined, format='JPEG')
    else:
        to_image.save(data_combined, format='PNG')
    # print(z, x, y,extension)
    # if extension == "PNG":
    #     to_image.close()
    #     save_util.delete_tmp_image(z,x,y)

    data = data_combined.getvalue()
    return data

def generate_low_zoom_tar(tar_dir, tar_new_dir, max_zoom, min_zoom, img_format):
    extension = None
    image_dict = {}
    for file_name in os.listdir(tar_dir):
        if not file_name.endswith(".tar"):
            continue
        tar = tarfile.open(os.path.join(tar_dir, file_name), "r")

        for name in tar.getnames():
            member = tar.getmember(name)
            f = tar.extractfile(member)
            data = f.read()
            if (sys.platform == "win32"):
                pic_name = name.replace("/","\\").split(os.path.sep)[-1]
            else:
                pic_name = name.rsplit(os.path.sep)[-1]
            if pic_name.split("_")[0] != str(max_zoom):
                continue
            image_dict[pic_name.split(".")[0]] = data
            if extension is None:
                extension = pic_name.split(".")[-1].lower()

    tmp_dict = {}
    for zoom in range(max_zoom - 1, min_zoom - 1, -1):
        start_time = time.time()
        tar_file_new = os.path.join(tar_new_dir, str(zoom) + ".tar")
        tar = tarfile.open(tar_file_new, "w")
        for key in image_dict.keys():
            z, x, y = key.split("_")
            z = int(int(z) - 1)
            x = int(int(x) / 2)
            y = int(int(y) / 2)
            key_new = str(z) + "_" + str(x) + "_" + str(y)

            if key_new in tmp_dict:
                continue
            data_new = __image_composite(image_dict, z, x, y, extension, img_format)
            tmp_dict[key_new] = data_new
            tile_name = str(zoom) + '/'+str(zoom) + "_" + str(x) + "_" + str(y) + "." + extension
            tarinfo = tarfile.TarInfo(name=tile_name)
            tarinfo.size = len(data_new)

            tar.addfile(tarinfo, io.BytesIO(data_new))
        tar.close()
        image_dict = tmp_dict
        tmp_dict.clear()
        end_time = time.time()
        print("cut image into tile, zoom = {zoom}".format(zoom = str(zoom)) + 
              ", time used: " + str(round(end_time - start_time, 3)) + "s.")