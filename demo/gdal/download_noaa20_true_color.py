import io
import os
import site
import datetime

import lxml.etree
import lxml.builder
from PIL import Image
from osgeo import gdal
from osgeo import osr


for item in site.getsitepackages():
    if "/lib/site-packages" in item.replace("\\", "/"):
        os.environ['PROJ_LIB'] = os.path.join(
            item, 'pyproj/proj_dir/share/proj')


def generate_tms_driver_xml_configuration_file(date, resolution, tile_size):
    """
    Generate tms driver xml configuration file
    :param date:
    :param resolution:
    :param tile_size:
    :return:
    """
    E = lxml.builder.ElementMaker()
    GDAL_WMS = E.GDAL_WMS
    Service = E.Service
    ServerUrl = E.ServerUrl
    DataWindow = E.DataWindow
    UpperLeftX = E.UpperLeftX
    UpperLeftY = E.UpperLeftY
    LowerRightX = E.LowerRightX
    LowerRightY = E.LowerRightY
    TileLevel = E.TileLevel
    TileCountX = E.TileCountX
    TileCountY = E.TileCountY
    YOrigin = E.YOrigin
    Projection = E.Projection
    BlockSizeX = E.BlockSizeX
    BlockSizeY = E.BlockSizeY
    BandsCount = E.BandsCount
    ZeroBlockHttpCodes = E.ZeroBlockHttpCodes
    configuration = GDAL_WMS(
        Service(
            ServerUrl(
                "https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/VIIRS_NOAA20_CorrectedReflectance_TrueColor/default/%s/%s/${z}/${y}/${x}.jpg" % (
                    date, resolution)
            ), name="TMS"
        ),
        DataWindow(
            UpperLeftX("-180.0"),
            UpperLeftY("90"),
            LowerRightX("396.0"),
            LowerRightY("-198"),
            TileLevel("2"),
            TileCountX("2"),
            TileCountY("1"),
            YOrigin("top"),
        ),
        Projection("EPSG:4326"),
        BlockSizeX(str(tile_size)),
        BlockSizeY(str(tile_size)),
        BandsCount("3"),
        ZeroBlockHttpCodes("204,404"),
    )
    return configuration


def get_past_two_week_days():
    """
    获取两周前的日期
    :return:
    """
    today = datetime.date.today()
    yestoday = today - datetime.timedelta(days=1)
    days = []
    for i in range(0, 14):
        days.append(str(yestoday - datetime.timedelta(days=i)))
    return days


def download_oneday_cloud_image(store_path, xml_configuration, date):
    """
    Download one day cloud image
    :param store_path:
    :param xml_configuration:
    :param date:
    :return:
    """
    xml_configuration_string = lxml.etree.tostring(
        xml_configuration, pretty_print=True).decode("utf-8")
    file_name = os.path.join(
        store_path, "noaa20_cloud_image_%s" % date + ".tif")
    if os.path.exists(file_name):
        image_validity = check_image_validity(file_name)
        if image_validity:
            print("%s already exists" % file_name)
        else:
            gdal.SetConfigOption("GDAL_ERROR_ON_LIBJPEG_WARNING", "TRUE")
            gdal.Translate(file_name, xml_configuration_string,
                           format="GTIFF", projWin=[-180, 85, 180, -85])
    else:
        gdal.SetConfigOption("GDAL_ERROR_ON_LIBJPEG_WARNING", "TRUE")
        gdal.Translate(file_name, xml_configuration_string,
                       format="GTIFF", projWin=[-180, 85, 180, -85])
    # file_name = os.path.join(store_path,"noaa20_cloud_image_%s" % date + ".jpg")
    # gdal.Translate(file_name, xml_configuration_string, format="JPEG", projWin=[-180, 90, 180, -90])


def download_today_cloud_image(store_path, xml_configuration):
    """
    Download today cloud image
    :param store_path:
    :param xml_configuration:
    :return:
    """
    xml_configuration_string = lxml.etree.tostring(
        xml_configuration, pretty_print=True).decode("utf-8")
    file_name = os.path.join(
        store_path, "noaa20_cloud_image_%s" % datetime.date.today() + ".tif")
    if os.path.exists(file_name):
        image_validity = check_image_validity(file_name)
        if image_validity:
            print("%s already exists" % file_name)
        else:
            gdal.SetConfigOption("GDAL_ERROR_ON_LIBJPEG_WARNING", "TRUE")
            gdal.Translate(file_name, xml_configuration_string,
                           format="GTIFF", projWin=[-180, 85, 180, -85])
    else:
        gdal.SetConfigOption("GDAL_ERROR_ON_LIBJPEG_WARNING", "TRUE")
        gdal.Translate(file_name, xml_configuration_string,
                       format="GTIFF", projWin=[-180, 85, 180, -85])


def check_epsg(image_path):
    """
    Check srs
    :param image_dir:
    :return: EPSG:3857 or EPSG:4326
    """
    dataset = gdal.Open(image_path)
    proj_info = osr.SpatialReference(wkt=dataset.GetProjection())
    epsg = proj_info.GetAttrValue('AUTHORITY', 1)
    return epsg


def check_image_validity(image_path):
    """
    Check image validity
    :param image_path:
    :return:
    """
    try:
        info = gdal.Info(image_path)
        if info is None:
            return False
        elif os.path.getsize(image_path)/1024 < 50:
            return False
        else:
            return True
    except Exception as e:
        print(e)
        return False
    

def reproject_geotiff(image_dir):
    """
    Reproject geotiff to EPSG:3857
    :param image_dir:
    :return:
    """
    for file_name in os.listdir(image_dir):
        if file_name.endswith(".tif"):
            file_name_new = file_name.replace(".tif", "_new.tif")
            epsg = check_epsg(os.path.join(image_dir, file_name))
            if epsg == "3857":
                pass
            else:
                gdal.Warp(os.path.join(image_dir, file_name_new), os.path.join(
                    image_dir, file_name), dstSRS="EPSG:3857")
                os.remove(os.path.join(image_dir, file_name))
                os.rename(os.path.join(image_dir, file_name_new),
                          os.path.join(image_dir, file_name))
        else:
            # os.remove(os.path.join(image_dir, file_name))
            pass


def convert_geotiff_to_jpg(image_dir):
    """
    Convert geotiff to jpg
    :param image_dir:
    :return:
    """
    for file_name in os.listdir(image_dir):
        if file_name.endswith(".tif"):
            file_name_new = file_name.replace(".tif", ".jpg")
            gdal.Translate(os.path.join(image_dir, file_name_new), os.path.join(image_dir, file_name), format="JPEG",
                           projWin=[-20037508, 15000000, 20037508, -7000000])
            filter_folders(image_dir)
            # os.remove(os.path.join(image_dir, file_name))
        else:
            # os.remove(os.path.join(image_dir, file_name))
            pass


def modify_background(image_dir):
    """
    Modify background
    :param image_path:
    :return:
    """
    for file_name in os.listdir(image_dir):
        if file_name.endswith(".jpg"):
            file_name_new = file_name.replace(".jpg", "_new.jpg")
            image = Image.open(os.path.join(image_dir, file_name))
            image = image.convert("RGBA")
            datas = image.getdata()
            new_data = []
            background_pixel_number = 0
            for pixels in datas:
                if pixels[0] < 1 and pixels[1] < 1 and pixels[2] < 1:
                    new_data.append((255, 255, 255, 0))
                    background_pixel_number += 1
                else:
                    new_data.append(pixels)
            image.putdata(new_data)
            if background_pixel_number < 10:
                image.convert("RGB").save(os.path.join(image_dir, file_name_new))
            else:
                data = convert_to_8bit(image)
                image = Image.open(io.BytesIO(data))
                image.save(os.path.join(image_dir, file_name_new), "PNG")
            os.remove(os.path.join(image_dir, file_name))
            os.rename(os.path.join(image_dir, file_name_new), os.path.join(image_dir, file_name))
        else:
            pass


def convert_to_8bit(img):
    """
    Convert to 8 bit
    :param img:
    :return:
    """
    img.load()
    alpha = img.split()[-1]
    img = img.convert("RGB").convert('P', palette=Image.Palette.ADAPTIVE, colors=255)
    mask = Image.eval(alpha, lambda a: 255 if a <= 50 else 0)
    img.paste(255, mask)
    bytes_io = io.BytesIO()
    img.save(bytes_io, "PNG", transparency=255)
    data = bytes_io.getvalue()
    return data


def filter_folders(target_dir):
    """
    Filter folders
    :param target_dir:
    :return:
    """
    for file_name in os.listdir(target_dir):
        if file_name.endswith(".xml"):
            os.remove(os.path.join(target_dir, file_name))
        else:
            pass


def scroll_delete_unused_images(target_dir):
    """
    Scroll delete unused images
    :param target_dir:
    :return:
    """
    days = get_past_two_week_days()
    days.append(str(datetime.date.today()))
    for file_name in os.listdir(target_dir):
        if file_name.endswith(".jpg") or file_name.endswith(".tif"):
            file_name_date = file_name.split("_")[-1].split(".")[0]
            if file_name_date in days:
                pass
            else:
                os.remove(os.path.join(target_dir, file_name))
        else:
            pass


if __name__ == '__main__':
    days = get_past_two_week_days()
    store_path = r"C:\Users\Administrator\Desktop\gif"
    tif_path = r"C:\Users\Administrator\Desktop\gif\noaa20_cloud_image_2022-07-10.tif"

    for day in days:
        xml_configuration = generate_tms_driver_xml_configuration_file(
            day, "250m", 512)
        print("start to download cloud image for %s." % day)
        times = 0
        while(times < 3):
            try:
                download_oneday_cloud_image(store_path, xml_configuration, day)
                print("download cloud image for %s success." % day)
                break
            except:
                times += 1
                print("download cloud image for %s failed, try again." % day)
                continue
    download_today_cloud_image(store_path, xml_configuration)
    reproject_geotiff(store_path)
    convert_geotiff_to_jpg(store_path)
    # modify_background(store_path)
    scroll_delete_unused_images(store_path)
    

    # print(lxml.etree.tostring(configuration, pretty_print=True).decode("utf-8"))