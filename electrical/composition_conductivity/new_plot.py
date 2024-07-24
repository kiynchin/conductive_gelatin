import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
data = pd.DataFrame({"Sample": ["PG-C", "CG-C", "GG-C"],
"raw_mean": [2.71E3, 3.73E3, 9.36E2], "raw_std": [6.83E2, 7.08E2, 1.84E2],
"adjusted_mean": [5.2E3, 6.74E3, 1.14E3], "adjusted_std": [1.73E3, 2.06E3, 2.98E2]})
plt.rcParams.update({'font.size': 16})


# Plotting
#plt.figure(figsize=(10, 6))
#plt.bar(data['Sample'], data['raw_mean'], yerr=data['raw_std'], capsize=4, color='teal')
#plt.bar(data['Sample'], data['adjusted_mean'], yerr= data['adjusted_std'], capsize=4, color='green')
plt.figure(figsize=(10, 6))
bar_width = 0.35
index = np.arange(len(data['Sample']))
bar1 = plt.bar(index, data['raw_mean'], bar_width, yerr=data['raw_std'], capsize=4, color='teal', label='Raw')
bar2 = plt.bar(index + bar_width, data['adjusted_mean'], bar_width, yerr=data['adjusted_std'], capsize=4, color='green', label='Adjusted')
plt.xticks(index + bar_width / 2, data['Sample'], fontsize=20)
plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
plt.title("Conductivity vs. Composition",fontsize=30)
plt.legend()
#plt.xlabel("Gelatin Composition", fontsize=30)
plt.ylabel("Conductivity (S/cm)",fontsize=30)

plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
plt.gca().yaxis.get_offset_text().set_fontsize(20)  # Adjusting the font size for scientific notation scale marker

plt.xticks(rotation=0, fontsize=20)  # Rotate x-tick labels for better visibility if needed
plt.yticks(fontsize=20)
#plt.grid(axis='y')
plt.tight_layout()  # Adjust layout to make room for the rotated x-tick labels
plt.savefig("new_composition_conductivity.pdf")
plt.show()

