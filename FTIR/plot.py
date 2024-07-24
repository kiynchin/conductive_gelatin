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
        
        # Plotting
        plt.plot(data['cm-1'], data['%T'], label=os.path.basename(file_path))
    
    # Setting the labels and title
    plt.xlabel('Wavenumber (cm-1)', fontsize=20)
    plt.ylabel('Transmittance (%)', fontsize=20)
    plt.title('FTIR Spectra', fontsize=22)
    plt.legend(fontsize=18)
    plt.gca().invert_xaxis()  # Inverting the x-axis for conventional FTIR display
    plt.show()

# Replace 'path_to_your_folder' with the path to your folder containing the CSV files
read_and_plot_ftir(os.getcwd())

