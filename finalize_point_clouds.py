import numpy
import math
import struct
import surface_mesh_generator_full_split as surf
import sys

file_name = str(sys.argv[1])
initial_part_number = sys.argv[2]
xsize = sys.argv[3]
ysize = sys.argv[4]
zsize = sys.argv[5]
rho_cut	= sys.argv[6]
eta_cut	= sys.argv[7]
stl_path = sys.argv[8]


initial_part_number = int(initial_part_number)
xsize = int(xsize)
ysize = int(ysize)
zsize = int(zsize)
rho_cut = float(rho_cut)
eta_cut = float(eta_cut)
stl_path = str(stl_path)


surface_points_array = surf.CreateSurfacePoints(file_name, initial_part_number, xsize, ysize, zsize, rho_cut, eta_cut)

num = numpy.arange(int(24))

for i in range(len(surface_points_array)):

    surface_points = surface_points_array[i]
    
    point_cloud_name = "point_cloud_part_%d.xyz" %(num[i])
    point_cloud_location = stl_path + point_cloud_name    

    bin = open(point_cloud_location, "w+")
    for i in surface_points:
        bin.write(str(i[0]) + ' ' + str(i[1]) + ' ' + str(i[2]) + '\n')




