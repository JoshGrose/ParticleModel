#!/bin/bash

part_number=4
time=400
mult_small=.88
mult_large=1.04

python /work/07329/joshg/stampede2/simulations/ParticleModel/sphere.py $part_number $time $mult_large
python /work/07329/joshg/stampede2/simulations/ParticleModel/small_sphere.py $part_number $time $mult_small
python /work/07329/joshg/stampede2/simulations/ParticleModel/hollow_sphere.py $part_number $time
python /work/07329/joshg/stampede2/simulations/ParticleModel/bubble_hollow.py $part_number $time

