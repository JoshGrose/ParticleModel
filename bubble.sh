#!/bin/bash

part_number=18
time=4
mult_small=.88
mult_large=1.04

python sphere.py $part_number $time $mult_large
python small_sphere.py $part_number $time $mult_small
python hollow_sphere.py $part_number $time
python bubble_hollow.py $part_number $time

