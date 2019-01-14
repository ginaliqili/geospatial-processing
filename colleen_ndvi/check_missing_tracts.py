import pandas as pd
import geopandas as gpd

result_csv = 'E:/NDVI_output/2014/result_2014.csv'
census_tracts_shp = 'G:/My Drive/Gina Colleen NDVI Work/Census Tracts/us_contiguous_census_tracts_projected.shp'
# load in census tracts as gdf
census_tracts_gdf = gpd.read_file(census_tracts_shp, driver = 'ESRI Shapefile', header=True)
results_df = pd.read_csv(result_csv)
results_geoids = results_df['GEO_ID']
tracts_geoids = census_tracts_gdf['GEO_ID']
print(list(set(tracts_geoids) - set(results_geoids)))