#!/bin/bash

#
time_array=(50 200 2000) #4 6 8 10 20 30 40 50 60 70 80 90 100 110 120 130 140 150 160 170 180 190 200 400 600 800 1000 1400 2000 2400 3000 3400 4000)
module load qt5

#source /work/07329/joshg/stampede2/software/conda/miniconda2/etc/profile.d/conda.sh
#conda activate empty

#vncserver :10
#export DISPLAY=:10

# run freecad and meshlab scripts for all timesteps
#TT=1 # total time
#for ((num=0;num<TT;num++)); do
#  offset=$((num * 1))
#  timenum=${time_array[num]}

#  export timenum  # source? # include other script??
#  echo "THIS SHOULD ONLY APPEAR TWICE"
#  ibrun -n 1 -o  $offset task_affinity ./conduct.sh &  #input1 &   # 64 tasks; offset by  0 entries in hostfile.
#done
#wait

#echo "FreeCAD done..."

#conda deactivate
#conda deactivate
#source ~/.bashrc
#export PATH="/opt/apps/xalt/xalt/bin:/opt/apps/cmake/3.16.1/bin:/opt/apps/intel18/python2/2.7.15/bin:/opt/apps/autotools/1.1/bin:/opt/apps/git/2.24.1/bin:/opt/apps/libfabric/1.7.0/bin:/opt/apps/intel18/impi/18.0.2/bin:/opt/intel/compilers_and_libraries_2018.2.199/linux/mpi/intel64/bin:/opt/intel/compilers_and_libraries_2018.2.199/linux/bin/intel64:/opt/apps/gcc/6.3.0/bin:/usr/lib64/qt-3.3/bin:/usr/local/bin:/bin:/usr/bin:/opt/dell/srvadmin/bin:."
#source ./sourcefile.sh
#ansys_env

#export OMP_NUM_THREADS=48

# run ansys scripts for all timesteps
TT=3
for ((num=0;num<TT;num++)); do
  start=$((num * 14))
  end=$((start + 13))
  timenum=${time_array[num]}

  #echo $start
  #echo $end

  folder_name='/work/07329/joshg/stampede2/simulations/ParticleModel/results_mod/particle_FULLset4_'"$timenum"'_newbed'
  folder_name="$folder_name"
  cp /work/07329/joshg/stampede2/simulations/ParticleModel/ansys_scripts/nanoparticle_workbench_final.wbjn "$folder_name"
  cp /work/07329/joshg/stampede2/simulations/ParticleModel/ansys_scripts/nanoparticle_sim_final.js "$folder_name"
  cp /work/07329/joshg/stampede2/simulations/ParticleModel/ansys_scripts/import_object_scaled_final.js "$folder_name"
  cp /work/07329/joshg/stampede2/simulations/ParticleModel/ansys_scripts/temp_export.js "$folder_name"
  
  #cp /work/07329/joshg/stampede2/simulations/ParticleModel/ansys_scripts/nanoparticle_workbench_slice.wbjn "$folder_name"
  #cp /work/07329/joshg/stampede2/simulations/ParticleModel/ansys_scripts/import_object_scaled_slice.js "$folder_name"

  touch '/work/07329/joshg/stampede2/simulations/ParticleModel/results_mod/particle_FULLset4_'"$timenum"'_newbed/option.txt'
  echo $timenum >> '/work/07329/joshg/stampede2/simulations/ParticleModel/results_mod/particle_FULLset4_'"$timenum"'_newbed/option.txt'

  python /home1/07329/joshg/text_swap_geom_mod.py $timenum
  python /home1/07329/joshg/text_swap_mech_mod.py $timenum
  python /home1/07329/joshg/text_swap_export_mod.py $timenum
  python /home1/07329/joshg/text_swap_wbjn_mod.py $timenum
  #python /home1/07329/joshg/text_swap_slice.py $timenum
  #python /home1/07329/joshg/text_swap_geomSlice.py $timenum

  export timenum  # source? # include other script??
  #echo "THIS SHOULD ONLY APPEAR TWICE"
  #ibrun -n 12 -o  $offset task_affinity ./ansys_batch.sh &  #input1 &   # 64 tasks; offset by  0 entries in hostfile.
  
  echo "THIS SHOULD ONLY APPEAR TWICE"
  
  cd /scratch/07329/joshg/ansys/
  time=$timenum
  rm_str1='.temp'"$time"'_files.backup'
  rm_str2='temp'"$time"'_files'
  rm_str3='temp'"$time"'.wbpj'
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

  ansys_fol='/work/07329/joshg/stampede2/simulations/ParticleModel/results_mod/particle_FULLset4_'"$time"'_newbed/' #nanoparticle_workbench_final.wbjn'
  cd "$ansys_fol"
  #ibrun -n 5 -o  $offset task_affinity /home1/apps/ANSYS/v201/Framework/bin/Linux64/runwb2 -R nanoparticle_workbench_final.wbjn &
  #numactl -C $start-$end  /home1/apps/ANSYS/v201/Framework/bin/Linux64/runwb2 -R nanoparticle_workbench_final.wbjn &    #"$ansys_fol"
  #numactl -C 4-27  /home1/apps/ANSYS/v201/Framework/bin/Linux64/runwb2 -R nanoparticle_workbench_final.wbjn &
  /home1/apps/ANSYS/v201/Framework/bin/Linux64/runwb2 -I -R nanoparticle_workbench_final.wbjn &
  #/home1/apps/ANSYS/v201/Framework/bin/Linux64/runwb2 -I -R nanoparticle_workbench_slice.wbjn
  # -B -R
  #./ansys_batch.sh &
  sleep 4
done
wait

#vncserver -kill :10

echo "ANSYS done..."

echo "Parallelized"