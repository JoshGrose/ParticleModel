import sys
time = sys.argv[1]
index = sys.argv[2]

path_to_file='/work/07329/joshg/stampede2/simulations/ParticleModel/sensitivity/mesh_results/meshResult_timestep' + str(time) + '_final/nanoparticle_workbench_final_' + str(index) +'.wbjn'

path_swap = '"//work//07329//joshg//stampede2//simulations//ParticleModel//sensitivity//mesh_results//meshResult_timestep' + str(time) + '_final"'

line_swap = "path = " + path_swap
with open(path_to_file, 'r') as file:
    data = file.readlines()

# give the workbench file the actual path
data[10] = line_swap + '\n'

# give the workbench file the mechanical filename
data[114] = 'mech_path = filepath_js + "//nanoparticle_sim_final_' + str(index) + '.js"' + '\n'

# give the workbench file the export filename
data[145] = 'mech_path = filepath_js + "//temp_export_' + str(index) + '.js"' + '\n'

with open(path_to_file, 'w') as file:
    file.writelines(data)
