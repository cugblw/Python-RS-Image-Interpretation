import io
import os
import shutil
import tarfile
from PIL import Image
import time
from shapely.geometry import Polygon
from osgeo import ogr

# sys.path.append('././')

import tile_lon_lat_convert as tc

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

class FilterFullTileExcludeCostal(object):
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
                            try :
                                tile_number = member.name.split('/')[4].split('.')[0]
                            except:
                                tile_number = member.name.split('/')[2].split('.')[0]
                                
                            z = int(tile_number.split('_')[0])
                            x = int(tile_number.split('_')[1])
                            y = int(tile_number.split('_')[2])

                            tile_boundary = tc.tile_edges(x, y, z)
                            intersection = self.boundary_intersect(tile_boundary)
                            
                            # if tile_number in costal_tile:
                            if int(zoom) in self.zoom_list:
                                if intersection or img.mode == 'RGB':
                                    tarinfo = tarfile.TarInfo(name=member.name)
                                    tarinfo.size = len(image)
                                    tar.addfile(tarinfo=tarinfo, fileobj=io.BytesIO(image))
                                    print("filter:",member.name)
                                else:
                                    pass
                            else:
                                pass
                        tar.close()
        del root, dirs, files

    def get_costal_range(self):
        Eastern_Coastal = [116.42954534252267, 26.375432078565836, 124.88526561489479, 42.17183258739287]
        Southern_Coastal = [106.88975836856439, 17.021485110593748, 123.77022557897759, 26.7161387562072]
        return Eastern_Coastal, Southern_Coastal
    
    def get_costal_wkt(self):
        Eastern_Coastal_WKT = "Polygon ((118.56670541136396935 26.49932541588997026, 118.69059874868810311 32.47717894177941389, 117.6065320471019362 36.28689906449652369, 116.42954534252267251 39.10547248862056335, 116.73927868583299983 40.4373258648549978, 117.14193203213643812 40.90192587982050298, 118.59767874569500634 41.49041923211013483, 120.85873215186045115 42.01696591573769979, 123.55341223866035705 42.17183258739287055, 124.82331894623271751 41.39749922911703095, 124.8852656148947915 39.84883251256536596, 123.58438557299137983 37.74264577805509191, 122.81005221471555444 35.14088569424828989, 122.74810554605348045 33.87097898667592233, 124.26579892827412266 31.26921890286911321, 123.70827891031552781 26.37543207856583649, 118.56670541136396935 26.49932541588997026))"
        Southern_Coastal_WKT = "Polygon ((118.56670541136396935 26.7161387562072008, 123.77022557897758759 26.56127208455203359, 121.416252169819046 21.45067191993152278, 116.30565200519853875 19.46837852274538605, 111.72159852420558934 17.54803179422131265, 108.22161174479882106 17.02148511059374769, 107.13754504321265415 17.20732511657994834, 106.88975836856438661 21.48164525426255622, 107.04462504021954317 22.72057862750389035, 115.28353197227443161 24.14535200673142867, 118.56670541136396935 26.7161387562072008))"

        return Eastern_Coastal_WKT, Southern_Coastal_WKT

    def boundary_intersect(self, tile_boundary):
        tile_boundary_wkt = Polygon([(tile_boundary[0],tile_boundary[1]),(tile_boundary[0],tile_boundary[3]),(tile_boundary[2],tile_boundary[3]),(tile_boundary[2],tile_boundary[1])])
        eastern_coastal_wkt, southern_coastal_wkt = self.get_costal_wkt()

        tile_boundary_polygon = ogr.CreateGeometryFromWkt(str(tile_boundary_wkt))
        
        eastern_coastal_polylon = ogr.CreateGeometryFromWkt(eastern_coastal_wkt)
        southern_coastal_polygon = ogr.CreateGeometryFromWkt(southern_coastal_wkt)
        easten_insection = tile_boundary_polygon.Intersection(eastern_coastal_polylon)
        south_insection = tile_boundary_polygon.Intersection(southern_coastal_polygon)

        if easten_insection.ExportToWkt() == 'POLYGON EMPTY' and south_insection.ExportToWkt() == 'POLYGON EMPTY':
            return False
        else:
            return True
    


if __name__ == '__main__':
    # # 指定tar包的路径
    tar_path = r'C:\Users\Administrator\Desktop\Image_Out'
    zoom_range = [1,22]
    
    time_start = time.time()

    # Method 1
    # filter_tile = FilterFullTile(tar_path, zoom_range)
    # filter_tile.filter()
    
    # Method 2 保留沿海地区半透明瓦片
    filter_tile = FilterFullTileExcludeCostal(tar_path, zoom_range)
    filter_tile.filter()

    time_end = time.time()
    print('time used: ' + str(time_end - time_start) + 's')
