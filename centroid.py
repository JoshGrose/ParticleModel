import csv
import numpy as np

part_number = 16
#def get_centroid(part_number):
mult = 1.1
scale = mult*.01058/1000.0
max_dist = []

time = 8

folder_str = '/home/joshua/Downloads/particle_set_' + str(time) + '_newbed/radii_file.txt' 

with open(folder_str, 'w') as file_1:
    writer = csv.writer(file_1, delimiter = '\n',lineterminator='\n',)

    for num in range(part_number):
        dist_arr = []
        xyz_string = '/home/joshua/simulations/scale/intermediate/point_cloud_part_' + str(num) + '.xyz'
        xyz_array = np.loadtxt(xyz_string).astype(float)
        col_avg_array = np.mean(xyz_array, axis=0)
    
        for point in xyz_array:
            dist = ((col_avg_array[0]-point[0])**2.0 + (col_avg_array[1]-point[1])**2.0 + (col_avg_array[2]-point[2])**2.0)**(0.50)
            dist_arr.append(dist) 
    
        max_dist.append(max(dist_arr)*scale)

    radii = max_dist
    writer.writerow(radii)
    file_1.close()
    # print radii
