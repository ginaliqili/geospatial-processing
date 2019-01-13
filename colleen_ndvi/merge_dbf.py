import arcpy
import glob,os
import csv
os.chdir("G:/My Drive/NDVI_2014")
from arcpy import env

env.workspace="G:/My Drive/NDVI_2014"
MergedArray=[]

for file_name in glob.glob("*.dbf"):
    geoid=arcpy.ListFields(str(file_name))[1]
    count=arcpy.ListFields(str(file_name))[2]
    mean=arcpy.ListFields(str(file_name))[3]
    print geoid
    geoid_name=geoid.name
    print geoid_name
    mean_name=mean.name
    count_name=count.name

    rows=arcpy.SearchCursor(str(file_name))

    for row in rows:
        id_val=row.getValue(geoid_name)
        id_val=str(id_val)
        #print type(id_val)
        cnt_val=row.getValue(count_name)
        #print type(cnt_val)
        ndvi_val=row.getValue(mean_name)



        for existingRow in MergedArray:
            if id_val == existingRow[0]:
                existingRow[2]=(existingRow[2]*existingRow[1]+cnt_val*ndvi_val)/(existingRow[1]+cnt_val)
                existingRow[1]=existingRow[1]+cnt_val
                break
        else:
            MergedArray.append([str(id_val),cnt_val,ndvi_val])


with open("G:/My Drive/NDVI_2014/result_2014.csv","wb") as f:
    writer=csv.writer(f)
    writer.writerow(['GEO_ID','COUNT','MEAN'])
    writer.writerows(MergedArray)
print len(MergedArray)
    
