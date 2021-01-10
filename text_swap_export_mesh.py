import sys
time = sys.argv[1]
filepath_nq = "/work/07329/joshg/stampede2/simulations/ParticleModel/results_mod/particle_FULLset4_" + str(time) + "_newbed/temp_export.js"
filepath_q = '"//work//07329//joshg//stampede2//simulations//ParticleModel//results_mod//particle_FULLset4_' + str(time) + '_newbed"'
line_rep = "var curr_dir = " + filepath_q
with open(filepath_nq, 'r') as file:
    data = file.readlines()

data[1] = line_rep + '\n'

with open(filepath_nq, 'w') as file:
    file.writelines(data)
