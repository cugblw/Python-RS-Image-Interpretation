import os
import sys
from pymbtiles import MBtiles, Tile
from osgeo_utils import gdal2mbtiles



tile_dir = r"C:\Users\Administrator\Desktop\tile_test"

def get_tile_list(tile_dir,extension):
    file_list = []
    for root, dirs, files in os.walk(tile_dir):
        for file in files:
            if file.endswith(extension):
                file_list.append(os.path.join(root, file))
    del dirs,root
    return file_list

def convert_tile_to_tiles(tile_list):
    tiles = []
    for tile_path in tile_list:
        tile_base_name = os.path.basename(tile_path)
        # print(tile_base_name)
        z,x,y = tile_base_name.split(".")[0].split('_')[0:3]
        z = int(z)
        x = int(x)
        y = int(y)
        with open(tile_path, 'rb') as f:
            tile_data = f.read()
            tile = Tile(z, x, y,tile_data)
            tiles.append(tile)
    return tiles


def save_tiles_to_mbtiles(tiles, mbtiles_path):
    with MBtiles(mbtiles_path, mode='w') as mbtiles:
        mbtiles.write_tiles(tiles)




# with MBTiles("my.mbtiles") as src:
#     mbtiles.add_tile(tile_data, x, y, z)
#     mbtiles.save()
#     mbtiles.close()

if __name__ == '__main__':
    tile_path = r'C:\Users\Administrator\Desktop\tile_test\15\15_25816_12855.png'
    tile_dir = r'C:\Users\Administrator\Desktop\tile_test'
    mbtiles = r'C:\Users\Administrator\Desktop\tile_test\my.mbtiles'
    # mbtiles = r'C:\Users\Administrator\Desktop\lanzhou_2m_test.mbtiles'
    tile_list = get_tile_list(tile_dir,".png")
    tiles = tuple(convert_tile_to_tiles(tile_list))
    print(tiles[0])
    save_tiles_to_mbtiles(tiles, mbtiles)
    # with MBtiles(mbtiles) as src:
    #     tile_data = src.read_tile(z=0, x=0, y=0)
    #     print(tile_data)