# Name: PythonProject_Script_Pro
# Description: Data Preprocessing Tool to Project input shapefiles into the same Coordinate System
## save the intermediate files to a separate folder, Clip the intermediate files, and save outputs 
### in a new Geodatabase
# Author: Blake Hill


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


arcpy.env.workspace = UDWorkspace

arcpy.CreateFolder_management(UDWorkspace, "UnclippedProjectedLayers")

arcpy.CreateFileGDB_management(GDBLocation, GDBName)

GDB = GDBLocation + "\\" + GDBName

# Error Checks
if '.shp' in FileEnding:
    arcpy.AddError( 'Files saved in Geodatabase cannot have ".shp" file extension')
else:
    pass


if '.gdb' in GDB:
    pass
else:
    arcpy.AddError( 'GDB Name must end in ".gdb"')
    sys.exit()

    
if 'PROJCS' in CoordinateSystem:
    pass
else:
    arcpy.AddError( 'Please select a **Projected** Coordinate System and run Tool again')
    sys.exit()

FCList = arcpy.ListFeatureClasses()


for FC in FCList:
    Output1 = UDWorkspace + "\\" + "UnclippedProjectedLayers" + "\\" + FC.replace('.shp', '_Project.shp')
    Output2 = GDB + "\\" + FC.replace('.shp', FileEnding)
    arcpy.Project_management(FC, Output1, CoordinateSystem)
    arcpy.Clip_analysis(Output1, ClipLayer, Output2)

arcpy.AddMessage( 'Intermediate files have been saved to Folder "UnclippedProjectedLayers" within the workspace')
arcpy.AddMessage( 'Folders may need to be refreshed in Catalog Pane to reflect changes')
