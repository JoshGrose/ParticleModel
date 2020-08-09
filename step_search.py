# -*- coding: UTF-8 -*-
import re
import sys

folder_name = str(sys.argv[1])

air_path = folder_name + "/AirBlock.step"
f  = open(air_path,"r")

step_file = f.read()

pattern = "translator 6.8 .\..\.."

num_occ = len(re.findall(pattern, step_file))/2

if num_occ == 0:
    num_occ = 1

num_occ = str(num_occ)

output_path = folder_name + "/air_pieces.txt"
fw = open(output_path,"w+")
fw.write(num_occ)

f.close()
fw.close()
