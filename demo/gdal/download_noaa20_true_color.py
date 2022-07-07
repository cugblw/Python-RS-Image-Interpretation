import datetime

from osgeo import gdal


# "gdal_translate -of JPEG  -projwin -180 90 180 -90 GIBS_NOAA20_True.xml GreatPlainsSmoke4.jpg"
# dataset =None
# gdal.Translate("GreatPlainsSmoke4.tif", "GIBS_NOAA20_True.xml", format="GTIFF", projWin=[-180, 90, 180, -90])

def generate_tms_driver_configuration_file(date, tile_size):
    # configuration = "<GDAL_WMS>
    #                 <Service name="TMS">
    #                 <ServerUrl>https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/VIIRS_NOAA20_CorrectedReflectance_TrueColor/default/2022-07-07/250m/${z}/${y}/${x}.jpg</ServerUrl>
    #                 </Service>
    #                 <DataWindow>
    #                     <UpperLeftX>-180.0</UpperLeftX>
    #                     <UpperLeftY>90</UpperLeftY>
    #                     <LowerRightX>396.0</LowerRightX>
    #                     <LowerRightY>-198</LowerRightY>
    #                     <TileLevel>2</TileLevel>
    #                     <TileCountX>2</TileCountX>
    #                     <TileCountY>1</TileCountY>
    #                     <YOrigin>top</YOrigin>
    #                 </DataWindow>
    #                 <Projection>EPSG:4326</Projection>
    #                 <BlockSizeX>512</BlockSizeX>
    #                 <BlockSizeY>512</BlockSizeY>
    #                 <BandsCount>3</BandsCount>
    #             </GDAL_WMS>"
    pass


def get_past_two_week_days():
    today = datetime.date.today()
    yestoday = today - datetime.timedelta(days=1)
    days = []
    for i in range(0, 14):
        days.append(yestoday - datetime.timedelta(days=i))
    return days

if __name__ == '__main__':
    days = get_past_two_week_days()
    for day in days:
        print(day)