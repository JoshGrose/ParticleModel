# -*- coding: UTF-8 -*-
import re
import sys

time = str(sys.argv[1])

time = str
file_name = "W:\Timestep" + time + "bubble\dp0\SYS\MECH\file0.err" # Timestep8bubble would be the current filename

f  = open(file_name,"r")

err_file = f.read()

pattern = \*\*\*ERROR\*\*\*

num_occ = len(re.findall(pattern, err_file))/2

if num_occ >= 0:
    print 1
