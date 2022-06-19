import sys
import sys

import geojson
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt

sys.path.append('.')
import core.convert_format as convert

'''
https://pypi.org/project/sentinelsat/
# productsname 
https://scihub.copernicus.eu/twiki/do/view/SciHubUserGuide/FullTextSearch?redirectedfrom=SciHubUserGuide.3FullTextSearch
'''

# api = SentinelAPI('weillee', 'WeilLee2021')
# # footprint = geojson_to_wkt(read_geojson('res/vector/map.geojson'))
# print(footprint)
# products = api.query(footprint,
#                      producttype='SLC',
#                      orbitdirection='ASCENDING',
#                      limit=10)
# print(products)
# api.download_all(products)

class SentinelDownloader(object):
    def __init__(self, username, password):
        self.api = SentinelAPI(username, password)

    def search_images(self, api, footprint, platformname, date, cloudcoverpercentage):
        polygon_geojson = convert.polygon_to_geojson(footprint)
        footprint = geojson_to_wkt(polygon_geojson)
        products = api.query(footprint,
                             platformname=platformname,
                             date=date,
                             cloudcoverpercentage=cloudcoverpercentage)
        return products

    def download_images(self, products):
            self.api.download_all(products)


if __name__ == '__main__':
    Polygon = "POLYGON ((121.14744186401366 23.047985767509395, 121.26142501831056 23.047985767509395, 121.26142501831056 23.148252272743257, 121.14744186401366 23.148252272743257, 121.14744186401366 23.047985767509395))"
    download_path='res/image'
    downloader = SentinelDownloader('weillee', 'WeilLee2021')
    products = downloader.search_images(
        downloader.api, Polygon, 'Sentinel-2', ['20201201','20210630'], (0,5))
    if len(products) > 0:
        print('Found %s images' % len(products))
        downloader.download_images(products)
    # downloader.download_images(products)
    
