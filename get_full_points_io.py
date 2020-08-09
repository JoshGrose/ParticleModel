import numpy
import math
import struct
import surface_mesh_generator_full_split as surf

def xyz_pass(file_name, initial_part_number, xsize, ysize, zsize, rho_cut, eta_cut):

    # this isnt necessary -- just passes information from one script to another
    surface_points_array = surf.CreateSurfacePoints(file_name, initial_part_number, xsize, ysize, zsize, rho_cut, eta_cut)
    return(surface_points_array)





