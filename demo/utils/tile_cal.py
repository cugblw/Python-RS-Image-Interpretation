from multiprocessing import Pool
import os
import math
import time

def generate_file_name(source_name, z, x, y):
    """通过瓦片编号计算瓦片存储路径"""
    if z > 6:
        dir_ = 1 << (z - 5)
        row = int(y / dir_)
        col = int(x / dir_)
        file_name = os.path.join(source_name, str(z), "R" + str(row), "C" + str(col),
                                 str(z) + "_" + str(x) + "_" + str(y) + ".jpg")
    else:
        file_name = os.path.join(source_name, str(z), str(z) + "_" + str(x) + "_" + str(y) + ".jpg")
    return file_name

def calculate_tile_xyz_recusively(zoom, x, y,zoom_max,tile_index):
    """递归计算瓦片编号"""
    if zoom > zoom_max:
        return
    
    tile_number = generate_file_name("satellite", zoom, x, y)
    with open(tile_index, "a+") as f:
        f.write(tile_number + "\n")

    print(tile_number)
    calculate_tile_xyz_recusively(zoom + 1, x * 2, y * 2, zoom_max,tile_index)
    calculate_tile_xyz_recusively(zoom + 1, x * 2 + 1, y * 2, zoom_max,tile_index)
    calculate_tile_xyz_recusively(zoom + 1, x * 2, y * 2 + 1, zoom_max,tile_index)
    calculate_tile_xyz_recusively(zoom + 1, x * 2 + 1, y * 2 + 1, zoom_max,tile_index)

def calculate_tile_xyz(zoom, x, y,zoom_max,tile_index):
    """递归计算瓦片编号"""
    if zoom > zoom_max:
        return
    
    tile_number = generate_file_name("satellite", zoom, x, y)
    with open(tile_index, "a+") as f:
        f.write("1")
    
    calculate_tile_xyz(zoom + 1, x * 2, y * 2, zoom_max,tile_index)
    calculate_tile_xyz(zoom + 1, x * 2 + 1, y * 2, zoom_max,tile_index)
    calculate_tile_xyz(zoom + 1, x * 2, y * 2 + 1, zoom_max,tile_index)
    calculate_tile_xyz(zoom + 1, x * 2 + 1, y * 2 + 1, zoom_max,tile_index)



if __name__ == "__main__":
    start_time = time.time()
    if os.path.exists("tile_index.txt"):
        os.remove("tile_index.txt")
    pool = Pool(processes=8)
    pool.apply(calculate_tile_xyz, (0, 0, 0, 8, "tile_index.txt"))
    pool.close()
    # calculate_tile_xyz(0,0,0,8,'tile_index.txt')
    with open('tile_index.txt','r') as f:
        print(len(f.read()))
    end_time = time.time()
    print("time:",str((end_time - start_time)/60) + "min")
