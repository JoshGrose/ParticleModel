FREECADPATH = '/usr/lib64/freecad/lib' # path to my freecad installation
import sys
sys.path.append(FREECADPATH)
import FreeCAD

import prologue_script as prologue
import freecad_operations_scaled as cad
import create_block_scaled as build
import numpy as np

def fc_main(folder_name, initial_part_number, part_number, file_name, stl_path, xsize, ysize, zsize, shifts, rho_cut, eta_cut):

    # set up peliminay arays/values and fill stl array with names of the surface meshes
    unordered_part_names = []
    stl_list = []
    part_name_list = []
    for i in range(1, part_number + 1):
        stl_list.append("point_cloud_part_%s.stl" %(str(i)))
        part_name_list.append("point_cloud_part_%s" %(str(i)))

    cut_number = 0
    face_check = 250  		# arbitrary, 2500 for original meshlab settngs -- modify based on the number of faces of the successful stl files
    volume_array = []

    # convert stl files to solid bodies
    for s in range(len(stl_list)):
        part_name, volume = cad.generate_solid(stl_list[s], part_name_list[s], s, stl_path)
        unordered_part_names.append(part_name)
        volume_array.append(volume)

    # build additional cad models (air, glass, cutting block) -- names assigned are names generated in freecad macro
    glass_name = "Pad"
    air_name = "Pad001"
    air_ext_name = "Pad003"
    CB_name = "Pad002"
    export_names = ["AirBlock","AirBlockExt"]
    
    minum, x_low, x_high, y_low, y_high, z_high  = build.get_bounds(file_name, initial_part_number, xsize, ysize, zsize, shifts, rho_cut, eta_cut) 		# this grabs the boundaries of the working space
    build.form_glass(minum, x_low, x_high, y_low, y_high, folder_name)
    air_volume = build.build_air(minum, x_low, x_high, y_low, y_high, z_high) 		# builds air and passes its volume for future cut checks
    build.build_cutting_block(minum, x_low, x_high, y_low, y_high)
    build.build_air_ext(minum, x_low, x_high, y_low, y_high) 		# builds top air column
    #air_cut_list = prologue.get_air_intersections(minum) 		# minum includes shift
    temp_vol = 10^8

    # (bool_temp hold the boolean, but it is likely not needed here)
    # cut out the form of the cutting block -- remove precut air and glass from the cutting block
    CB_name, size_temp, bool_temp = cad.cut(CB_name, air_name, cut_number, temp_vol, 1) # havent had an issue yet with the cutting block adding to the air
    cut_number+=1
    CB_name, size_temp, bool_temp = cad.cut(CB_name, glass_name, cut_number, temp_vol, 1)
    cut_number+=1
    print "Cutting Block Formed \n"

 
    # remove the bottom block of air from air_ext -- give air_ext its final shape, resting above the domain
    air_ext_name, size_temp, bool_temp = cad.cut(air_ext_name, air_name, cut_number, temp_vol, 1)
    cut_number+=1
    cad.save_and_export(folder_name, air_ext_name, export_names[1])


    for part_name in unordered_part_names:
        print "Air Cut -- Cut Begins Here"
        air_name, size_temp, bool_temp = cad.cut(air_name, part_name, cut_number, air_volume, 1) # havent had an issue here either
        cut_number += 1
    cad.save_and_export(folder_name,air_name,export_names[0])

    #calculate conductivities
    k_array = cad.calculate_conductivities(volume_array) # pass to ANSYS eventually

    # order the bodies by size based on number of xyz points
    parts = len(stl_list)
    part_set = prologue.get_order_by_size(file_name, initial_part_number, xsize, ysize, zsize, rho_cut, eta_cut) # part_set is the ordered list of part numbers -- used as indecies

    # interactions_array contains information on which parts cut which other parts
    interactions_array, interactions_matrix = prologue.detect_interactions(part_set, file_name, initial_part_number, xsize, ysize, zsize, rho_cut, eta_cut)

    for tool in part_set:

        for object in interactions_array[tool]:

            if interactions_matrix[tool][object] == 1: # watch the order of tool and object -- must match function where this is generated
                obj_ind = part_set.index(object)
               
                # does the object get smaller when cut?
                shrink = False
                while shrink == False:
                    temp_name, size, shrink = cad.cut(unordered_part_names[object], unordered_part_names[tool], cut_number, volume_array[object], 0)
                    cut_number += 1
                   
                    #check to see if geometries are actual bodies and not failed shapes 
                    if size < face_check:
                        # if size check fails, reverse the order of the cut
                        temp_name, size, bool_temp = cad.cut(unordered_part_names[tool], unordered_part_names[object], cut_number, volume_array[object], 0)
                        unordered_part_names[tool] = temp_name #temporary variable for the output name
                        print "Number of Faces is too Small to be Realistic: Replace Existing Cut with the Reverse Cut"
                        cut_number += 1

                    else:
                        unordered_part_names[object] = temp_name


    # see which particles intersect the cutting block
    CB_cut_list = prologue.get_CB_intersections(minum, x_low, x_high, y_low, y_high, file_name, initial_part_number, xsize, ysize, zsize, rho_cut, eta_cut)

    # use cutting block to slice off outer boundaries of nanoparticles
    for part in CB_cut_list:
        CB_shrink = False
        while CB_shrink == False:
            name, size, CB_shrink = cad.cut(unordered_part_names[part], CB_name, cut_number, volume_array[part], 0)
            cut_number +=1
            unordered_part_names[part] = name
            print "Cutting Block Particle Cut "

    # similar to above, use the glass block to cut the bottoms off the intersecting particles
    glass_cut_list = prologue.get_glass_intersections(minum, x_low, x_high, y_low, y_high, file_name, initial_part_number, xsize, ysize, zsize, rho_cut, eta_cut)

    # continue to loop until glass cut succeeds -- may need to account for negative volumes here
    for part in glass_cut_list:
        GP_bool = False
        while GP_bool == False:
            print "Glass Cut -- Cut Begins Here"
            name, size, GP_bool = cad.cut(unordered_part_names[part], glass_name, cut_number, volume_array[part], 0)
            cut_number +=1
            unordered_part_names[part] = name


    #save and export part names -- end of process
    for i in range(len(unordered_part_names)):
        
        particle_name = "Particle" + str(i+1)
        cad.save_and_export(folder_name, unordered_part_names[i], particle_name) # save final part

    z_low = minum

    x_low = x_low/1000
    x_high = x_high/1000
    y_low = y_low/1000
    y_high = y_high/1000
    z_low = z_low/1000
    z_high = z_high/1000


    bound_path = folder_name + "/part_bound.txt"
    fw = open(bound_path,"w+")
    fw.write(str(x_low) + "\n" + str(x_high) + "\n " + str(y_low) + "\n" + str(y_high) + "\n" + str(z_low) + "\n" + str(z_high))
    fw.close()

    num_path = folder_name + "/part_num.txt"
    fw1 = open(num_path,"w+")
    fw1.write(str(part_number))
    fw1.close()

    # calculate volume ratio and export to text file
    
    vol_array = np.array(volume_array)
    np_vol = np.sum(vol_array)
     
    volume_ratio = np_vol/((1000**3)*(x_high-x_low)*(y_high-y_low)*(z_high-z_low))
    vr_path = folder_name + "/volume_ratio.txt"
    fw1 = open(vr_path,"w+")
    fw1.write(str(volume_ratio))
    fw1.close()

