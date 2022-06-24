import base64
import os

def generate_file_name(zoom,x,y):
    return str(zoom) + '/' + str(zoom)+ "_" + str(x) + "_" + str(y) + ".png"

def search_tile(zoom: int, x: int, y: int):
    path = r'C:\Users\Administrator\Desktop\tile_test'
    tile_path = generate_file_name(zoom, x, y)
    file_path = os.path.join(path, tile_path)
    file_path_jpg = file_path.replace('.png', '.jpg')

    # if not os.path.exists(file_path) and not os.path.exists(file_path_jpg):
    #     print("Data does not exist!")
    #     blank = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR4nGP4//8/AwAI/AL+p5qgoAAAAABJRU5ErkJggg=="
    #     img = base64.b64decode(blank)
    #     return img
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
            return data
    elif os.path.exists(file_path_jpg):
        with open(file_path_jpg, "rb") as f:
            data = f.read()
            return data
    else:
        print("Data does not exist!")
        blank = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR4nGP4//8/AwAI/AL+p5qgoAAAAABJRU5ErkJggg=="
        img = base64.b64decode(blank)
        return img