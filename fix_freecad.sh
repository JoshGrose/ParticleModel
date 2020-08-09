#!/bin/bash

initial_part_number=21
#timestep=8 #2 #0 #7500 #2000  #400 #200 # -- numbers in the 1000's represent decimals -> 2000 = .2
time_array=(0 2 4 6 8 10 20 30 40 50 60 70 80 90 100 110 120 130 140 150 160 170 180 190 200 400 600 800 1000 1400 2000 2400 3000 3400 4000)
#time_array=(0 2)
NUMTIME=35
num_extra_files=7
OPTNUM=5
option_array=(900 1000 1200 1400 1600)  # subject to change

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
rho_cut=.01 #0.05
# partie contribution cutoff
eta_cut=.000001 #0.000005

# Location of stl and xyz files
stl_path='/home/joshua/simulations/scale/intermediate/'                                                                                      # PATH TO STL/XYZ FILES

# build georgina filenames
declare -a file_arr=()
declare -a fol_arr=()

for((i=0;i<OPTNUM;i++)); do
  
  option=${option_array[i]}
  mesh_fol='/home/joshua/simulations/scale/mewtwo_script_'"$option"'1200.mlx'

  for ((num=0;num<NUMTIME;num++)); do
    # create file and part names

    timestep=${time_array[num]}
    folder_name='/home/joshua/Downloads/particle_FULLset_'"$timestep"'_newbed'
    number=$(ls "$folder_name" | wc -l)
    num_array+=("$number")

    data_path='/home/joshua/simulations/scale/timeseries/fullT'"$timestep"'SN50400002.dat'
    part_number=`python /home/joshua/simulations/scale/part_number.py $data_path $initial_part_number $xsize $ysize $zsize $rho_cut $eta_cut` 
    part_number=$(($part_number + $num_extra_files))

    echo "$number"
    echo "$part_number"

    if ((file_number < part_number)); then

      timestep=${time_array[num]}
      data_path='/home/joshua/simulations/scale/timeseries/fullT'"$timestep"'SN50400002.dat'                                                     # PATH TO GEORGINA DATA FILES
      folder_name='/home/joshua/Downloads/particle_FULLset_'"$timestep"'_newbed'                                                                  # PATH TO FOLDER WHERE STEP FILES WILL BE SAVED
      rm -r "$folder_name" 
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
      for ((numo=0;numo<=PARTS;numo++));do
        snap run meshlab.meshlabserver -i ${xyz_names[numo]} -o ${stl_names[numo]} -s "$mesh_fol"  # rerun with alternate mesh settings
      done

      # run feeecad script to generate solid bodies and ontacts between partiles                                                                 # PATH TO PYTHON SCRIPTS (line below)
      python /home/joshua/simulations/scale/convert_scaled.py $folder_name $initial_part_number $part_number $data_path $stl_path $xsize $ysize $zsize $x_shift_h $x_shift_l $y_shift_h $y_shift_l $z_shift_l $rho_cut $eta_cut  < /dev/null

      # determine the number of pieces of air are contained in the air block step file
      python /home/joshua/simulations/scale/step_search.py $folder_name

    fi

  done

done
