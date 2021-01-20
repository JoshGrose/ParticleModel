#FREECADPATH = '/work/07329/joshg/stampede2/software/conda/miniconda2/pkgs/freecad-0.18.2-py37h648b96a_0/lib' # path to my freecad installation
FREECADPATH = '/work/07329/joshg/stampede2/software/conda/miniconda2/pkgs/freecad-0.19.alpha2-py38h4ca094a_0/lib'
import sys
sys.path.append(FREECADPATH)
import FreeCAD
import FreeCAD as App
import Part
import Mesh
import numpy as np
import math

def save_and_export(folder_name, final_object_name, final_file_name):

    export_string = u"%s/%s.step" % (folder_name,final_file_name)

    __objs__=[]
    __objs__.append(FreeCAD.getDocument("Unnamed").getObject(final_object_name)) # use this to save and export each file
    Part.export(__objs__, export_string) # exports solid part
    del __objs__


def cut(base_name, tool_name, cut_num, original_volume, cut_type): # can these part ojects be imported? large_body001_solid, small_body001_solid, base_name, tool_name, cut_num, action_number

    import FreeCAD as App

    # check for negative geometry ...
    #exec_string_volume_base = "base_vol = App.ActiveDocument." + base_name + ".Shape.Volume"
    #exec(exec_string_volume_base, None, globals())
    #exec_string_volume_tool = "tool_vol = App.ActiveDocument." + tool_name + ".Shape.Volume"
    #exec(exec_string_volume_tool, None, globals())

    base_vol = getattr(App.ActiveDocument,base_name).Shape.Volume
    tool_vol = getattr(App.ActiveDocument,tool_name).Shape.Volume

    # print information about the incoming body volumes
    print("-------------For Incoming Cut " + str(cut_num) + ", These are the Input Volumes (Base Top, Tool Bottom)-----------")
    print(base_vol)
    print(tool_vol)


#    if base_vol < 0:
    
    
    #    exec_string_comp = "base_copy = App.ActiveDocument." + base_name + ".Shape.copy()"
    #    exec(exec_string_comp)
    #    base_copy.compliment()
    
#    if tool_vol < 0:
    

    #    exec_string_comp = "tool_copy = App.ActiveDocument." + tool_name + ".Shape.copy()"
    #    exec(exec_string_comp)
    #    tool_copy.compliment()
       


    # perform the cut
    if cut_num == 0:
        cut_string = "Cut"
    else:
        cut_string = "Cut00" + str(cut_num)

    #exec_string_1 = "App.activeDocument()." + cut_string + ".Base = App.activeDocument()." + base_name
    #exec_string_2 = "App.activeDocument()." + cut_string + ".Tool = App.activeDocument()." + tool_name
    App.activeDocument().addObject("Part::Cut", cut_string) 
    #exec(exec_string_1, None, globals())
    #exec(exec_string_2, None, globals())
    getattr(App.activeDocument(),cut_string).Base = getattr(App.activeDocument(),base_name)
    getattr(App.activeDocument(),cut_string).Tool = getattr(App.activeDocument(),tool_name)

    App.ActiveDocument.recompute()

    # check to see if body gets smaller after cut
    #exec_string_volume = "new_vol = App.ActiveDocument." + cut_string + ".Shape.Volume"
    #exec(exec_string_volume, None, globals())
    new_vol = getattr(App.ActiveDocument,cut_string).Shape.Volume
    shrink = True
    if new_vol > original_volume: # or new_vol < 0:
        shrink = False

    # check for inverted shape
    if new_vol < 0:
        #exec_string_copy = "cut_copy=App.ActiveDocument." + cut_string + ".Shape.copy()"
        #exec(exec_string_copy, None, globals())
        cut_copy=getattr(App.ActiveDocument,cut_string).Shape.copy()
        cut_copy.reverse()

        #cut_copy=App.ActiveDocument.point_cloud_part_15zz001_solid.Shape.copy()
        #cut_copy.reverse()
        cut_string = cut_string + "_rev"
        __o__=App.ActiveDocument.addObject("Part::Feature",cut_string)
        __o__.Label=cut_string
        __o__.Shape=cut_copy
        del cut_copy, __o__
        #exec_string_volume_rev = "new_vol = App.ActiveDocument." + cut_string + ".Shape.Volume"
        #exec(exec_string_volume_rev, None, globals())
        new_vol = getattr(App.ActiveDocument,cut_string).Shape.Volume

    # also use number of faces to determine size change
    cut_size = len(FreeCAD.getDocument("Unnamed").getObject(cut_string).Shape.Faces)

    # print cut information
    print("base name " + base_name)
    print("tool name " + tool_name)
    print("Old Volume: ABOVE, New Volume: BELOW")
    print(original_volume) # volume of the part after the cut is performed
    print(new_vol) # volume of the part before cut is performed
    print("---------------------End of Cut---------------------")
    print("\n \n \n")


    # append object to project
    __objs__=[]
    __objs__.append(FreeCAD.getDocument("Unnamed").getObject(cut_string))

    # using number of faces to determine size change ##############################
    cut_size = len(FreeCAD.getDocument("Unnamed").getObject(cut_string).Shape.Faces)

    return cut_string, cut_size, shrink


def intersect(object_1, object_2, cut_num):

    cut_string = "Cut00" + str(cut_num)

    App.activeDocument().addObject("Part::MultiCommon",cut_string)
    getattr(App.activeDocument(),cut_string).Shapes = [getattr(App.activeDocument(),object_1),getattr(App.activeDocument(),object_2),]

    App.ActiveDocument.recompute()

    return cut_string


def generate_solid(surf, surf_name, ind, stl_path):
    
    # import stl's, assign names and set up environment
    import FreeCAD as App
    #import_path = "/home/joshua/simulations/scale/" + str(surf)
    import_path = stl_path + str(surf)   

    part_name = surf_name + "00"+ "1" # + str(ind)
    solid_name = part_name + "_solid"
    solid_name_2 = part_name + " (Solid)"
    if ind == 0:
        App.newDocument("Unnamed")
    Mesh.insert(import_path, "Unnamed")
    App.getDocument("Unnamed").addObject("Part::Feature", part_name)

    # convert imported stl's to solid
    __shape__=Part.Shape()
    __shape__.makeShapeFromMesh(FreeCAD.getDocument("Unnamed").getObject(surf_name).Mesh.Topology,0.100000)
    App.getDocument("Unnamed").getObject(part_name).Shape=__shape__
    App.getDocument("Unnamed").getObject(part_name).purgeTouched()
    del __shape__

    # grab volumes for conductivity calculation
    #exec_string_volume = "App.ActiveDocument." + part_name + ".Shape.Volume"
    #exec(exec_string_volume, None, globals())

    vol = getattr(App.ActiveDocument,part_name).Shape.Volume    

    print(vol)
    volume = np.abs(vol)

    # export body to project
    #execute_string = "__s__=App.ActiveDocument." + part_name + ".Shape"
    #exec(execute_string, locals(), globals())
    __s__ = getattr(App.ActiveDocument,part_name).Shape

    __s__=Part.Solid(__s__)
    __o__=App.ActiveDocument.addObject("Part::Feature", solid_name) # "large_body001_solid" 
    __o__.Label= solid_name_2  #"large_body001 (Solid)"
    __o__.Shape=__s__
    del __s__ , __o__ # remember this has been changed

    return solid_name, volume 

def calculate_conductivities(volume_array):
# create conductivities list based on volumes -- ifs?
# actual volume scaling will be necessary at some point anyway -- get actual volume in nm^3 -- defaults to mm^3 apparenty

    k = []

    volume_array_nm = []

    for vol in volume_array:

        new_vol = abs(vol*(10**18))
        volume_array_nm.append(new_vol)

    vol_max = max(volume_array_nm)

    for vol in volume_array_nm:

        pow = 1.0/3.0
        d_eff = ((vol/vol_max)**pow)*425 # substitute assuming the largest particle is 100nm
        #pi = math.pi
        #d_eff = (vol*6/pi)**(1/3) -- useful once actual volumes are determined
        #print d_eff

        nat_log = np.log(d_eff)

        k_part = 37.262*nat_log + 145.46
        k.append(k_part)

    return k





#Part.export(__objs__, u"%s/glass_block.step" % (folder_name))
def import_object(folder_name, filename):
    
    # maybe add a recompute here?
    # App.ActiveDocument.recompute()
    file = u"%s/%s" % (folder_name,filename) #folder_name + filename      #Unicode?
    Part.insert(file,"Unnamed")
    

#return k
