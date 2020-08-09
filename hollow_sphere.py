import csv
import numpy as np
import sys
FREECADPATH = '/usr/lib64/freecad/lib' # path to my freecad installation
sys.path.append(FREECADPATH)
import FreeCAD
import FreeCAD as App
import Part
import Mesh

part_number = int(sys.argv[1])
time = int(sys.argv[2])

#part_number = 18
#time = 4 # eventually import this

folder_str = '/home/joshua/Downloads/particle_FULLset_' + str(time) + '_newbed' 

hollow_name = "Sphere_hollow"
cut_string_old = hollow_name
count = 0

App.newDocument("Unnamed")

for num in range(part_number):

    sphere_name_small = "Sphere_small_" + str(num+1)
    sphere_name_large = "Sphere_" + str(num+1)

    insert_string_small = "/home/joshua/Downloads/particle_FULLset_" + str(time) + "_newbed/" + sphere_name_small + ".stp"    
    insert_string_large = "/home/joshua/Downloads/particle_FULLset_" + str(time) + "_newbed/" + sphere_name_large + ".stp"

    Part.insert(insert_string_small,"Unnamed")
    Part.insert(insert_string_large,"Unnamed")


    tool_name = sphere_name_small
    base_name = sphere_name_large
    cut_string = hollow_name + str(num+1)

    base_string = "App.activeDocument()." + cut_string + ".Base = App.activeDocument()." + base_name
    tool_string = "App.activeDocument()." + cut_string + ".Tool = App.activeDocument()." + tool_name
    App.activeDocument().addObject("Part::Cut", cut_string)
    exec(base_string)
    exec(tool_string)
    App.ActiveDocument.recompute()
    cut_string_old = cut_string
    count = count + 1

    __objs__=[]
    __objs__.append(FreeCAD.getDocument("Unnamed").getObject(cut_string))

    export_string = u"%s/%s.stp" % (folder_str,cut_string)
    Part.export(__objs__, export_string) # exports solid part
    del __objs__

    App.ActiveDocument.recompute()



#solid_name = fusion_name + "_solid"
#App.ActiveDocument.recompute()
#__s__=App.ActiveDocument.Fusion.Shape.Faces
#__s__=Part.Solid(Part.Shell(__s__))
#__o__=App.ActiveDocument.addObject("Part::Feature",solid_name)
#__o__.Label=solid_name
#__o__.Shape=__s__
