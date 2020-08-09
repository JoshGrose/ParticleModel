FREECADPATH = '/usr/lib64/freecad/lib' # path to my freecad installation
import sys
sys.path.append(FREECADPATH)
import FreeCAD

import prologue_script as prologue
#import multi_intersection_script as multi_intersection
#import freecad_operations_2 as cad
#import create_block as build
import freecad_scaled as fcad
#import miscilaneous as misc
import numpy as np
import sys

folder_name = str(sys.argv[1])
initial_part_number = sys.argv[2]
part_number = sys.argv[3]
data_file_name = str(sys.argv[4])
stl_path = str(sys.argv[5])
xsize = sys.argv[6]
ysize = sys.argv[7]
zsize = sys.argv[8]
x_shift_h = sys.argv[9]
x_shift_l = sys.argv[10]
y_shift_h = sys.argv[11]
y_shift_l = sys.argv[12]
z_shift_l = sys.argv[13]
rho_cut	= sys.argv[14]
eta_cut	= sys.argv[15]

shift_inputs = np.array([x_shift_h, x_shift_l, y_shift_h, y_shift_l, z_shift_l])
shifts = shift_inputs.astype(np.float)

xsize = int(xsize)
ysize = int(ysize)
zsize = int(zsize)
rho_cut	= float(rho_cut)
eta_cut	= float(eta_cut)


initial_part_number=int(initial_part_number)
part_number = int(part_number)
fcad.fc_main(folder_name, initial_part_number, part_number, data_file_name, stl_path , xsize, ysize, zsize, shifts, rho_cut, eta_cut)


