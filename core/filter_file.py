import os

# Filter Image files and remove others
def filter_files(image_dir):
    for root, dirs, files in os.walk(image_dir):
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list

        # 遍历文件
        for file in files:
            file_path = os.path.join(root,file)
            if file_path.endswith('tiff') or file_path.endswith('TIF') or file_path.endswith('tif'):
                pass
            else:
                os.remove(file_path)

# Convert the image format to tif
def convert_format_to_tif(img_path):
    if img_path.endswith("tif"):
        pass
    elif img_path.endswith("TIF") or img_path.endswith("tiff"):
        image_src = os.path.dirname(img_path)
        filename = os.path.basename(img_path)
        filename_new = filename.split(".")[0] + ".tif"
        os.rename(img_path, os.path.join(image_src,filename_new))
    else:
        image_src = os.path.dirname(img_path)
        filename = os.path.basename(img_path)
        filename_new = filename.split(".")[0] + ".tif"
        command = "gdal_translate -co TILED=YES -co COMPRESS=LZW -ot Byte -scale " + img_path + " " + os.path.join(image_src, filename_new)
        os.system(command)


if __name__ == '__main__':
    filter_files(r"C:\Users\Administrator\Desktop\Image_Src\2m")
    convert_format_to_tif(r"C:\Users\Administrator\Desktop\Image_Src\2m\xinjiang_1shi_5.TIF")