from shapely.ops import voronoi_diagram
from shapely.affinity import scale
import geopandas as gpd



def create_convex_hull(
    geom:gpd.GeoDataFrame, 
    xscale=1.1,
    yscale=1.1,
):
    gdf = geom.copy()
    # Create a single geometry with Muilti points object
    multipoints = gdf.unary_union
    
    # Create a convex hull from the multipoints and scale it
    # with the purpose of creating a bounding box
    convex_hull = scale(
        multipoints.convex_hull,
        xfact = xscale,
        yfact = yscale,
    )
    
    return convex_hull

def create_voronoi(
    geom:gpd.GeoDataFrame, 
    xscale=1.1,
    yscale=1.1,
):
    gdf = geom.copy()
    # Create a single geometry with Muilti points object
    multipoints = gdf.unary_union
    
    # Create a convex hull from the multipoints and scale it
    # with the purpose of creating a bounding box
    
    convex_hull = scale(
        multipoints.convex_hull,
        xfact = xscale,
        yfact = yscale,
    )
    
    # Create a voronoi diagram from the multipoints 
    polys = gpd.GeoSeries([i for i in voronoi_diagram(multipoints)])
    cliped = polys.clip(convex_hull)
    
    d = {}
    
    for i, r in gdf.iterrows():
        for p in cliped:
            if p.contains(r['geometry']):
                d[i] = p
                break
        
    geopoly  =  gpd.GeoSeries(d)
    gdf['geometry'] = geopoly
    
    return gdf