import datetime
import os
from unicodedata import name

import lxml.etree
import lxml.builder

from osgeo import gdal


# "gdal_translate -of JPEG  -projwin -180 90 180 -90 GIBS_NOAA20_True.xml GreatPlainsSmoke4.jpg"
# dataset =None
# gdal.Translate("GreatPlainsSmoke4.tif", "GIBS_NOAA20_True.xml", format="GTIFF", projWin=[-180, 90, 180, -90])

def generate_tms_driver_xml_configuration_file(date, resolution, tile_size):
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
    configuration = GDAL_WMS(
        Service(
            ServerUrl(
                "https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/VIIRS_NOAA20_CorrectedReflectance_TrueColor/default/%s/%s/${z}/${y}/${x}.jpg" % (date,resolution)
            ),name="TMS"
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
    )
    return configuration


def get_past_two_week_days():
    today = datetime.date.today()
    yestoday = today - datetime.timedelta(days=1)
    days = []
    for i in range(0, 14):
        days.append(str(yestoday - datetime.timedelta(days=i)))
    return days

def download_oneday_cloud_image(store_path, xml_configuration, date, resolution, tile_size):
    xml_configuration = generate_tms_driver_xml_configuration_file(date, resolution, tile_size)
    xml_configuration_string = lxml.etree.tostring(xml_configuration, pretty_print=True).decode("utf-8")
    image_name = os.path.join(store_path,"noaa20_cloud_image_%s" % date + ".tif")
    gdal.Translate(image_name, xml_configuration_string, format="GTIFF", projWin=[-180, 85, 180, -85])
    # image_name = os.path.join(store_path,"noaa20_cloud_image_%s" % date + ".jpg")
    # gdal.Translate(image_name, xml_configuration_string, format="JPEG", projWin=[-180, 90, 180, -90])

def reproject_geotiff(image_dir):
    # gdal.Warp(image_path, image_path, dstSRS=srs)
    for image_name in os.listdir(image_dir):
        if image_name.endswith(".tif"):
            image_name_new = image_name.replace(".tif", "_new.tif")
            gdal.WarpOptions = gdal.WarpOptions(dstSRS="EPSG:4326")
            gdal.Warp(image_name, image_name_new, options=gdal.WarpOptions)
            os.remove(image_name)
            os.rename(image_name_new, image_name)
        else:
            os.remove(image_name)


if __name__ == '__main__':
    days = get_past_two_week_days()
    store_path = r"C:\Users\Administrator\Desktop\gif"

    # for day in days:
    #     xml_configuration = generate_tms_driver_xml_configuration_file(day, "250m", 512)
    #     print("start to download cloud image for %s." % day )
    #     times = 0
    #     while(times < 3):
    #         try:
    #             download_oneday_cloud_image(store_path, xml_configuration, day, "250m", 512)
    #             print("download cloud image for %s success." % day)
    #             break
    #         except:
    #             times += 1
    #             print("download cloud image for %s failed, try again." % day)
    #             continue
    reproject_geotiff(store_path)


    # print(lxml.etree.tostring(configuration, pretty_print=True).decode("utf-8"))
