# Macro Begin: /home/joshua/.FreeCAD/create_block.FCMacro +++++++++++++++++++++++++++++++++++++++++++++++++
# Macro Begin: /home/joshua/.FreeCAD/extra_macro.FCMacro +++++++++++++++++++++++++++++++++++++++++++++++++
FREECADPATH = '/usr/lib64/freecad/lib' # path to my freecad installation
import sys
sys.path.append(FREECADPATH)

import FreeCAD as App

import Mesh
import Sketcher
import PartDesign
#import ImportGui
import Part

import surface_mesh_generator_full_split as surf_mesh
import get_boundary_scaled as bound # get_boundary_subset

def form_glass(minum, x_low, x_high, y_low, y_high, folder_name):

    #App.newDocument("Unnamed")
    App.activeDocument().addObject('Sketcher::SketchObject','Sketch')
    App.activeDocument().Sketch.Placement = App.Placement(App.Vector(0.000000,0.000000, minum),App.Rotation(0.000000,0.000000,0.000000,1.000000))
    #Gui.activeDocument().activeView().setCamera('#Inventor V2.1 ascii \n OrthographicCamera {\n viewportMapping ADJUST_CAMERA \n position 0 0 87 \n orientation 0 0 1  0 \n nearDistance -112.88701 \n farDistance 287.28702 \n aspectRatio 1 \n focalDistance 87 \n height 143.52005 }')
    #Gui.activeDocument().setEdit('Sketch')
    #Gui.getDocument('Unnamed').resetEdit()
    App.getDocument('Unnamed').recompute()
    App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(x_low,y_low,0),App.Vector(x_high,y_low,0))) # these 4 create the rectangle
    App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(x_high,y_low,0),App.Vector(x_high,y_high,0))) # x, y
    App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(x_high,y_high,0),App.Vector(x_low,y_high,0)))
    App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(x_low, y_high,0),App.Vector(x_low,y_low,0)))

    App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1)) 
    App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1)) 
    App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',2,2,3,1)) 
    App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',3,2,0,1)) 
    App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Horizontal',0)) 
    App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Horizontal',2)) 
    App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Vertical',1)) 
    App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Vertical',3)) 
    App.ActiveDocument.recompute()
    #App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',0,1,-1,1)) 
    App.ActiveDocument.recompute()
    #Gui.getDocument('Unnamed').resetEdit()
    App.getDocument('Unnamed').recompute()

#App.getDocument("Unnamed").addObject("Part::Extrusion","Extrude")
#App.getDocument("Unnamed").Extrude.Base = FreeCAD.getDocument("Unnamed").Sketch
#App.getDocument("Unnamed").Extrude.Dir = (0,0,-40)
#App.getDocument("Unnamed").Extrude.Solid = (True)
#App.getDocument("Unnamed").Extrude.TaperAngle = (0)
#FreeCADGui.getDocument("Unnamed").Sketch.Visibility = False
#App.getDocument("Unnamed").Extrude.Label = 'Extrude'

#App.getDocument("Unnamed").addObject("Part::Extrusion","Extrude001")
#App.getDocument("Unnamed").Extrude001.Base = FreeCAD.getDocument("Unnamed").Sketch
#App.getDocument("Unnamed").Extrude001.Dir = (0,0,-40)
#App.getDocument("Unnamed").Extrude001.Solid = (True)
#App.getDocument("Unnamed").Extrude001.TaperAngle = (0)
#FreeCADGui.getDocument("Unnamed").Sketch.Visibility = False
#App.getDocument("Unnamed").Extrude001.Label = 'Extrude001'


    App.activeDocument().addObject("PartDesign::Pad","Pad")
    App.activeDocument().Pad.Sketch = App.activeDocument().Sketch
    App.activeDocument().Pad.Length = 10.0
    App.ActiveDocument.recompute()
#Gui.activeDocument().hide("Sketch")
#Gui.activeDocument().setEdit('Pad',0)
    App.ActiveDocument.Pad.Length = .4232 # can be modified if needed
    App.ActiveDocument.Pad.Reversed = 1
    App.ActiveDocument.Pad.Midplane = 0
    App.ActiveDocument.Pad.Length2 = 100.000000
    App.ActiveDocument.Pad.Type = 0
    App.ActiveDocument.Pad.UpToFace = None
    App.ActiveDocument.recompute()
#Gui.activeDocument().resetEdit()
# Macro End: /home/joshua/.FreeCAD/create_block.FCMacro +++++++++++++++++++++++++++++++++++++++++++++++++

    __objs__=[]
    __objs__.append(App.getDocument("Unnamed").getObject("Pad"))
#ImportGui.export(__objs__,u"/home/joshua/Downloads.step")

#
    Part.export(__objs__, u"%s/glass_block.step" % (folder_name))

#

    del __objs__

def get_bounds(filename, initial_part_number, xsize, ysize, zsize, shifts, rho_cut, eta_cut):

    minum, x_low, x_high, y_low, y_high, z_high = bound.limits(filename, initial_part_number, xsize, ysize, zsize, shifts, rho_cut, eta_cut)

    return minum, x_low, x_high, y_low, y_high, z_high

def build_air(minum,  x_low, x_high, y_low, y_high, z_high):
    #App.newDocument("Unnamed")
    App.activeDocument().addObject('Sketcher::SketchObject','Sketch001')
    App.activeDocument().Sketch001.Placement = App.Placement(App.Vector(0.000000,0.000000, minum),App.Rotation(0.000000,0.000000,0.000000,1.000000))

    App.getDocument('Unnamed').recompute()
    App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(x_low,y_low,0),App.Vector(x_high,y_low,0))) # these 4 create the rectangle
    App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(x_high,y_low,0),App.Vector(x_high,y_high,0))) # x, y
    App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(x_high,y_high,0),App.Vector(x_low,y_high,0)))
    App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(x_low,y_high,0),App.Vector(x_low,y_low,0)))

    App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1))
    App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1))
    App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',2,2,3,1))
    App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',3,2,0,1))
    App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Horizontal',0))
    App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Horizontal',2))
    App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Vertical',1))
    App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Vertical',3))
    App.ActiveDocument.recompute()
    #App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',0,1,-1,1))
    #App.ActiveDocument.recompute()

    App.getDocument('Unnamed').recompute()

    App.activeDocument().addObject("PartDesign::Pad","Pad001")
    App.activeDocument().Pad001.Sketch = App.activeDocument().Sketch001
    App.activeDocument().Pad001.Length = 10.0
    App.ActiveDocument.recompute()

    height = z_high-minum
    App.ActiveDocument.Pad001.Length = height # larger for air (120) -- can be modified if necessary
    App.ActiveDocument.Pad001.Reversed = 0 # changed for air
    App.ActiveDocument.Pad001.Midplane = 0
    App.ActiveDocument.Pad001.Length2 = 0 #100.000000 #THIS LIKELY WILL BE CHANGED
    App.ActiveDocument.Pad001.Type = 0
    App.ActiveDocument.Pad001.UpToFace = None
    App.ActiveDocument.recompute()

    air_volume = App.ActiveDocument.Pad001.Shape.Volume

    return air_volume
#    __objs__=[]
#    __objs__.append(App.getDocument("Unnamed").getObject("Pad001"))
#ImportGui.export(__objs__,u"/home/joshua/Downloads.step")

#    Part.export(__objs__, u"/home/joshua/Downloads/air_block.step")

#    del __objs__

def build_cutting_block(minum, x_low, x_high, y_low, y_high):

    # modify downshift
    scale = .01058
    cb_shift = scale*40

    App.activeDocument().addObject('Sketcher::SketchObject','Sketch002')
    App.activeDocument().Sketch002.Placement = App.Placement(App.Vector(0.000000,0.000000, minum-cb_shift),App.Rotation(0.000000,0.000000,0.000000,1.000000)) #-40 needs to be parameterized

    App.getDocument('Unnamed').recompute()
    App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(x_low-cb_shift,y_low-cb_shift,0),App.Vector(x_high+cb_shift,y_low-cb_shift,0))) # these 4 create the rectangle
    App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(x_high+cb_shift,y_low-cb_shift,0),App.Vector(x_high+cb_shift,y_high+cb_shift,0))) # x, y
    App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(x_high+cb_shift,y_high+cb_shift,0),App.Vector(x_low-cb_shift,y_high+cb_shift,0))) # y's were ajdested for cuts on all sides
    App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(x_low-cb_shift,y_high+cb_shift,0),App.Vector(x_low-cb_shift,y_low-cb_shift,0)))

    App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1))
    App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1))
    App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',2,2,3,1))
    App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',3,2,0,1))
    App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Horizontal',0))
    App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Horizontal',2))
    App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Vertical',1))
    App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Vertical',3))
    App.ActiveDocument.recompute()
    #App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',0,1,-1,1))
    #App.ActiveDocument.recompute()

    App.getDocument('Unnamed').recompute()

    App.activeDocument().addObject("PartDesign::Pad","Pad002")
    App.activeDocument().Pad002.Sketch = App.activeDocument().Sketch002
    App.activeDocument().Pad002.Length = 10.0
    App.ActiveDocument.recompute()

    App.ActiveDocument.Pad002.Length = 1.638 # 60 plus 10 shift plus 40 for subset (this 40 should eventually be replaced with a specific value) ... larger for air (120) -- can be modified if necessary
    App.ActiveDocument.Pad002.Reversed = 0 # changed for air
    App.ActiveDocument.Pad002.Midplane = 0
    App.ActiveDocument.Pad002.Length2 = 1.058
    App.ActiveDocument.Pad002.Type = 0
    App.ActiveDocument.Pad002.UpToFace = None
    App.ActiveDocument.recompute()

def build_air_ext(minum,  x_low, x_high, y_low, y_high):
    #App.newDocument("Unnamed")
    App.activeDocument().addObject('Sketcher::SketchObject','Sketch003')
    App.activeDocument().Sketch003.Placement = App.Placement(App.Vector(0.000000,0.000000, minum),App.Rotation(0.000000,0.000000,0.000000,1.000000))

    App.getDocument('Unnamed').recompute()
    App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(x_low,y_low,0),App.Vector(x_high,y_low,0))) # these 4 create the rectangle
    App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(x_high,y_low,0),App.Vector(x_high,y_high,0))) # x, y
    App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(x_high,y_high,0),App.Vector(x_low,y_high,0)))
    App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(x_low,y_high,0),App.Vector(x_low,y_low,0)))

    App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1))
    App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1))
    App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Coincident',2,2,3,1))
    App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Coincident',3,2,0,1))
    App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Horizontal',0))
    App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Horizontal',2))
    App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Vertical',1))
    App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Vertical',3))
    App.ActiveDocument.recompute()
    #App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',0,1,-1,1))
    #App.ActiveDocument.recompute()

    App.getDocument('Unnamed').recompute()

    App.activeDocument().addObject("PartDesign::Pad","Pad003")
    App.activeDocument().Pad003.Sketch = App.activeDocument().Sketch003
    App.activeDocument().Pad003.Length = 10.0
    App.ActiveDocument.recompute()

    App.ActiveDocument.Pad003.Length = 1.2696 # 120 plus 10 due to offset above larger for air (120) -- can be modified if necessary
    App.ActiveDocument.Pad003.Reversed = 0 # changed for air
    App.ActiveDocument.Pad003.Midplane = 0
    App.ActiveDocument.Pad003.Length2 = 100.000000
    App.ActiveDocument.Pad003.Type = 0
    App.ActiveDocument.Pad003.UpToFace = None
    App.ActiveDocument.recompute()


