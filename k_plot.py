import matplotlib.pyplot as plt

def plot(title_string, plot_string, timeseries, k_array):

    plt.plot(timeseries, k_array, 'ro')
    plt.title(title_string)
    plt.ylabel('Thermal Conductivity (W/m*K)')
    plt.xlabel('Time')
    plt.savefig(plot_string)
    #plt.show()

