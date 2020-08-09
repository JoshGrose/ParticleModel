#!/bin/bash

# BASH SCRIPT FOR RUNNING SINGLE TIMESTEP STEP FILE GENERATOR

initial_part_number=21
#timestep=8 #2 #0 #7500 #2000  #400 #200 # -- numbers in the 1000's represent decimals -> 2000 = .2 
time_array=(0 2 4 6 8 10 20 30 40 50 60 70 80 90 100 110 120 130 140 150 160 170 180 190 200 400 600 800 1000 1400 2000 2400 3000 3400 4000)
#time_array=(2000)
NUMTIME=35

# important parameters for the sim
# size of the domain
xsize=61 #60 #50
ysize=104 #104 #96
zsize=104 #104 #96

# boundary shifts to generate cuts
x_shift_h=7.0  #7.0 # this wave of shifts works for the early time steps
x_shift_l=7.0  #7.0
y_shift_h=7.0  #7.0
y_shift_l=7.0  #7.0
#z_shift_h=7.0 #7.0
z_shift_l=3.5  #3.5

# density cutoff
rho_cut=.02 #0.05  
# partie contribution cutoff
eta_cut=.000002 #0.000005

# Location of stl and xyz files
stl_path='/home/joshua/simulations/scale/intermediate/'                                                                                      # PATH TO STL/XYZ FILES
#stl_path='/home/joshua/simulations/scale/temp/'

# build georgina filenames
declare -a file_arr=()
declare -a fol_arr=()

# run script for all timesteps -- replace 1 with num_time
for ((num=0;num<NUMTIME;num++)); do
  # create file and part names
  timestep=${time_array[num]}
  data_path='/home/joshua/simulations/scale/timeseries/fullT'"$timestep"'SN50400002.dat'                                                     # PATH TO GEORGINA DATA FILES
  folder_name='/home/joshua/Downloads/particle_FULLset_'"$timestep"'_newbed'                                                                  # PATH TO FOLDER WHERE STEP FILES WILL BE SAVED
  mkdir "$folder_name"
  folder_name="$folder_name"

  # get the number of particles in the current system
  part_number=`python /home/joshua/simulations/scale/part_number.py $data_path $initial_part_number $xsize $ysize $zsize $rho_cut $eta_cut`                    #  PATH TO PYTHON SCRIPTS
  PARTS=$((part_number - 1)) # variable controlling other loops

  # generate the point clouds by filtering for only the surface points
  python /home/joshua/simulations/scale/finalize_point_clouds.py $data_path $initial_part_number $xsize $ysize $zsize $eta_cut $rho_cut $stl_path< /dev/null                   #  PATH TO PYTHON SCRIPTS

  # create list of xyz and stl filenames to pass into meshlab
  xyz_names=()
  stl_names=()

  for ((numa=0;numa<=PARTS;numa++)); do
    stl_num=$((numa + 1))
    xyz_names+=("$stl_path"'point_cloud_part_'"$numa"'.xyz')
    stl_names+=("$stl_path"'point_cloud_part_'"$stl_num"'.stl')
  done

  #run meshlab to generate the stl files
  for ((numo=0;numo<=PARTS;numo++));
  do
    snap run meshlab.meshlabserver -i ${xyz_names[numo]} -o ${stl_names[numo]} -s /home/joshua/simulations/scale/mewtwo_script_orig.mlx      # PATH TO PYTHON SCRIPTS -- wont be snap run on TACC
  done

  # run feeecad script to generate solid bodies and ontacts between partiles                                                                 # PATH TO PYTHON SCRIPTS (line below)
  python /home/joshua/simulations/scale/convert_scaled.py $folder_name $initial_part_number $part_number $data_path $stl_path $xsize $ysize $zsize $x_shift_h $x_shift_l $y_shift_h $y_shift_l $z_shift_l $rho_cut $eta_cut  < /dev/null

  # determine the number of pieces of air are contained in the air block step file
  python /home/joshua/simulations/scale/step_search.py $folder_name                                                                          # PATH TO PYTHON SCRIPTS
  echo "Run Complete"

  # clean folder
  #cd /home/joshua/simulations/scale/intermediate/
  #rm *point_cloud_part*
  #cd ..

done

#for ((num=0;num3<NUMTIME;num3++)); do

  #timestep=${time_array[num3]}
  # Run ANSYS section of code
  #python /path/to/my/AT_write.py $timestep # likely unecessary -- use echo instead 
  #touch ansys_time.txt
  #echo "$timestep" >> ansys_time.txt   
  #./path/to/my/runwb2 -B -R /path/to/my/nanopaticle_workbench.wbpj
  #rm ansys_time.txt 

#done

# generate plots fom each set of timeseries data -- maybe run this in a seperate bash script
#python /path/to/my/conductivity_plot.py


