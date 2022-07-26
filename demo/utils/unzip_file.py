import os
import tarfile


def unzip_result_tar(tar_path):
    '''unzip result tar file'''
    for root, dirs, files in os.walk(tar_path):
        if len(dirs) != 0:
            return
        else:
            for file in files:
                if file.endswith('.tar'):
                    tar_file = os.path.join(root, file)
                    tar = tarfile.open(tar_file)
                    tar.extractall(path=tar_path)
                    tar.close()

if __name__ == '__main__':
    tar_path = r'C:\Users\Administrator\Desktop\new'
    unzip_result_tar(tar_path)