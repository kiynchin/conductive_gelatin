import pandas as pd
import matplotlib.pyplot as plt
import os
label_dict = {"pristine": "PG", "hmwg":"CG", "g60":"GG", "conductive":"C", "nonconductive":"NC"}
# Initialize an empty DataFrame to hold all aggregated data
all_data = pd.DataFrame()
plt.rcParams.update({'font.size': 16})

# Loop through each file in the current directory
for filename in os.listdir('.'):
    if filename.endswith('.csv'):
        # Extract the sample name from the filename
        sample_name = filename.split('.')[0]
        
        # Read the CSV file
        temp_df = pd.read_csv(filename)
        
        # Add a column for the sample name extracted from the filename
        temp_df['Sample'] = f"{label_dict[sample_name]}-C"
        
        # Append the data to the all_data DataFrame
        all_data = pd.concat([all_data, temp_df], ignore_index=True)

# Group the data by 'Sample' and calculate mean and standard deviation of 'Lead Adjusted Conductivity (S/cm)'
aggregated_data = all_data.groupby('Sample')['Lead Adjusted Conductivity (S/cm)'].agg(['mean', 'std']).reset_index()
print(aggregated_data['mean'])
print(aggregated_data['std'])

# Plotting
plt.figure(figsize=(10, 6))
plt.bar(aggregated_data['Sample'], aggregated_data['mean'], yerr=aggregated_data['std'], capsize=4, color='teal')
plt.title("Conductivity vs. Composition",fontsize=30)
#plt.xlabel("Gelatin Composition", fontsize=30)
plt.ylabel("Conductivity (S/cm)",fontsize=30)

plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
plt.gca().yaxis.get_offset_text().set_fontsize(20)  # Adjusting the font size for scientific notation scale marker

plt.xticks(rotation=0, fontsize=20)  # Rotate x-tick labels for better visibility if needed
plt.yticks(fontsize=20)
#plt.grid(axis='y')
plt.tight_layout()  # Adjust layout to make room for the rotated x-tick labels
plt.savefig("composition_conductivity.pdf")
plt.show()

