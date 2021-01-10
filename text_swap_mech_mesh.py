import sys
time = str(sys.argv[1])
mesh_type = int(sys.argv[2])
mesh_size_1 = str(sys.argv[3])
mesh_size_2 = str(sys.argv[4])
#mesh_size_3 = sys.argv[5]
index = str(sys.argv[5])

# setup for mechanical script
# replace first line with correct filepath
mechanical_file='/work/07329/joshg/stampede2/simulations/ParticleModel/sensitivity/mesh_results/meshResult_timestep' + str(time) + '_final/nanoparticle_sim_final_' + str(index) + '.js'
filepath_write_mechanical = '"//work//07329//joshg//stampede2//simulations//ParticleModel//sensitivity//mesh_results//meshResult_timestep' + str(time) + '_final"'
line_rep_mech = "var curr_dir = " + filepath_write_mechanical
with open(mechanical_file, 'r') as file:
    data_mech = file.readlines()

data_mech[1] = line_rep_mech + '\n'

# setup for export script
export_file='/work/07329/joshg/stampede2/simulations/ParticleModel/sensitivity/mesh_results/meshResult_timestep' + str(time) + '_final/temp_export_' + str(index) + '.js'
filepath_write_export = '"//work//07329//joshg//stampede2//simulations//ParticleModel//sensitivity//mesh_results//meshResult_timestep' + str(time) + '_final"'

line_rep_export = "var curr_dir = " + filepath_write_export
with open(export_file, 'r') as file:
    data_export = file.readlines()

data_export[1] = line_rep_export + '\n'

# 



# change mesh settings
# line numbers  #299 for curvature min size, 303 for proximity min size, 346 for body of influence, 363 for particle face sizing, 379 for air face sizing, 388 for curv min, 389 for prox min

L1a = 371 # particle face sizing +6 361 370
L1b = 387 # air face sizing +6 386
L2 = 354 #body of influence +2 +6 353 354
L3a = 300 # curve min body +2 +6  306
L3b = 304 #proximity min body +2 +6  310
L3c = 396 # curve min face +2 +6 395
L3d =  398 # prox min face +2 +6 397
Lfo = 22 

print(mesh_type)
print(type(mesh_type))

if mesh_type == 1:  # face sizing
    line_rep_FaceSizeA = 'ListView.ItemValue = ' + '"' + str(mesh_size_1) + '"'
    data_mech[L1a] = line_rep_FaceSizeA + '\n'

    line_rep_FaceSizeB = 'ListView.ItemValue = ' + '"' + str(mesh_size_2) + '"'
    data_mech[L1b] = line_rep_FaceSizeB + '\n'
 
    line_rep_out = 'var result_1 = filepath.concat("//TempResults_FaceSizing_Index_' + str(index) +  '");'  
    data_export[Lfo] = line_rep_out + '\n'

    print(mesh_size_1)

elif mesh_type == 2:  # body sizing

    line_rep_BoiSize = 'ListView.ItemValue = ' + '"' + str(mesh_size_1) + '"'
    data_mech[L2] = line_rep_BoiSize + '\n'

    line_rep_out = 'var result_1 = filepath.concat("//TempResults_BoiSizing_Index_' + str(index) +  '");'
    data_export[Lfo] = line_rep_out + '\n'

elif mesh_type == 3:  # both proximity sizings
    
    line_rep_ProxSize = ""
    data_mech[L3] = line_rep_ProxSize

    line_rep_out = 'var result_1 = filepath.concat("//TempResults_ProxSizing_Index_' + str(index) +  '");'
    data_export[Lfo] = line_rep_out

with open(mechanical_file, 'w') as file:
    file.writelines(data_mech)

with open(export_file, 'w') as file:
    file.writelines(data_export)
