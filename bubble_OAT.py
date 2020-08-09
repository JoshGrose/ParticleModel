import csv
import numpy as np
import sys
FREECADPATH = '/usr/lib64/freecad/lib' # path to my freecad installation
sys.path.append(FREECADPATH)
import FreeCAD
import FreeCAD as App
import Part
import Mesh

App.newDocument("Unnamed")


part_number = 8
#def get_centroid(part_number):
mult = 1.3
sf = .01058
scale = mult*sf/1000.0
max_dist = []

time = 100 # eventually import this

folder_str = '/home/joshua/Downloads/particle_FULLset_' + str(time) + '_newbed' 
fusion_name = "Fusion"


for num in range(part_number):

    #sphere_name = "Sphere_" + str(part_number-num)
    sphere_name_old = "Sphere_" + str(num)
    sphere_name = "Sphere_" + str(num+1)
    export_string = u"%s/%s.stp" % (folder_str,fusion_name+'_OAT')
    dist_arr = []

    #xyz_string = '/home/joshua/simulations/scale/intermediate/point_cloud_part_' + str((part_number-1)-num) + '.xyz'
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

    fusion_name_old = fusion_name + str(num)
    fusion_name_new = fusion_name + str(num+1)

    if num ==1:
        App.activeDocument().addObject("Part::MultiFuse",fusion_name_new)
        fusion_string = 'App.activeDocument().' + fusion_name_new + '.Shapes = [App.activeDocument().' + sphere_name + ',App.activeDocument().' + sphere_name_old + ',]'
        print radius
        exec(fusion_string)    
        App.ActiveDocument.recompute()
       
    elif num>1:
        #__objs__=[]
        #__objs__.append(FreeCAD.getDocument("Unnamed").getObject(sphere_name))
        App.activeDocument().addObject("Part::MultiFuse",fusion_name_new)
        fusion_string = 'App.activeDocument().' + fusion_name_new + '.Shapes = [App.activeDocument().' + fusion_name_old + ',App.activeDocument().' + sphere_name + ',]'
        #App.activeDocument().Fusion.Shapes = [App.activeDocument().Sphere,App.activeDocument().Sphere002,App.activeDocument().Sphere001,App.activeDocument().Sphere003,]
        print radius
        exec(fusion_string)    
        App.ActiveDocument.recompute()


#solid_name = fusion_name + "_solid"
#__s__=App.ActiveDocument.Fusion.Shape.Faces
#__s__=Part.Solid(Part.Shell(__s__))
#__o__=App.ActiveDocument.addObject("Part::Feature",solid_name)
#__o__.Label=solid_name
#__o__.Shape=__s__

__objs__=[]
__objs__.append(FreeCAD.getDocument("Unnamed").getObject(fusion_name_new))
#del __s__, __o__

Part.export(__objs__, export_string) # exports solid part
del __objs__

