The scripts in this folder were used to download, preprocess, and compute zonal statistics for the contiguous US census tracts based on annual NDVI composites for years 2012, 2013, and 2014 as part of Colleen's greenspace project.

Steps:
1) Run `ndvi_annual_composite_GEE.js` code in the code editor of Google Earth Engine (GEE). This script pulls the cloudfree imagery over the contiguous US by filtering the QA bands of surface reflectance imagery from Landsat 7 or Landsat 8 (L7 for 2012/2013, L8 for 2014), calculates NDVI, and outputs the image tiles to Google Drive. This step produces 33 image tiles (.tif files) per year, where each tif file is roughly 2GB. This step takes approximately 23 hours for each year. 

2) Run `convert_tif_img.py` to convert tif files to img files. This is a very time intensive task. Run in serial for one year, this will take 20 hours. I kicked off three separate jobs (one for each year) at the same time (total of 20 hours). In the future if this task needs to be shortened, multiprocessing can be implemented. Also, the reason we have to convert from .tif to .img is because step 3 does not work with tif files (some values result to nan after running arcpy's zonal statistics as table function).

3) Run `zonal_stats.py` to calculate the mean and pixel count for each census tract for each img file. This avoids having to mosaic all img files together and then runzonal statistics on a huge mosaic, which would be too computationally intensive. This step takes a little over 2 hours for each year.

4) Run `merge_dbf.py` to get the final output csv file for each year. This step solves the issue where duplicate zonal statistics are calculated for census tracts that overlap two or more img tiles. The mathematical algorithm used in this script to calculate the mean NDVI of those census tracts that share boundary with multiple tiles is as follows:

<div align="center">Mean NDVI = (NDVI<sub>1</sub> * Area<sub>1</sub> + NDVI<sub>2</sub> * Area<sub>2</sub> + ... + NDVI<sub>n</sub> * Area<sub>n</sub>) / (Area<sub>1</sub> + Area<sub>2</sub> + ... + Area<sub>n</sub>)</div>