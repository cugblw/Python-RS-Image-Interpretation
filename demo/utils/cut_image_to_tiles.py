import time
import gdal2tiles

start_time = time.time()
gdal2tiles.generate_tiles(r'C:\Users\Administrator\Desktop\Image_Src\2m\lanzhou_2m_test.tif', r'C:\Users\Administrator\Desktop\tile_test')
end_time = time.time()
print("cut image into tile, time used: " + str(round(end_time - start_time, 3)) + "s.")