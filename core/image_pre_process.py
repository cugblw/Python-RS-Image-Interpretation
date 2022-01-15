import os
import sys
from osgeo import gdal
from sqlalchemy import null


# 数据存放，保存目录

source_data_path = {
    "image":{
        "r_band":"/",
        "g_band":"/",
        "b_band":"/",
        "pan_band":"/",
        "nir_band":"/",
    },
    "vector":"/",
    "result":"/"
}

result_data_path = {
    "image":{
        "rgb_tif":"/",
        "fusion_tif":"/",
        "clip_tif":"/",
        "convert_crs_tif":"/"
    },
    "vector":"/",
}

class ImagePreProcess:
## 读取影像:哨兵/Landsat/GF-1/GF-2
## 读取矢量：shp/geojson
    def read_image():
        r_band = null
        g_band = null
        b_band = null
        nir_band= null
        pan_band = null

        return [b_band,g_band,r_band,pan_band,nir_band]


    def read_vector():
        return None


    ## 单波段：几何/正射校正
    def geometric_correction():
        return None


    ## 波段合成(RGB/Faslse Color)
    def rbg_color_composite():
        return None


    def false_color_composite():
        return None


    ## 影像融合(全色与多光谱)
    def image_fusion():
        return None


    ## 影像镶嵌(多幅影像之间)
    def image_mosaic():
        return None


    ## 匀色处理（多幅影像镶嵌之后）
    def image_seamless_mosaic():
        return null


    ## 影像裁剪(矢量边接)
    def clip_image():
        return None


    ## 大气校正
    def radiometric_correction():
        return None



if __name__ == '__main__':
    pass



