import pandas as pd
import matplotlib.pyplot as plt
import re
import seaborn as sns
from matplotlib.ticker import FormatStrFormatter


# Read the CSV file
df = pd.read_csv('85C_hmwg.csv')

# Process 'Sample' column to extract minutes and trial number
df[['Sedimentation Time Extracted', 'Trial']] = df['Sample'].str.extract('H(\d+)-(\d)')
df['Sedimentation Time Extracted'] = pd.to_numeric(df['Sedimentation Time Extracted'], errors='coerce')
df['Trial'] = pd.to_numeric(df['Trial'], errors='coerce')
# Filter the dataframe for samples with valid sedimentation times and trials
valid_samples_df = df.dropna(subset=['Sedimentation Time Extracted', 'Trial'])

# Box and whisker plot
plt.figure(figsize=(8, 7))

plt.rcParams.update({'font.size': 22})
sns.boxplot(width=0.4, linewidth=2, x='Sedimentation Time Extracted', y='Lead-adjusted conductivity (mm)', data=valid_samples_df)
#plt.bar(valid_samples_df['Sedimentation Time Extracted'], valid_samples_df['Lead-adjusted conductivity (mm)'])
#plt.title('Conductivity vs. Sedimentation Time', fontsize=24)
plt.xlabel('Sedimentation Time (min)', fontsize=24)
plt.ylabel('Conductivity (S/cm)', fontsize=24)
#plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%d'))  # Two decimal places
plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
plt.gca().yaxis.get_offset_text().set_fontsize(18)  
plt.savefig('sedimentation_conductivity.pdf')
# Filter samples with sedimentation time < 60 and calculate average conductivity
avg_cond_df = df[df['Sedimentation Time Extracted'] >= 60].groupby('Sample')['Average Conductivity'].mean().reset_index()
plt.show()

# Plot
plt.figure(figsize=(10, 6))
plt.bar(avg_cond_df['Sample'], avg_cond_df['Average Conductivity'], color='skyblue')
plt.title('Average Conductivity for Samples with Sedimentation Time ≥ 60')
plt.xlabel('Sample')
plt.ylabel('Average Conductivity (S/cm)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('average_conductivity.pdf')

