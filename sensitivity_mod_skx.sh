#!/bin/bash

#----------------------------------------------------
# Example SLURM job script to run OpenMP applications
# on TACC's Stampede2 system.
#----------------------------------------------------
#SBATCH -J ansys_pylaunch                              # Job name
#SBATCH -o ansys_pylaunch.out                          # Name of stdout output file(%j expands to jobId)
#SBATCH -p skx-normal                                           # Submit to the 'normal' or 'development' queue
#SBATCH -N 1                                    # Total number of nodes requested
#SBATCH -n 40                                   # Total number of mpi tasks requested
#SBATCH -t 09:00:00                                     # Run time (hh:mm:ss)
#SBATCH -A Modeling-of-Microsca         # default account
#SBATCH --mail-user=joshgrose@utexas.edu        # email address to use
#SBATCH --mail-type=begin                                       # email me when the job starts

#

# paticle face mesh 1, air_face_mesh 2 
mesh_array_1=("2.28E-6")  #("15.8E-6"  "10.5E-6"  "7E-6") # "4.7E-6" "3.6E-6" "3.1E-6") # currently "index 4.5"
mesh_array_2=("1.33E-6")  #("9E-6" "6E-6" "4E-6" ) #"2.7E-6" "2.09E-6" "1.8E-6") # currently "index 4.5"
mesh_array_3=(0 0)

# BOI mesh
#mesh_array_1=("18E-6"  "12E-6"  "8E-6") # "5.3E-6" "3.6E-6")
#mesh_array_2=(0 0 0)
#mesh_array_3=(0 0 0)

# Prox Meshing


index_array=(6) #(1 2 3) # need to be swapped for higher numbers on next run to prevent overwriting of results files
mesh_type=1 # 1 for face sizing, 2 for BOI sizing, 3 for proximity sizing
timenum=2 # choose which timestep to perform the analysis on
module load qt5

source /work/07329/joshg/stampede2/software/conda/miniconda2/etc/profile.d/conda.sh
conda activate empty
vncserver :10
export DISPLAY=:10
#export OMP_NUM_THREADS=48

# run ansys scripts for all timesteps
TT=1 #3
for ((num=0;num<TT;num++)); do
  start=$((num * 20)) #14 for running 3 at a time
  end=$((start + 19)) #13

  index=${index_array[num]}
  mesh_size_1=${mesh_array_1[num]}
  mesh_size_2=${mesh_array_2[num]}
  #echo $start
  #echo $end

  folder_name='/work/07329/joshg/stampede2/simulations/ParticleModel/sensitivity/mesh_results/meshResult_timestep'"$timenum"'_final'
  folder_name="$folder_name"

  mechanical_name='nanoparticle_sim_final_'"$index"'.js' #    '/work/07329/joshg/stampede2/simulations/ParticleModel/sensitivity/ansys_scripts/nanoparticle_sim_final_'"$index"'.js'
  mechanical_name="$mechanical_name"
  export_name='temp_export_'"$index"'.js' #  '/work/07329/joshg/stampede2/simulations/ParticleModel/sensitivity/ansys_scripts/temp_export_'"$index"'.js'
  export_name="$export_name"
  wbpj_name='nanoparticle_workbench_final_'"$index"'.wbjn' #    '/work/07329/joshg/stampede2/simulations/ParticleModel/sensitivity/ansys_scripts/nanoparticle_sim_final_'"$in$  mechanical_name="$mechanical_name"
  wbpj_name="$wbpj_name"


  cp /work/07329/joshg/stampede2/simulations/ParticleModel/sensitivity/ansys_scripts/nanoparticle_workbench_final.wbjn "$folder_name"
  cp /work/07329/joshg/stampede2/simulations/ParticleModel/sensitivity/ansys_scripts/nanoparticle_sim_final.js "$folder_name"
  cp /work/07329/joshg/stampede2/simulations/ParticleModel/sensitivity/ansys_scripts/import_object_scaled_final.js "$folder_name"
  cp /work/07329/joshg/stampede2/simulations/ParticleModel/sensitivity/ansys_scripts/temp_export.js "$folder_name"
 
  cd "$folder_name"
  cp nanoparticle_sim_final.js "$mechanical_name"
  cp temp_export.js "$export_name"
  cp nanoparticle_workbench_final.wbjn "$wbpj_name"

  rm '/work/07329/joshg/stampede2/simulations/ParticleModel/sensitivity/mesh_results/meshResult_timestep'"$timenum"'_final/option.txt'  
  touch '/work/07329/joshg/stampede2/simulations/ParticleModel/sensitivity/mesh_results/meshResult_timestep'"$timenum"'_final/option.txt'
  echo $timenum >> '/work/07329/joshg/stampede2/simulations/ParticleModel/sensitivity/mesh_results/meshResult_timestep'"$timenum"'_final/option.txt'
  echo $index >> '/work/07329/joshg/stampede2/simulations/ParticleModel/sensitivity/mesh_results/meshResult_timestep'"$timenum"'_final/option.txt'

  python /work/07329/joshg/stampede2/simulations/ParticleModel/sensitivity/text_swap_geom_mesh.py $timenum
  python /work/07329/joshg/stampede2/simulations/ParticleModel/sensitivity/text_swap_mech_mesh.py $timenum $mesh_type $mesh_size_1 $mesh_size_2 $index
  #python /work/07329/joshg/stampede2/simulations/ParticleModel/sensitivity/text_swap_export_mesh.py $timenum
  python /work/07329/joshg/stampede2/simulations/ParticleModel/sensitivity/text_swap_wbjn_mesh.py $timenum $index

  export timenum  # source? # include other script??
  #echo "THIS SHOULD ONLY APPEAR TWICE"
  #ibrun -n 12 -o  $offset task_affinity ./ansys_batch.sh &  #input1 &   # 64 tasks; offset by  0 entries in hostfile.
  
  echo "THIS SHOULD ONLY APPEAR TWICE"
  
  cd /scratch/07329/joshg/ansys/
  time=$timenum
  rm_str1='.temp'"$time"'_'"$index"'_files.backup'
  rm_str2='temp'"$time"'_'"$index"'_files'
  rm_str3='temp'"$time"'_'"$index"'.wbpj'
  rm -r "$rm_str1"
  rm -r "$rm_str2"
  rm -r "$rm_str3"
  rm -r _ProjectScratch
  # cd /home1/apps/ANSYS/v201/Framework/bin/Linux64/

  #vncserver -geometry 1920x1080 :10
  #export DISPLAY=:10

  module load ansys
  module load qt5
  unset SLURM_GTIDS
  ansys_fol='/work/07329/joshg/stampede2/simulations/ParticleModel/sensitivity/mesh_results/meshResult_timestep'"$timenum"'_final' #workbench journal location
  cd "$ansys_fol"
  #ibrun -n 5 -o  $offset task_affinity /home1/apps/ANSYS/v201/Framework/bin/Linux64/runwb2 -R nanoparticle_workbench_final.wbjn &
  #numactl -C $start-$end  /home1/apps/ANSYS/v201/Framework/bin/Linux64/runwb2 -R nanoparticle_workbench_final.wbjn &    #"$ansys_fol"
  #numactl -C 4-27  /home1/apps/ANSYS/v201/Framework/bin/Linux64/runwb2 -R nanoparticle_workbench_final.wbjn &
  #/home1/apps/ANSYS/v201/Framework/bin/Linux64/runwb2 -I -R nanoparticle_workbench_final.wbjn &
  
  /home1/apps/ANSYS/v201/Framework/bin/Linux64/runwb2 -I -R "$wbpj_name" &

  #/home1/apps/ANSYS/v201/Framework/bin/Linux64/runwb2 -I -R nanoparticle_workbench_slice.wbjn
  # -B -R
  #./ansys_batch.sh &
  sleep 60
done
wait

vncserver -kill :10

echo "ANSYS done..."

echo "Parallelized"
