import pandas
import csv
import matplotlib.pyplot as plt

# set the key (eventually make this a function input
method = 1
key_list = ["Particle", "Original", "Full"]
key = key_list[method-1]

# Heat Transfer Parameters
q_flux = 1E10

# Calculate Area Ratio (HF Area/ Total Area)

timeseries = [0, 2, 4, 6, 8, 10, 20, 40, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 200, 400, 800, 1000, 1400, 2000, 2400, 3000, 3400, 4000]

# list of names dependant on the type of analysis being performed 
batch_list = ["FN1200","FN2400","FN3600","FN4800"]

for batch_name in batch_list:

    k_array = []

    save_string = '/home/joshua/Downloads/kPlots/conductivity_file_' + batch_name + '.csv'

    with open(save_string, 'w') as file_1:
        writer = csv.writer(file_1, delimiter = '\t',lineterminator='\n',)

        for time in timeseries:

            length_string = '/home/joshua/Downloads/particle_set_' + str(time) + '_newbed/part_bound.txt'

            with open(length_string) as length_file:
                bound_list = list(csv.reader(length_file))

            x_low = float(bound_list[0][0])
            x_high = float(bound_list[1][0])
            L = (x_high - x_low)/1000


            #L = 9E-7 #.077 for 4080 original cut depths #.08 for case 400 #.09 for case 0
            results_string = '/home/joshua/Downloads/Timestep' + str(time) + 'SmoothResults/'
            wb_string = results_string + 'ANSYS_table_export.csv'
            complete_result_string = results_string + 'Temperature_Results.txt'
            particle_faces_hot_string = results_string + 'Temperature_Results_Particle_Faces_Hot'
            particle_faces_cold_string = results_string + 'Temperature_Results_Particle_Faces_Cold'
            hot_full_string = results_string + 'Temperature_Results_Hot'
            cold_full_string = results_string + 'Temperature_Results_Cold'


            vr_string = '/home/joshua/Downloads/particle_set_' + str(time) + '_newbed/volume_ratio.txt'


            with open(vr_string) as vr_file:
                VR_list = list(csv.reader(vr_file))
            VF = float(VR_list[0][0])

            with open(wb_string) as temp_csv:
                data = list(csv.reader(temp_csv))

            # get ratio of heat flux area to total area
            A_HF = float(data[7][3]) 
            A_T = float(data[7][4])
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

                df_hot = pandas.read_csv(particle_faces_hot_string, sep='\t')
                df_cold = pandas.read_csv(particle_faces_cold_string, sep='\t')
                temp_avg_hot = df_hot.iloc[:,4].mean()
                temp_avg_cold = df_cold.iloc[:,4].mean()

            elif key == "Full":

                df_hot = pandas.read_csv(hot_full_string, sep='\t')
                df_cold = pandas.read_csv(cold_full_string, sep='\t')
                temp_avg_hot = df_hot.iloc[:,4].mean()
                temp_avg_cold = df_cold.iloc[:,4].mean()
    
            # solve for Thermal Conductivity (k)
            k = q_flux*AR*(L)/(temp_avg_hot - temp_avg_cold)
            k_array.append(k)
            k = [k]
      
            writer.writerow(k)

    file_1.close()

    title_string = 'conductivity_plot_' + batch_name + '.png'
    plot_string = '/home/joshua/Downloads/kPlots/' + title_string

    plt.plot(timeseries, k_array, 'ro')
    plt.title(title_string)
    plt.ylabel('Thermal Conductivity (W/m*K)')
    plt.xlabel('Time')    
    plt.savefig(plot_string)
    #plt.show()
