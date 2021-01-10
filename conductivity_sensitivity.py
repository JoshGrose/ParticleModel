import pandas
import csv

# set the key (eventually make this a function input
method = 1
key_list = ["Particle", "Original", "Full"]
key = key_list[method-1]

# Heat Transfer Parameters
q_flux = 1E10

mesh_type = "FaceSizing"

# Calculate Area Ratio (HF Area/ Total Area)

timeseries = [2] #[0, 2, 4, 6, 8, 10, 20, 40, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 200, 400, 800, 1000, 1400, 2000, 2400, 3000, 3400, 4000]
index_list = [4]  #[1, 2, 3, 4]
path_str = "/work/07329/joshg/stampede2/simulations/ParticleModel/sensitivity/mesh_results/"

with open('/work/07329/joshg/stampede2/simulations/ParticleModel/sensitivity/k_results/conductivity_file.csv', 'w') as file_1:
    writer = csv.writer(file_1, delimiter = '\t',lineterminator='\n',)

    for time in timeseries:
        writer.writerow(str(time))

        for index in index_list:
  
            filename = "TempResults_" + mesh_type + "_Index_" + str(index)
 
            full_path_str = path_str + "meshResult_timestep" + str(time) + "_final/"

            results_string = full_path_str          #+ "TempResults_FaceSizing_Index_" + str(index)

            length_string = full_path_str + "part_bound.txt"

            with open(length_string) as length_file:
                bound_list = list(csv.reader(length_file))

            x_low = float(bound_list[0][0])
            x_high = float(bound_list[1][0])
            L = (x_high - x_low)/1000


            #L = 9E-7 #.077 for 4080 original cut depths #.08 for case 400 #.09 for case 0
            #results_string = '/home/joshua/Downloads/Timestep' + str(time) + 'SmoothResults/'
            wb_string = results_string + 'ANSYS_table_export.csv'
            
            #complete_result_string = results_string + 'Temperature_Results.txt'
            particle_faces_hot_string = results_string + filename

            #particle_faces_cold_string = results_string + 'Temperature_Results_Particle_Faces_Cold'
            #hot_full_string = results_string + 'Temperature_Results_Hot'
            #cold_full_string = results_string + 'Temperature_Results_Cold'


            vr_string = results_string + "volume_ratio.txt"


            with open(vr_string) as vr_file:
                VR_list = list(csv.reader(vr_file))
                VF = float(VR_list[0][0])

            with open(wb_string) as temp_csv:
                data = list(csv.reader(temp_csv))

            # get ratio of heat flux area to total area
            A_HF = float(data[7][5]) 
            A_T = float(data[7][6])
            AF = A_HF/A_T
  
            # get volume fraction from part volumes
            # VF = .747 #.475 # eventually look in text vile for cumulative particle volume and total volume

            # calvuate heat flux area ratio
            AR = AF/VF
 
            # Calculate Temperature Diff

            if key == "Original": # currently broken

                AR = 1
                df = pandas.read_csv('/home/joshua/Downloads/Temperature_Results.txt', sep='\t')

                # get max temperature average
                upper=.055 # get these from bounds
                lower=.0077

                df = df[df['Z Location (m)'] <= upper]# and df['Z Location (m)'] >= lower]
                df = df[df['Z Location (m)'] >= lower]
                maximum = df[df['X Location (m)'] == df['X Location (m)'].max()]

                temp_avg_hot = maximum.iloc[:,4].mean()

                # get min temperature average
                minimum = df[df['X Location (m)'] == df['X Location (m)'].min()]

                temp_avg_cold = minimum.iloc[:,4].mean()

            elif key == "Particle":

                df_hot = pandas.read_csv(particle_faces_hot_string, sep='\t', encoding= 'unicode_escape')
                #df_cold = pandas.read_csv(particle_faces_cold_string, sep='\t')
                temp_avg_hot = df_hot.iloc[1:,1].mean()
                temp_avg_cold = 22 #df_cold.iloc[:,4].mean()
                print(temp_avg_hot)
                print(temp_avg_cold)

            elif key == "Full":

                df_hot = pandas.read_csv(hot_full_string, sep='\t')
                df_cold = pandas.read_csv(cold_full_string, sep='\t')
                temp_avg_hot = df_hot.iloc[:,4].mean()
                temp_avg_cold = df_cold.iloc[:,4].mean()
    
            # solve for Thermal Conductivity (k)
            k = q_flux*AR*(L)/(temp_avg_hot - temp_avg_cold)
            k = [k]
      
            write_string = "Index: " + str(index) + " -> k = " + str(k)

            writer.writerow(write_string)
            writer.writerow(k)

            print(k)
        
        #writer.writerow("\n")
