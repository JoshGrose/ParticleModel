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
mult = float(sys.argv[3])

#part_number = 18
#time = 4
#mult = 1.02

sf = .01058
scale = mult*sf/1000.0
max_dist = []

App.newDocument("Unnamed")

folder_str = '/home/joshua/Downloads/particle_FULLset_' + str(time) + '_newbed' 
fusion_string = 'App.activeDocument().Fusion.Shapes = ['
fusion_name = "Fusion"


for num in range(part_number):
    sphere_name = "Sphere_" + str(num+1)
    export_string = u"%s/%s.stp" % (folder_str,sphere_name)
    dist_arr = []
    xyz_string = '/home/joshua/simulations/scale/intermediate/point_cloud_part_' + str(num) + '.xyz'
    xyz_array = np.loadtxt(xyz_string).astype(float)
    col_avg_array = np.mean(xyz_array, axis=0)
    
    x = col_avg_array[0]*sf
    y =	col_avg_array[1]*sf 
    z =	col_avg_array[2]*sf 

    for point in xyz_array:
        dist = ((col_avg_array[0]-point[0])**2.0 + (col_avg_array[1]-point[1])**2.0 + (col_avg_array[2]-point[2])**2.0)**(0.50)
        dist_arr.append(dist) 
    
    len = max(dist_arr)*scale 
    max_dist.append(len)
    radius = str(len*1000) + ' mm'

    App.getDocument("Unnamed").addObject("Part::Sphere",sphere_name)
    App.ActiveDocument.ActiveObject.Label = sphere_name
    App.ActiveDocument.recompute()

    FreeCAD.getDocument("Unnamed").getObject(sphere_name).Placement = App.Placement(App.Vector(x,y,z),App.Rotation(App.Vector(0,0,1),0))

    #FreeCAD.getDocument("Unnamed").getObject(sphere_name).Radius = '1 mm'
    FreeCAD.getDocument("Unnamed").getObject(sphere_name).Radius = radius

    App.ActiveDocument.recompute()

    exec_string_volume = "new_vol = App.ActiveDocument." + sphere_name + ".Shape.Volume"
    exec(exec_string_volume)
    print new_vol
    if new_vol < 0:
        exec_string_copy = "sphere_copy=App.ActiveDocument." + sphere_name + ".Shape.copy()"
        exec(exec_string_copy)
        sphere_copy.reverse()

        sphere_name = sphere_name + "_rev"
        __o__=App.ActiveDocument.addObject("Part::Feature",sphere_name)
        __o__.Label=sphere_name
        __o__.Shape=sphere_copy
        del sphere_copy, __o__
        exec_string_volume_rev = "new_vol = App.ActiveDocument()." + sphere_name + ".Shape.Volume"
        exec(exec_string_volume_rev)
        App.ActiveDocument.recompute()

    print radius
    __objs__=[]
    __objs__.append(FreeCAD.getDocument("Unnamed").getObject(sphere_name))
    Part.export(__objs__, export_string) # exports solid part
    del __objs__

