import csv
import numpy as np
import sys
#FREECADPATH = '/work/07329/joshg/stampede2/software/conda/miniconda2/pkgs/freecad-0.18.2-py37h648b96a_0/lib' # path to my freecad installation
FREECADPATH = '/work/07329/joshg/stampede2/software/conda/miniconda2/pkgs/freecad-0.19.alpha2-py38h4ca094a_0/lib'
sys.path.append(FREECADPATH)
import FreeCAD
import FreeCAD as App
import Part
import Mesh
import Base     # from freeCAD import Base


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

folder_str = '/work/07329/joshg/stampede2/simulations/ParticleModel/results_mod/particle_FULLset4_' + str(time) + '_newbed' 
fusion_string = 'App.activeDocument().Fusion.Shapes = ['
fusion_name = "Fusion"

sketch_num = 0

for num in range(part_number):
    sphere_name = "Sphere_" + str(num+1)
    export_string = u"%s/%s.stp" % (folder_str,sphere_name)
    dist_arr = []
    xyz_string = '/work/07329/joshg/stampede2/simulations/ParticleModel/intermediate/time_' + str(time) + '/point_cloud_part_' + str(num) + '.xyz'
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



    # import sphere primatives
    App.getDocument("Unnamed").addObject("Part::Sphere",sphere_name)
    App.ActiveDocument.ActiveObject.Label = sphere_name
    App.ActiveDocument.recompute()

    FreeCAD.getDocument("Unnamed").getObject(sphere_name).Placement = App.Placement(App.Vector(x,y,z),App.Rotation(App.Vector(0,0,1),0))

    #FreeCAD.getDocument("Unnamed").getObject(sphere_name).Radius = '1 mm'
    FreeCAD.getDocument("Unnamed").getObject(sphere_name).Radius = radius

    App.ActiveDocument.recompute()


########################################################################### NEW #############################################################################

    # build spheres from scratch
    #radius = 40
    center = [x,y,z]
    sketch_num = sketch_num + 1
    sketch_name = "Sketch_" + str(sketch_num)

    #setup sketch
    App.activeDocument().addObject('Sketcher::SketchObject', sketch_name)               # 0.0000 also?
    getattr(App.ActiveDocument, sketch_name).Placement = App.Placement(App.Vector(0.000000,0.000000,center[2]),App.Rotation(0.000000,0.000000,0.000000,1.000000))
    getattr(App.ActiveDocument, sketch_name).MapMode = "Deactivated"

    getattr(App.ActiveDocument, sketch_name).addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector("Xiao",center[0],center[1],center[2]),App.Vector(0,0,1),radius),-1.5708,1.5708),False)
    getattr(App.ActiveDocument, sketch_name).addConstraint(Sketcher.Constraint('DistanceX',0,3,center[0])) # x center coordinate
    getattr(App.ActiveDocument, sketch_name).addConstraint(Sketcher.Constraint('DistanceY',0,3,center[1])) # y center coordinate
    getattr(App.ActiveDocument, sketch_name).addConstraint(Sketcher.Constraint('DistanceZ',0,3,center[2])) # y center coordinate

    getattr(App.ActiveDocument, sketch_name).addConstraint(Sketcher.Constraint('Radius',0,radius)) # radius 
    radius_string = str(radius) + " mm"
    getattr(App.ActiveDocument, sketch_name).setDatum(2,App.Units.Quantity(radius_string)) # radius
    getattr(App.ActiveDocument, sketch_name).addGeometry(Part.LineSegment(App.Vector(center[0],(center[1] - radius),0),App.Vector(center[0],(center[1] - radius),center[2])),False)
    getattr(App.ActiveDocument, sketch_name).addConstraint(Sketcher.Constraint('Vertical',1)) 
    getattr(App.ActiveDocument, sketch_name).addConstraint(Sketcher.Constraint('PointOnObject',0,3,1)) 
    getattr(App.ActiveDocument, sketch_name).addConstraint(Sketcher.Constraint('Coincident',0,2,1,1)) 
    getattr(App.ActiveDocument, sketch_name).addConstraint(Sketcher.Constraint('Coincident',0,1,1,2)) 

    App.getDocument('Unnamed').recompute()

    FreeCAD.ActiveDocument.addObject("Part::Revolution",sphere_name) # "Revolve"
    getattr(FreeCAD.ActiveDocument,sphere_name).Source = getattr(FreeCAD.ActiveDocument,sketch_name)
    getattr(FreeCAD.ActiveDocument,sphere_name).Axis = (0.000000000000000,-1.000000000000000,0.000000000000000)
    getattr(FreeCAD.ActiveDocument,sphere_name).Base = (center[0], (center[1] - radius),0.000000000000000)
    getattr(FreeCAD.ActiveDocument,sphere_name).Angle = 360.000000000000000
    getattr(FreeCAD.ActiveDocument,sphere_name).Solid = True
    getattr(FreeCAD.ActiveDocument,sphere_name).AxisLink = (getattr(App.ActiveDocument, sketch_name), "Edge2")
    getattr(FreeCAD.ActiveDocument,sphere_name).Symmetric = False

########################################################################################################################################



    # check for inverted spheres
    exec_string_volume = "new_vol = App.ActiveDocument." + sphere_name + ".Shape.Volume"
    exec(exec_string_volume)
    print(new_vol)
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

    print(radius)
    __objs__=[]
    __objs__.append(FreeCAD.getDocument("Unnamed").getObject(sphere_name))
    Part.export(__objs__, export_string) # exports solid part
    del __objs__

