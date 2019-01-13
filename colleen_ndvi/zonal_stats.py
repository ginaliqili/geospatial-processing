import arcpy
from arcpy import env
import time
import os
from arcpy.sa import *
import gc
import glob
gc.enable()

start=time.time()
os.chdir("E:/NDVI_output/2014")
arcpy.CheckOutExtension("spatial")
arcpy.env.overwriteOutput = True
env.workspace="E:/NDVI_output/2014"

tracts_shp="G:/My Drive/Gina Colleen NDVI Work/Census Tracts/us_contiguous_census_tracts_projected.shp"

# perform zonal statistics
count = 0
for img in glob.glob("*.img"):
    count += 1
    output_dbf = img[:10] + "_" + str(count) + ".dbf"
    print(output_dbf)
    try:
        arcpy.sa.ZonalStatisticsAsTable(tracts_shp,"GEO_ID", img , output_dbf, "DATA","ALL")
        arcpy.DeleteField_management(output_dbf,["ZONE_CODE","AREA","MIN","MAX","RANGE","STD","SUM","VARIETY","MAJORITY","MINORITY","MEDIAN"])
        print(img)
    except:
        print("issue with " + img)
    

end=time.time()
print(end-start)



