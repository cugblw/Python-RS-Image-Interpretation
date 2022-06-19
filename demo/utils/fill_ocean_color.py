# -*- encoding: utf-8 -*-

'''
@File    :   fill_ocean_color.py
@Time    :   2022/06/14 01:07:33
@Author  :   Lee
@Version :   1.0
@License :   (C)Copyright Cennavi, Li Wei
@Desc    :   填充海水颜色，只争取16m的切图结果
'''


import io
import os
import tarfile
from PIL import Image

class FillOCeanColor(object):
    """
    input: tar_path, new_path, color
    """
    def __init__(self, tar_path, new_path, color="#131D29"):
        self.tar_path = tar_path
        self.new_path = new_path
        self.color = color


    def fill_transparency(self):
        """
        fill transparency
        """
        for root, dirs, files in os.walk(self.tar_path):
            for file in files:
                if file.endswith('.tar'):
                    tar_file = tarfile.open(os.path.join(root, file))
                    members = tar_file.getmembers()
                    with tarfile.open(os.path.join(self.new_path, file.split(".")[0]+"_new.tar"), 'w') as tar:
                        for member in members:
                            image = tar_file.extractfile(member)
                            image = image.read()
                            img = Image.open(io.BytesIO(image))
                            if img.mode == 'RGBA':
                                data = self.fill_ocean_color(img, self.color)
                                tarinfo = tarfile.TarInfo(member.name)
                                tarinfo.size = len(data)
                                tar.addfile(tarinfo, io.BytesIO(data))

                            else:
                                tarinfo = tarfile.TarInfo(member.name)
                                tarinfo.size = len(image)
                                tar.addfile(tarinfo, io.BytesIO(image))
                    tar_file.close()
                    tar.close()
        del root, dirs, files, file, tar_file, members, member, image, img, tarinfo


    def fill_ocean_color(self, img, color = "#131D29"):
        new_img = Image.new("RGBA", img.size,color)
        new_img.paste(img, (0,0),img)
        new_img = new_img.convert("RGB")
        bytes_io = io.BytesIO()
        new_img.save(bytes_io, format="JPEG")
        data = bytes_io.getvalue()
        return data


if __name__ == '__main__':
    tar_path = r"C:\Users\cugbl\Desktop\out"
    new_path = r"C:\Users\cugbl\Desktop\new"
    # 海洋填充背景颜色
    color = "#131D29"
    fc = FillOCeanColor(tar_path, new_path, color)
    fc.fill_transparency()