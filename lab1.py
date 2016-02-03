#For each county in Washington, create a GeoJSON file whose filename is the county name 
#and whose contents are the polygons for the block groups within that county. 
#This means that you will end up with as many GeoJSON files as there are counties in WA.
#Each such file should be named after a county and contain only the block groups from that county.

import sys
sys.path.append('C:/Program Files (x86)/ArcGIS/Desktop10.3/bin')
sys.path.append('C:/Program Files (x86)/ArcGIS/Desktop10.3/arcpy')
sys.path.append('C:/Program Files (x86)/ArcGIS/Desktop10.3/ArcToolbox/Scripts')


import arcpy
from arcpy import env
env.workspace = "U:/geog458/saep_bg10_lab1"
saep = "saep_bg10.shp"

# list to save county name and fip
county = []
mycursor = arcpy.da.SearchCursor("WashingtonFIPS.dbf",["CountyName"])
for row in mycursor:
    county.append(row[0])

fip = []
mycursor = arcpy.da.SearchCursor("WashingtonFIPS.dbf",["FIPSCounty"])
for row in mycursor:
    fip.append(row[0])

# feature class to class
for i in range(0,len(fip)):
    outFeatureClass = str(county[i])
    inFeature = saep
    outLocation = "U:/geog458/saep_bg10_lab1/shp/"
    fipstr = str(fip[i])
    expression = '"COUNTYFP10" = ' + "'%s'" %fipstr #this expression?
  
    arcpy.FeatureClassToFeatureClass_conversion(inFeature, outLocation, 
    outFeatureClass, expression)
    
    

#shp file to geojson

from subprocess import call
import os
os.environ["GDAL_DATA"] = "C:/OSGeo4W/share/gdal"
os.environ["GDAL_DRIVER_PATH"] = "C:/OSGeo4W/bin/gdalplugins"
os.environ["PROJ_LIB"] = "C:/OSGeo4W/share/proj"
os.environ["PATH"] = "C:/OSGeo4W/bin;" + os.environ["PATH"] + ";c:/OSGeo4W/apps/msys/bins;C:/OSGeo4W/apps/Python27/Sripts"


import glob
os.chdir("U:/geog458/saep_bg10_lab1/shp1")   #work all the .shp file in one folder
for file in glob.glob("*.shp"):
    call(['C:\\OSGeo4W\\bin\\ogr2ogr',
      '-f','GeoJSON','-t_srs','WGS84',
      '-s_srs','EPSG:2927',
      file.replace('.shp', '.geojson'),
      file])

   
#sort popution and print out
pop = []
FIP = []
mycursor = arcpy.da.SearchCursor(saep , ["COUNTYFP10","POP2013"])
for row in mycursor:
    pop.append(row[1])
    FIP.append(row[0])
del mycursor


import pandas as pd 
import numpy as np   
df = pd.DataFrame({'FIP':FIP,'POP13':pop})
df1= pd.DataFrame({'county':county,'FIP':fip})
dfgroup = df.groupby('FIP',as_index=False)
dfsum  = dfgroup.agg(np.sum)


result = pd.merge(dfsum,df1, on='FIP', how='left')
result = result.sort(['POP13'], ascending=[False])

result



