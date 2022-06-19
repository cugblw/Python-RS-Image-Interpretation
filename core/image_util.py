from io import BytesIO

import numpy as np
from PIL import Image


def convert_image_from_array(rgb_data):
    return Image.fromarray(np.uint8(rgb_data)).convert('RGB')


def get_resize_times(height, width, size):
    times_height = height / (size * 20)
    times_width = width / (size * 20)
    times = max(times_height, times_width)
    return times


def resize_image(img, size):
    img_new = img.resize((size, size), Image.BOX)
    return img_new


def resize_image_by_times(img, times):
    img_new = None
    return img_new


def convert_image_transparency(img):
    rgba = img.convert("RGBA")
    datas = rgba.getdata()
    new_data = []
    for pixels in datas:
        if pixels[0] == 0 and pixels[1] == 0 and pixels[2] == 0:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(pixels)
    rgba.putdata(new_data)
    return rgba


def convert_image_to_bytes(img):
    # PIL Image to base64
    img_file = BytesIO()
    img.save(img_file, format='PNG')
    img_bytes = img_file.getvalue()  # im_bytes: image in binary format.
    return img_bytes





# 读取图片

# 读取视频

# 噪点去除

# 图像分割

# 转成灰度值

# 高斯模糊

# 边缘检测

# 图片膨胀

# 图片侵蚀


# 画形状（直线、矩形、圆、文字）

# 侦测颜色

# 轮廓检测