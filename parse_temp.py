import pandas
import csv

# set the key (eventually make this a function input
method = 1
key_list = ["Particle", "Original", "Full"]
key = key_list[method-1]

# Heat Transfer Parameters
q_flux = 1E10
L = 9E-7 #.077 for 4080 original cut depths #.08 for case 400 #.09 for case 0

# Calculate Area Ratio (HF Area/ Total Area)

with open('/home/joshua/Downloads/ANSYS_table_export.csv') as temp_csv:
    data = list(csv.reader(temp_csv))

#with open('/home/joshua/Downloads/ANSYS_table_export.csv') as temp_csv:
#    data = list(csv.reader(temp_csv))

# get ratio of heat flux area to total area
A_HF = float(data[7][3]) 
A_T = float(data[7][4])
AF = A_HF/A_T

# get volume fraction from part volumes
VF = .47 #.475 # eventually look in text vile for cumulative particle volume and total volume

# calvuate heat flux area ratio
AR = AF/VF

# Calculate Temperature Diff

if key == "Original":

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

    df_hot = pandas.read_csv('/home/joshua/Downloads/Temperature_Results_Particle_Faces_Hot', sep='\t')
    df_cold = pandas.read_csv('/home/joshua/Downloads/Temperature_Results_Particle_Faces_Cold', sep='\t')
    temp_avg_hot = df_hot.iloc[:,4].mean()
    temp_avg_cold = df_cold.iloc[:,4].mean()

elif key == "Full":

    df_hot = pandas.read_csv('/home/joshua/Downloads/Temperature_Results_Hot', sep='\t')
    df_cold = pandas.read_csv('/home/joshua/Downloads/Temperature_Results_Cold', sep='\t')
    temp_avg_hot = df_hot.iloc[:,4].mean()
    temp_avg_cold = df_cold.iloc[:,4].mean()
    
# solve for Thermal Conductivity (k)
k = q_flux*AR*(L)/(temp_avg_hot - temp_avg_cold)
print(k)
