import arcpy
from arcpy import env
import time
import os
from arcpy.sa import *
import gc
import glob
gc.enable()

start=time.time()
os.chdir("G:/My Drive/NDVI_2012")
arcpy.CheckOutExtension("spatial")
arcpy.env.overwriteOutput = True
env.workspace="G:/My Drive/NDVI_2012"
outpath = "E:/NDVI_output/2012/"

tracts_shp="G:/My Drive/Gina Colleen NDVI Work/Census Tracts/us_contiguous_census_tracts_projected.shp"


# convert all NDVI tif files to img files

for tif in glob.glob("*.tif"):
    try: 
        arcpy.CopyRaster_management(tif, outpath + tif.split(".")[0]+".img", "", "-3.402823e+38", "", "", "", "")
        print("converted " + tif + " to " + tif.split(".")[0]+".img")
    except:
        print("failed to conver " + tif + " to IMG file")
