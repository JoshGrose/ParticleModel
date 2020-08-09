import numpy as np
import get_full_points_io as get_points # need to modify get_points.py to create get_points_io.py

def get_order_by_size(file_name, initial_part_number, xsize, ysize, zsize, rho_cut, eta_cut):
    # check lengths of each array and determine order
    points_container = get_points.xyz_pass(file_name, initial_part_number, xsize, ysize, zsize, rho_cut, eta_cut) # list of xyz surface coordinates
    len_list = []
    len_list_unsort = []
    ordered_part_set = []
    for point_list in points_container:
        len_list_unsort.append(len(point_list))
        len_list.append(len(point_list))
    len_list.sort()
    np_list = np.array(len_list_unsort)

    for item in len_list:

        t = np.where(np_list == item)

        if len(t[0]) == 1:
            ordered_part_set.append(len_list_unsort.index(item)) # list of original part numbers created here
        else:
            for index in t[0]:
                if index not in ordered_part_set:
                    ordered_part_set.append(index)

    print ordered_part_set
    return ordered_part_set # correctly ordered

def detect_interactions(part_set, file_name, initial_part_number, xsize, ysize, zsize,  rho_cut, eta_cut):
    print "Part Set:"
    print part_set
    #num_of_parts = len(part_sets)
    points_container = get_points.xyz_pass(file_name, initial_part_number, xsize, ysize, zsize, rho_cut, eta_cut) # list of xyz surface coordinates

    part_list = points_container # represents entire body # imported from get_points # might need to be indexed or adjusted
    num_of_parts = len(part_list)
    final_list_inner = []
    final_list_outer = []

    interactions_array = []
    interactions_matrix = np.zeros((num_of_parts, num_of_parts)) # check on the syntax here

    # check to see if any lists match -- detects intersection

    for i in range(len(part_list)):
        final_list_inner = []
        for elem in range(len(part_list[i])): # remove [i]?
            final_list_inner.append(tuple(part_list[i][elem]))
        final_list_outer.append(set(final_list_inner))

    for tool in range(len(final_list_outer)):
        interactions_array.append([])
        for base in range(len(final_list_outer)):
            set_1 = final_list_outer[tool]
            set_2 = final_list_outer[base]
            if set_1 != set_2:
                if (set_1 & set_2):
                    #print "true"
                    interactions_array[tool].append(base)
                    #if interactions_matrix[k][j] == 0:
                    if part_set.index(tool) < part_set.index(base):
                        interactions_matrix[tool][base] = 1 # note the jk order

    print interactions_array
    print interactions_matrix
    print str(num_of_parts) + " number of parts passed from surface generator"
    return interactions_array, interactions_matrix # correctly ordered

def get_air_intersections(minum, x_low, x_high, y_low, y_high, file_name, initial_part_number, rho_cut, eta_cut): # this still has it split into 4 quadrants... it works, but is unnessary as of now

    air_cut_list_1 = []
    air_cut_list_2 = []
    air_cut_list_3 = []
    air_cut_list_4 = []
    air_cut_list = []

    xo = (x_low+x_high)/2
    yo = (y_low+y_high)/2

    points_container = get_points.xyz_pass(file_name, initial_part_number, rho_cut, eta_cut) # list of xyz surface coordinates

    part_list = points_container # represents entire body # imported from get_points # might need to be indexed or adjusted
    num_of_parts = len(part_list)
    bottom = minum

# NOTHING SHOULD BE BELOW 0 XMAX+XMIN /2

    for i in range(len(part_list)):
        in_block_1 = False
        in_block_2 = False
        in_block_3 = False
        in_block_4 = False

        for int in range(len(part_list[i])):
            if part_list[i][int][0] <= xo  and part_list[i][int][1] >= yo:
                in_block_1 = True
            if part_list[i][int][0] >= xo and part_list[i][int][1] >= yo:
                in_block_2 = True
            if part_list[i][int][0] <= xo and part_list[i][int][1] <= yo:
                in_block_3 = True
            if part_list[i][int][0] >= xo and part_list[i][int][1] <= yo:
                in_block_4 = True

        if in_block_1: # 0 or 2?
            air_cut_list_1.append(i)
        if in_block_2: # 0 or 2?
            air_cut_list_2.append(i)
        if in_block_3: # 0 or 2?
            air_cut_list_3.append(i)
        if in_block_4: # 0 or 2?
            air_cut_list_4.append(i)

    print air_cut_list_1
    print air_cut_list_2
    print air_cut_list_3
    print air_cut_list_4
    air_cut_list.append(air_cut_list_1)
    air_cut_list.append(air_cut_list_2)
    air_cut_list.append(air_cut_list_3)
    air_cut_list.append(air_cut_list_4)


    return air_cut_list

def get_CB_intersections(minum, x_low, x_high, y_low, y_high, file_name, initial_part_number, xsize, ysize, zsize, rho_cut, eta_cut):

    # scale the boundaies back up for comparison
    scale = 1/.01058
    minum = minum*scale
    x_high = x_high*scale
    y_high = y_high*scale

    x_low = x_low*scale
    y_low = y_low*scale
    

    CB_interactions_list = []
    points_container = get_points.xyz_pass(file_name, initial_part_number, xsize, ysize, zsize, rho_cut, eta_cut) # list of xyz surface coordinates

    part_list = points_container # represents entire body # imported from get_points # might need to be indexed or adjusted
    num_of_parts = len(part_list)

#    for i in range(len(part_list)):
#        if min(part_list[i][1]) < x_low or max(part_list[i][1]) > x_high: # 0 or 2?
#            CB_interactions_list.append(i)
    for i in range(len(part_list)):
        in_block_CB = False

        for int in range(len(part_list[i])):
            if part_list[i][int][0] <= x_low or part_list[i][int][0] >= x_high or part_list[i][int][1] <= y_low or part_list[i][int][1] >= y_high:
                in_block_CB = True
        if in_block_CB: # 0 or 2?
            CB_interactions_list.append(i)

    print CB_interactions_list
    return CB_interactions_list

def get_glass_intersections(minum, x_low, x_high, y_low, y_high, file_name, initial_part_number, xsize, ysize, zsize, rho_cut, eta_cut):

    # scale the boundaries back up for compaison
    scale = 1/.01058
    minum = minum*scale
    x_high = x_high*scale
    y_high = y_high*scale

    x_low = x_low*scale
    y_low = y_low*scale

    glass_interactions_list = []
    points_container = get_points.xyz_pass(file_name, initial_part_number, xsize, ysize, zsize, rho_cut, eta_cut) # list of xyz surface coordinates

    part_list = points_container # represents entire body # imported from get_points # might need to be indexed or adjusted
    num_of_parts = len(part_list)

#    for i in range(len(part_list)):
#        if min(part_list[i][1]) < x_low or max(part_list[i][1]) > x_high: # 0 or 2?
#            CB_interactions_list.append(i)
    for i in range(len(part_list)):
        in_block_glass = False

        for int in range(len(part_list[i])):
            if part_list[i][int][2] <= minum:
                in_block_glass = True
        if in_block_glass: # 0 or 2?
            glass_interactions_list.append(i)

    print glass_interactions_list
    return glass_interactions_list

