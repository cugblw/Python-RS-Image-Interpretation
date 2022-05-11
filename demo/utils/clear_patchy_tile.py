import os
import shutil
import tarfile
from PIL import Image

def delete_tile_from_directory(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".jpg"):
                img = Image.open(os.path.join(root, file))
                if img.mode == 'RGBA':
                    del img
                    print('delete ' + file)
                    os.remove(os.path.join(root, file))
    del root, dirs, files

def delete_tile(tile_path):
    img = Image.open(tile_path)
    if img.mode == 'RGBA':
        del img
        print('delete ' + tile_path)
        os.remove(tile_path)
    

def un_tar(tar_path):
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

def delete_tar_file(tar_path):
    os.remove(tar_path)

def delete_folders(path):
    for file in os.listdir(tar_path):
        d = os.path.join(tar_path, file)
        if os.path.isdir(d):
            shutil.rmtree(os.path.join(tar_path, file))

def un_tar_list(tar_path):
    for root, dirs, files in os.walk(tar_path):
        print(dirs)
        for file in files:
            if file.endswith(".tar"):
                un_tar(os.path.join(root, file).replace('\\','/'))
    del root
    del dirs
    del files

def zip_folders(path):
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


if __name__ == '__main__':
    tar_path = r'C:\Users\Administrator\Desktop\tar_list'
    
    un_tar_list(tar_path)
    delete_tile_from_directory(tar_path)
    zip_folders(tar_path)
    delete_folders(tar_path)