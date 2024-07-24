import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

def read_and_plot_ftir(folder_path):
    # Search for all CSV files in the specified directory
    file_paths = glob.glob(os.path.join(folder_path, '*.csv'))
    
    # Set up the plot
    plt.figure(figsize=(10, 8))
    
    # Loop through each file
    for file_path in file_paths:
        # Read the CSV file
        data = pd.read_csv(file_path, skiprows=1)
        
        name = file_path.split("/")[-1].strip(".csv")
        # Plotting
        plt.plot(data['cm-1'], data['%T'], label=name, linewidth=2)
    
    # Setting the labels and title
    peak_dict = {
                'C=O stretching': (1650,),
                'N-H stretching, C-N bending': (1540,),
                'C-H bending': (1400,1450),
                'C-N stretching, N-H bending': (1240,)
            }



    i =0
    inc = 0.2
    for label, peak in peak_dict.items():
        i = i+1
        if len(peak)==1:
            plt.axvline(peak, linewidth=2, label=label, alpha=0.9, color=(1-inc*i, inc*i, inc*i))
        else:
            plt.axvspan(peak[0], peak[-1], label=label, alpha=0.5, color=(1-inc*i, inc*i, inc*i))
    plt.xlim(1700,1100)
    plt.ylim(50,150)
    plt.xlabel('Wavenumber (cm-1)', fontsize=24)
    plt.ylabel('Transmittance (%)', fontsize=24)
    plt.title('FTIR Spectra', fontsize=24)
    plt.xticks(fontsize=22)
    plt.yticks(fontsize=22)
    plt.legend(fontsize=18)
    plt.gca().invert_xaxis()  # Inverting the x-axis for conventional FTIR display
    plt.show()

# Replace 'path_to_your_folder' with the path to your folder containing the CSV files
read_and_plot_ftir(os.getcwd())

