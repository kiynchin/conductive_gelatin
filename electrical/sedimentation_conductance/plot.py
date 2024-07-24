import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd


plt.figure(figsize=(8,4))
data = pd.read_csv('data.csv')
print(data) 
 
plt.errorbar(data['Time'], data['Conductance'],linewidth=3.0, yerr=data['Standard Deviation'], capsize=10, fmt="o-")
plt.xlabel('Sedimentation Time (minutes)', fontsize=24)
plt.ylabel('Conductance (S)', fontsize=24)
plt.tick_params(axis='y', labelsize=24)
plt.xticks([0,20,40,60])
plt.yticks(fontsize=24)
plt.xticks(fontsize=24)
plt.savefig("conductance.pdf")
plt.show()	
