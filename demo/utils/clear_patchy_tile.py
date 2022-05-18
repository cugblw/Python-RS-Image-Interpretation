import io
import os
import shutil
import tarfile
from PIL import Image
import time

class ClearPatchyTile(object):
    def __init__(self, tar_path):
        self.tar_path = tar_path

    def clear_patchy_tile(self):
        # pool = Pool(processes=4)
        self.un_tar_list(self.tar_path)
        self.delete_tile_from_directory(self.tar_path)
        self.zip_folders(self.tar_path)
        self.delete_folders(self.tar_path)

    def delete_tile_from_directory(self,tar_path):
        for root, dirs, files in os.walk(tar_path):
            for file in files:
                if file.endswith(".jpg"):
                    img = Image.open(os.path.join(root, file))
                    if img.mode == 'RGBA':
                        del img
                        print('delete ' + file)
                        os.remove(os.path.join(root, file))
        del root, dirs, files

    def delete_tile(self, tile_path):
        img = Image.open(tile_path)
        if img.mode == 'RGBA':
            del img
            print('delete ' + tile_path)
            os.remove(tile_path)
        

    def un_tar(self,tar_path):
        tar = tarfile.open(tar_path)
        names = tar.getnames()
        # temp_file_path = ''
        if os.path.isdir(tar_path.split('.tar')[0]):
            print(tar_path.split('.tar')[0] + ' 文件夹已存在')
            pass
        else:
            os.mkdir(tar_path.split('.')[0])
            print('创建一个新的文件夹：' + tar_path.split('.')[0])
        #解压后是很多文件，预先建立同名目录
        for name in names:
            tar.extract(name, tar_path.split('.')[0])
        tar.close()
        # return temp_file_path

    def delete_tar_file(self,tar_path):
        os.remove(tar_path)

    def delete_folders(self,tar_path):
        for file in os.listdir(tar_path):
            d = os.path.join(tar_path, file)
            if os.path.isdir(d):
                shutil.rmtree(os.path.join(tar_path, file))

    def un_tar_list(self,tar_path):
        for root, dirs, files in os.walk(tar_path):
            for file in files:
                if file.endswith(".tar"):
                    self.un_tar(os.path.join(root, file).replace('\\','/'))
        del root
        del dirs
        del files

    def zip_folders(self,tar_path):
        for root, dirs, files in os.walk(tar_path):
            # os.chdir(root)
            if 'satellite' in dirs:
                os.chdir(tar_path)
                break

            for tile_dir in dirs:
                os.chdir(os.path.join(root,tile_dir))

                with tarfile.open(tile_dir + '_new.tar', 'w') as tar:
                    tar.add('satellite')
                    tar.close()
                if os.path.exists(os.path.join(root,tile_dir) + '_new.tar'):
                    os.remove(tile_dir + '_new.tar')
                shutil.move(tile_dir + '_new.tar', root)

class FilterFullTile(object):
    def __init__(self, path, zoom_range):
        self.path = path
        self.zoom_range = zoom_range
        zoom_list = []
        for i in range(zoom_range[0], zoom_range[1] + 1):
            zoom_list.append(i)
        self.zoom_list = zoom_list

    def filter(self):
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if file.endswith(".tar"):
                    tar_file = tarfile.open(os.path.join(root, file))
                    members = tar_file.getmembers()
                    with tarfile.open(os.path.join(root, file.split(".")[0]+"_new.tar"), 'w') as tar:
                        for member in members:
                            image = tar_file.extractfile(member)
                            image = image.read()
                            img = Image.open(io.BytesIO(image))
                            zoom = member.name.split('/')[1]

                            if img.mode == 'RGB' and int(zoom) in self.zoom_list:
                                tarinfo = tarfile.TarInfo(name=member.name)
                                tarinfo.size = len(image)
                                tar.addfile(tarinfo=tarinfo, fileobj=io.BytesIO(image))
                                print("filter:",member.name)
                            else:
                                pass
                        tar.close()
        del root, dirs, files


if __name__ == '__main__':
    # 指定tar包的路径
    tar_path = r'C:\Users\Administrator\Desktop\tar_list'
    zoom_range = [12,17]
    
    time_start = time.time()

    # Method 1
    # clear_tile = ClearPatchyTile(tar_path)
    # clear_tile.clear_patchy_tile()

    # Method 2
    filter_tile = FilterFullTile(tar_path, zoom_range)
    filter_tile.filter()

    time_end = time.time()
    print('time used: ' + str(time_end - time_start) + 's')