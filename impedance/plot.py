import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
from matplotlib.ticker import FormatStrFormatter


sample = int(sys.argv[1])
# Specify the directory path
directory_path = f'data/electrode{sample}_impedance'

# Get a list of all .txt files in the directory
txt_files = [file for file in os.listdir(directory_path) if file.endswith('.txt')]

# Choose one .txt file to read the first column from
first_txt_file = txt_files[0] if txt_files else None

# Initialize an empty list to store data from the second column of each CSV file
data = []

# Read the first column from the chosen .txt file, skipping the first two rows
if first_txt_file:
    txt_path = os.path.join(directory_path, first_txt_file)
    with open(txt_path, 'r') as txt_f:
        lines = txt_f.readlines()[2:-1]  # Skip the first two rows
        first_column = [float(line.strip().split('\t')[0]) for line in lines]  # Convert to float
        print(len(first_column))

    # Create a dictionary with the 'Frequency' column and data from .csv files
    data_dict = {'Frequency': first_column}
    print(len(data_dict['Frequency']))

    for txt_file in txt_files:
        txt_path = os.path.join(directory_path, txt_file)
        df = pd.read_csv(txt_path, sep='\t', skiprows=1, skipfooter=1, usecols=[1], dtype={'Column1': float})  # Read only the second column
        print(len(df))
        column_name = os.path.splitext(txt_file)[0]  # Extract the filename without extension
        data_dict[column_name] = df.iloc[:, 0]  # Store the column as a Series in the dictionary

    # Create a pandas DataFrame from the dictionary
    df = pd.DataFrame(data_dict)

    # Sort the columns (except for the first one) in alphabetical order
    sorted_columns = ['Frequency'] + sorted(df.columns[1:])
    df = df[sorted_columns]
    
    # Get the mean and standard deviation values
    df['mean'] = df.iloc[:, 1:].mean(axis=1)
    df['std dev'] = df.iloc[:, 1:].std(axis=1)

    # Print the resulting DataFrame
    # print(df
    
    # Save the resulting DataFrame as a CSV file
    output_csv_name = 'combined_data.csv'  # input("Enter the desired CSV file name (including .csv extension): ")
    output_csv_path = os.path.join(directory_path, output_csv_name)

    df.to_csv(output_csv_path, index=False)  # Set index=False to exclude index column

    # Plot results
    fig1, ax1 = plt.subplots(figsize=(9, 6))
    # ax1.plot(df['Frequency'], df.drop(['Frequency', 'mean', 'std dev'], axis=1), '^', label='Clinical Grade')
    ax1.plot(df['Frequency'], df['mean'], 'o', label='Mean')
    upper_bound = df['mean'] + df['std dev']
    lower_bound = df['mean'] - df['std dev']

    # Create the shaded area
    ax1.fill_between(df['Frequency'], lower_bound, upper_bound, color='gray', alpha=0.5, label='Standard Deviation')
    ax1.legend(prop={'size': 24}, markerscale=2, loc='upper right')
    for axis in ['top', 'bottom', 'left', 'right']:
        ax1.spines[axis].set_linewidth(1)

    plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    ax1.yaxis.get_offset_text().set_fontsize(24)
    plt.xscale('log')
    plt.yticks(fontsize=24)
    plt.xticks(fontsize=24)
    plt.ylabel('Impedance Amplitude ($\Omega$)', fontsize=24)
    plt.xlabel('Frequency (Hz)', fontsize=24)

    # Use LogFormatterSciNotation for scientific notation on the y-axis


    plt.title(f'Skin-electrode interface impedance', fontsize=24)
    ax1.tick_params(axis='both', which='major', labelsize=24)
    ax1.tick_params(axis='both', which='minor', labelsize=24)
    plt.savefig(f"electrode{sample}_impedance.pdf")

    plt.show()

else:
    print("No .txt files found in the directory.")
