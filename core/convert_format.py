import geojson
import shapely.wkt


def points_to_geojson(points):
    """
    Convert a list of points to a geojson object.
    """
    return None


def polyline_to_geojson(polyline):
    """
    Convert a list of lines to a geojson object.
    """
    return None


def polygon_to_geojson(polygon):
    """
    Convert a list of polygons to a geojson object.
    """
    polygon_geometry = shapely.wkt.loads(polygon)
    polygon_geojson = geojson.Feature(geometry=polygon_geometry, properties={})
    # polygon_geojson.geometry
    return polygon_geojson



### To do
# geojson to shapefile

# coordinates to shp

# csv/txt to shapefile

# polygon to geojson
