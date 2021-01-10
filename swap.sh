#!/bin/bash

time=2 
mesh_type_1=1 
mesh_size_1="15.8E-6"
mesh_size_2="10.5E-6"
index=1

python text_swap_mech_mesh.py $time $mesh_type_1 $mesh_size_1 $mesh_size_2 $index
