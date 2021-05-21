# Name: PythonProject_Script_Pro
# Description: Data Preprocessing Tool to Project input shapefiles into the same Coordinate System
## save the intermediate files to a separate folder, Clip the intermediate files, and save outputs 
### in a new Geodatabase
# Author: Blake Hill

# Import system module
import arcpy
import sys

# Overwriting Files will be allowed
arcpy.env.overwriteOutput = True

# Local Variables
UDWorkspace = arcpy.GetParameterAsText(0)
FileEnding = arcpy.GetParameterAsText(1)
CoordinateSystem = arcpy.GetParameterAsText(2)
GDBLocation = arcpy.GetParameterAsText(3)
GDBName = arcpy.GetParameterAsText(4)
ClipLayer = arcpy.GetParameterAsText(5)

# Set workspace environment
arcpy.env.workspace = UDWorkspace

# Folder to store Intermediate Projected Layers
arcpy.CreateFolder_management(UDWorkspace, "UnclippedProjectedLayers")

# Create File Geodatabase to store Processed Files
arcpy.CreateFileGDB_management(GDBLocation, GDBName)

GDB = GDBLocation + "\\" + GDBName

# Check for Error in Clipped file name
if '.shp' in FileEnding:
    arcpy.AddError( 'Files saved in Geodatabase cannot have ".shp" file extension')
else:
    pass

# Check for Errors in GDB Name 
if '.gdb' in GDB:
    pass
else:
    arcpy.AddError( 'GDB Name must end in ".gdb"')
    sys.exit()
    
# Check for Errors in using a GEOCS instead of PROJCS
if 'PROJCS' in CoordinateSystem:
    pass
else:
    arcpy.AddError( 'Please select a **Projected** Coordinate System and run Tool again')
    sys.exit()


# List & print workspace featureclasses
FCList = arcpy.ListFeatureClasses()

# Project input layers to same Coordinate System and Store Intermediate Files in a separate folder
## for easy deletion afterwards, then batch clip the intermediate layers and save to new GDB
for FC in FCList:
    Output1 = UDWorkspace + "\\" + "UnclippedProjectedLayers" + "\\" + FC.replace('.shp', '_Project.shp')
    Output2 = GDB + "\\" + FC.replace('.shp', FileEnding)
    arcpy.Project_management(FC, Output1, CoordinateSystem)
    arcpy.Clip_analysis(Output1, ClipLayer, Output2)

arcpy.AddMessage( 'Intermediate files have been saved to Folder "UnclippedProjectedLayers" within the workspace')
arcpy.AddMessage( 'Folders may need to be refreshed in Catalog Pane to reflect changes')
