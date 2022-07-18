info_dict = {'description': 'D:\\lanzhou_2m.tif',
             'driverShortName': 'GTiff',
             'driverLongName': 'GeoTIFF',
             'files': ['D:\\lanzhou_2m.tif'],
             'size': [20551, 6606],
             'coordinateSystem': {'wkt': 'GEOGCRS["WGS 84",DATUM["World Geodetic System 1984",ELLIPSOID["WGS 84",6378137,298.257223563,LENGTHUNIT["metre",1]]],PRIMEM["Greenwich",0,ANGLEUNIT["degree",0.0174532925199433]],CS[ellipsoidal,2],AXIS["geodetic latitude (Lat)",north,ORDER[1],ANGLEUNIT["degree",0.0174532925199433]],AXIS["geodetic longitude (Lon)",east,ORDER[2],ANGLEUNIT["degree",0.0174532925199433]],ID["EPSG",4326]]', 'dataAxisToSRSAxisMapping': [2, 1]},
             'geoTransform': [103.57949413680839, 1.8e-05, 0.0, 36.14077426942471, 0.0, -1.8e-05],
             'metadata': {'': {'AREA_OR_POINT': 'Area'}, 'IMAGE_STRUCTURE': {'INTERLEAVE': 'PIXEL'}},
             'cornerCoordinates': {'upperLeft': [103.5794941, 36.1407743], 'lowerLeft': [103.5794941, 36.0218663], 'lowerRight': [103.9494121, 36.0218663], 'upperRight': [103.9494121, 36.1407743], 'center': [103.7644531, 36.0813203]},
             'wgs84Extent': {'type': 'Polygon', 'coordinates': [[[103.5794941, 36.1407743], [103.5794941, 36.0218663], [103.9494121, 36.0218663], [103.9494121, 36.1407743], [103.5794941, 36.1407743]]]},
             'bands': [{'band': 1, 'block': [20551, 1], 'type': 'Byte', 'colorInterpretation': 'Red', 'description': 'Layer_1', 'noDataValue': 0.0, 'metadata': {'': {'LAYER_TYPE': 'athematic'}}}, 
                       {'band': 2, 'block': [20551, 1], 'type': 'Byte', 'colorInterpretation': 'Green', 'description': 'Layer_2', 'noDataValue': 0.0, 'metadata': {'': {'LAYER_TYPE': 'athematic'}}}, 
                       {'band': 3, 'block': [20551, 1], 'type': 'Byte', 'colorInterpretation': 'Blue', 'description': 'Layer_3', 'noDataValue': 0.0, 'metadata': {'': {'LAYER_TYPE': 'athematic'}}}]}


print(info_dict['coordinateSystem']['wkt'])