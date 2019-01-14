import os
import argparse
import gdal
from gdalconst import GA_ReadOnly
import glob
from shapely.geometry import box
import pandas as pd
import geopandas as gpd
from rasterstats import zonal_stats
import time

def _setup():
    parser = argparse.ArgumentParser(description='set up script with important file name variables')
    parser.add_argument('--ndvi_tif_directory', type=str, required=True, help='directory containing NDVI tif files exported from GEE')
    parser.add_argument('--census_tracts_shp', type=str, required=True, help='census tracts shp file')
    parser.add_argument('--output_csv', type=str, required=True, help='output csv filename')
    args = parser.parse_args()
    return args                           

if __name__ == "__main__":
    args = _setup()

    # create gdf for tiles
    filenames = []
    bboxes = []
    for filename in glob.glob(args.ndvi_tif_directory + "*.tif"):
        filenames.append(filename)
        data = gdal.Open(filename, GA_ReadOnly)
        geoTransform = data.GetGeoTransform()
        minx = geoTransform[0]
        maxy = geoTransform[3]
        maxx = minx + geoTransform[1] * data.RasterXSize
        miny = maxy + geoTransform[5] * data.RasterYSize
        ll = (minx, miny)
        ur = (maxx, maxy)
        b = box(minx, miny, maxx, maxy, ccw=True)
        bboxes.append(b)
    bbox_df = pd.DataFrame({
        'filename': filenames,
        'bbox': bboxes
    })
    bbox_gdf = gpd.GeoDataFrame(bbox_df, geometry='bbox')
    print(bbox_gdf.to_file('bboxes_2014.shp', driver='ESRI Shapefile'))

    '''
    # load in census tracts as gdf
    census_tracts_gdf = gpd.read_file(args.census_tracts_shp, driver = 'ESRI Shapefile', header=True)
    #census_tracts_gdf = census_tracts_gdf.head(2000)

    bbox_filenames_list = []
    bbox_list = []
    tract_list = []
    geo_id_list = []

    for idx, tract in census_tracts_gdf.iterrows():
        # Get the tif filenames that intersect the tract
        bbox_filenames_list.append(','.join(bbox_gdf[bbox_gdf.geometry.intersects(tract.geometry)]['filename'].tolist()))
        tract_list.append(tract['geometry'])
        geo_id_list.append(tract['GEO_ID'])
        print("done processing census tract " + str(idx) + " with geo id " + tract['GEO_ID'])

    per_tract_df = pd.DataFrame({
        'bbox_filename': bbox_filenames_list,
        'tracts': tract_list,
        'geo_ids':  geo_id_list
    })

    per_bbox_df = per_tract_df.groupby('bbox_filename')['tracts'].apply(list).to_frame()
    per_bbox_df2 = per_tract_df.groupby('bbox_filename')['geo_ids'].apply(list).to_frame()

    bboxes = []
    tracts = []
    geo_ids = []
    counts = []
    means = []
    nodata = []

    # go through each tif file/tile and create a df the tells us the zonal stats of each tract or 
    # partial tract that is contained within it
    count = 0
    # loop through each tile
    for idx in range(len(per_bbox_df['tracts'])):
        # get the tract geoms and ids contained within
        tract_list = per_bbox_df['tracts'][idx]
        geo_id_list = per_bbox_df2['geo_ids'][idx]

        # get the tif file(s) associated with each tract. most times just one tif file, but sometimes more if tract overlaps
        tif_files = per_bbox_df.index[idx].split(',')
        for idx2 in range(len(tract_list)):
            count += 1
            print("tract " + str(count))
            # get zonal stat of each tract. tif_files usually of length 1
            for tif_file in tif_files:
                bboxes.append(tif_file)
                tracts.append(tract_list[idx2])
                geo_ids.append(geo_id_list[idx2])
                try:
                    stat_dict = zonal_stats(tract_list[idx2], tif_file, stats="count nodata mean")
                except:
                    try:
                        time.sleep(5)
                        stat_dict = zonal_stats(tract_list[idx2], tif_file, stats="count nodata mean")
                    except: 
                        try:
                            time.sleep(300)
                            stat_dict = zonal_stats(tract_list[idx2], tif_file, stats="count nodata mean")
                        except:
                            import IPython
                            IPython.embed()
                means.append(stat_dict[0]['mean'])
                nodata.append(stat_dict[0]['nodata'])
                counts.append(stat_dict[0]['count'])

    
    true_count = [x-y for x,y in zip(counts, nodata)]
    zonal_stats_df = pd.DataFrame({
        'bbox': bboxes,
        'tract': tracts,
        'geo_id': geo_ids,
        'count': counts,
        'nodata': nodata,
        'true_count': true_count,
        'mean': means
    })

    zonal_stats_df.to_csv(args.output_csv)

    # create a df where each row is a tract and column summarizes annual ndvi
    ## group  zonal_stats_df by tract
    #import IPython
    #IPython.embed()
    #tract_stats_df = zonal_stats_df.groupby('geo_id')['mean', 'count'].apply(list).to_frame()
    
    '''

    
    

        




        

        
