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

part_number = int(sys.argv[1])
time = int(sys.argv[2])

#part_number = 18
#time = 4 # eventually import this

folder_str = '/work/07329/joshg/stampede2/simulations/ParticleModel/results_mod/particle_FULLset4_' + str(time) + '_newbed' 
fusion_string = 'App.activeDocument().bubble.Shapes = ['
fusion_name = "bubble"

App.newDocument("Unnamed")

for num in range(part_number):

    sphere_name = "Sphere_hollow" + str(num+1)
    export_string = u"%s/%s.stp" % (folder_str,fusion_name)
    dist_arr = []

    insert_string = "/work/07329/joshg/stampede2/simulations/ParticleModel/results_mod/particle_FULLset4_" + str(time) + "_newbed/" + sphere_name + ".stp"

    Part.insert(insert_string,"Unnamed")

    #__objs__=[]
    #__objs__.append(FreeCAD.getDocument("Unnamed").getObject(sphere_name))
    fusion_string = fusion_string + 'App.activeDocument().' + sphere_name + ','

App.activeDocument().addObject("Part::MultiFuse",fusion_name)
#App.activeDocument().bubble.Shapes = [App.activeDocument().Sphere,App.activeDocument().Sphere002,App.activeDocument().Sphere001,App.activeDocument().Sphere003,]

fusion_string = fusion_string + ']'
exec(fusion_string)

solid_name = fusion_name + "_solid"

App.ActiveDocument.recompute()
#__s__=App.ActiveDocument.bubble.Shape.Faces
#__s__=Part.Solid(Part.Shell(__s__))
#__o__=App.ActiveDocument.addObject("Part::Feature",solid_name)
#__o__.Label=solid_name
#__o__.Shape=__s__

__objs__=[]
__objs__.append(FreeCAD.getDocument("Unnamed").getObject(fusion_name))
#del __s__, __o__

Part.export(__objs__, export_string) # exports solid part
del __objs__

