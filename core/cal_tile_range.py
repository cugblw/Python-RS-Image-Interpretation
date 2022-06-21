import core.tile_lon_lat_convert as tlc

def tile_range_dict(extent, start_zoom, end_zoom):
    """
    计算瓦片的范围
    """
    tile_range = {}
    for zoom in range(start_zoom, end_zoom+1):
        #lon_min, lon_max, lat_min, lat_max, z
        (x_min,x_max,y_min,y_max) = tlc.bbox_to_xyz(extent[0], extent[2],extent[1], extent[3], zoom)
        tile_range[zoom] = (x_min,x_max,y_min,y_max)
    return tile_range

def tile_range_list(extent, start_zoom, end_zoom):
    """
    计算瓦片的范围
    """
    tile_range = []
    if end_zoom < max(end_zoom -4,start_zoom):
        for zoom in range(start_zoom, end_zoom+1):
            #lon_min, lon_max, lat_min, lat_max, z
            (x_min,x_max,y_min,y_max) = tlc.bbox_to_xyz(extent[0], extent[2],extent[1], extent[3], zoom)
            tile_range.append((zoom,max(end_zoom -4,start_zoom),x_min,x_max,y_min,y_max))
        return tile_range
    else:

        for zoom in range(start_zoom, max(end_zoom -4,start_zoom)):
            (x_min,x_max,y_min,y_max) = tlc.bbox_to_xyz(extent[0], extent[2],extent[1], extent[3], zoom)
            tile_range.append((zoom,max(end_zoom -4,start_zoom),x_min,x_max,y_min,y_max))
        (x_min,x_max,y_min,y_max) = tlc.bbox_to_xyz(extent[0], extent[2],extent[1], extent[3], max(end_zoom -4,start_zoom))
        for x in range(x_min, x_max+1):
            for y in range(y_min, y_max+1):
                tile_range.append((max(end_zoom -4,start_zoom),end_zoom,x,x,y,y))
        return tile_range
