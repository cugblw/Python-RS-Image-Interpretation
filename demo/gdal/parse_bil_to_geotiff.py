import os
import site
import struct
import numpy as np
from osgeo import gdal, osr

for item in site.getsitepackages():
    if "/lib/site-packages" in item.replace("\\", "/"):
        os.environ['PROJ_LIB'] = os.path.join(item, 'pyproj/proj_dir/share/proj')

def parse_bil_file(bil_path, width, height):
    # where you put the extracted BIL file
    file = open(bil_path, "rb")
    contents = file.read()
    file.close()

    # unpack binary data into a flat tuple z
    s = "<%dH" % (int(width*height))
    z = struct.unpack(s, contents)

    heights = [[None for x in range(height)] for y in range(width)]

    for r in range(0,height):
        for c in range(0,width):
            elevation = z[(width*r)+c]

            if (elevation==65535 or elevation<0 or elevation>20000):
                # may not be needed depending on format, and the "magic number"
                # value used for 'void' or missing data
                elevation=0.0

            heights[r][c]=float(elevation)
    return np.array(heights)

def get_zoom_x_y(file_path):
    tile_number = (file_path.split('.')[0]).split('_')
    zoom = int(tile_number[0])
    x = int(tile_number[1])
    y = int(tile_number[2])
    return zoom, x, y

def tile2lonlat(zoom, px, py):
    #计算每个瓦片的经差和纬差
    angPerTile = float(360) / (2**zoom)
    #左上 角
    ulx = px * angPerTile -180 
    uly = (2**zoom - py ) * angPerTile -180
    #右下角
    lrx = ulx + angPerTile 
    lry = uly - angPerTile
    return [ulx, uly, lrx, lry]

def georeference_raster_tile(z, x, y, path):
    bounds = tile2lonlat(z, x, y)
    # bounds = [90.0, 40.97989806962013, 135.0, 0.0]
    print(bounds)
    filename, extension = os.path.splitext(path)
    gdal.Translate(filename + '.tif',
                   path,
                   outputSRS='EPSG:4326',
                   outputBounds=bounds)

# georeference_raster_tile(3,6,3,r"C:\Users\Administrator\Desktop\3_6_3.jpg")

def get_geotransform_from_boundary(boundary,size):
    geotransform = []
    
    #此处值的添加顺序不能调整
    geotransform.append(boundary[0])
    geotransform.append((boundary[2]-boundary[0])/size)
    geotransform.append(0.0)
    geotransform.append(boundary[1])
    geotransform.append(0.0)
    geotransform.append((boundary[3]-boundary[1])/size)
    
    return tuple(geotransform)

def save_array_to_tiff(tif_file_path,array_data,size,geotransform):
    driver = gdal.GetDriverByName("GTiff")
    wkt = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,\
    AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0],\
    UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AXIS["Latitude",\
    NORTH],AXIS["Longitude",EAST],AUTHORITY["EPSG","4326"]]'

    dst_ds = driver.Create(tif_file_path,
                        size,
                        size,
                        1,
                        gdal.GDT_Int16)

    #writting output raster
    dst_ds.GetRasterBand(1).WriteArray( array_data )
    #setting nodata value
    dst_ds.GetRasterBand(1).SetNoDataValue(-999)
    #setting extension of output raster
    # top left x, w-e pixel resolution, rotation, top left y, rotation, n-s pixel resolution
    dst_ds.SetGeoTransform(geotransform)
    # setting spatial reference of output raster
    srs = osr.SpatialReference()
    srs.ImportFromWkt(wkt)
    dst_ds.SetProjection( srs.ExportToWkt() )
    #Close output raster dataset

    ds = None
    dst_ds = None

if __name__ == '__main__':
    # dem瓦片文件大小
    size = 129
    # bil文件路径
    bil_path = r"C:\Users\Administrator\Desktop\bil\bil_zoom3"
    # tif文件保存路径
    tif_path = r"C:\Users\Administrator\Desktop\bil_to_tif"

    if not os.path.exists(tif_path):
        os.makedirs(tif_path)

    for root,dirs,files in os.walk(bil_path):
        for file in files:
            print("start to parse '{}';".format(file))
            file_name = file.split('.')[0] + '.tif'
            tif_file_name = os.path.join(tif_path,file_name)
            zoom, x, y = get_zoom_x_y(file)
            geo_boundary = tile2lonlat(zoom, x ,y)
            geotransform =get_geotransform_from_boundary(geo_boundary,size)
            array_data = parse_bil_file(os.path.join(root,file),size,size)
            save_array_to_tiff(tif_file_name,array_data,size,geotransform)
            print("convert '{}' to '{}';".format(file,file_name))

    print ("Convert bil to geotiff  completed!")