The scripts in this folder were used to download, preprocess, and compute zonal statistics for the contiguous US census tracts based on annual NDVI composites for years 2012, 2013, and 2014 as part of Colleen's greenspace project.

Steps:
1) Run `ndvi_annual_composite_GEE.js` code in the code editor of Google Earth Engine (GEE) this script pulls the cloudfree imagery by filtering the QA bands over a bounding box representing the contiguous US from Landsat 7 or Landsat 8 (L7 for 2012/2013, L8 for 2014), calculates NDVI, and outputs the image tiles to Google Drive. This step produces 33 image tiles (.tif files) per year.

2) Run `convert_tif_img.py` to convert tif files to img files.

3) Run `zonal_stats.py` to calculate the mean and pixel count for each census tract for each img file. This avoids having to mosaic all img files together and then running zonal statistics, which would be too computationally intensive.

4) Run `merge_dbf.py` to get the final output csv file for each year. This step solves the issue where duplicate zonal statistics are calculated for census tracts that overlap two or more image tiles. The mathematical algorithm used in this script to calculate the mean NDVI of those census tracts that share boundary with multiple tiles of an NDVI img file is as follows:

Mean NDVI = (NDVI1*Area1+NDVI2*Area2+...+NDVIn*AreaN)/(Area1+Area2+..._AreaN)