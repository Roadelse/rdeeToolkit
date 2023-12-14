#coding=utf-8


def get_gdf_from_def(x_orig, y_orig, x_cell, y_cell, rows, cols, crs = '+proj=longlat +datum=WGS84 +no_defs', format = "gdf"):
    import geopandas as gpd
    from shapely.geometry import Polygon, box

    polygons = []
    for row in range(rows):
        for col in range(cols):
            polygons.append(box(x_orig + col * x_cell, y_orig + row * y_cell, x_orig + (col + 1) * x_cell, y_orig + (row + 1) * y_cell))
    resGdf = gpd.GeoDataFrame(geometry = polygons)
    resGdf.crs = crs

    if format == 'gse':
        return resGdf.geometry
    else:
        return resGdf

def get_gdf_from_latlon1d(lats, lons, format = "gdf", lat_edge_half = False, crs = '+proj=longlat +datum=WGS84 +no_defs'):
    import geopandas as gpd
    from shapely.geometry import Polygon, box

    dLat = lats[1] - lats[0]
    dLon = lons[1] - lons[0]

    rows = len(lats)
    cols = len(lons)

    polygons = []
    for row in range(rows):
        for col in range(cols):
            if lat_edge_half and row == 0:
                polygons.append(box(lons[col] - dLon / 2, lats[row], lons[col] + dLon / 2, lats[row] + dLat / 2))
            elif lat_edge_half and row == rows - 1:
                polygons.append(box(lons[col] - dLon / 2, lats[row] - dLat / 2, lons[col] + dLon / 2, lats[row]))
            else:
                polygons.append(box(lons[col] - dLon / 2, lats[row] - dLat / 2, lons[col] + dLon / 2, lats[row] + dLat / 2))
    resGdf = gpd.GeoDataFrame(geometry = polygons)
    resGdf.crs = crs

    if format == 'gse':
        return resGdf.geometry
    else:
        return resGdf