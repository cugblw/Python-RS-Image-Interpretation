import os
from PIL import Image

def delete_tile(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".jpg"):
                # print(os.path.join(root, file))
                # file_list.append(file)
                img = Image.open(os.path.join(root, file))
                if img.mode == 'RGBA':
                    del img
                    print('delete ' + file)
                    os.remove(os.path.join(root, file))

if __name__ == '__main__':
    path = r'C:\Users\Administrator\Desktop\tar_list\satellite'
    delete_tile(path)