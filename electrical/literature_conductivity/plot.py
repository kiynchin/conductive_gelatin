import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Data setup
#compositions = ["GE-AgNWs", "Gel/AS", "GO/GelMA", "GelDA/GO", "CG-C"]
compositions = ["Jing 2019", "Liu 2020", "Park 2020", "Han 2021", "This work"] 
conductivities = [0.1, 0.05, 0.0087, 0.017, 3110]  # Converting 3.11E+03 S/cm to 3110
types = [0, 0, 0, 0, 1]  # Indicator for the type of conductivity
colors = ['gray' if t == 0 else 'green' for t in types]

# Setup figure and axes for the plot with a break in y-axis
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(12,6))
fig.subplots_adjust(hspace=0.05)  # Adjust space between the subplots

# Define breaks
break_start = 0.14
break_end = 2000

# Set limits for the upper and lower plots
ax2.set_ylim(0, break_start)
ax1.set_ylim(break_end, 3200)  # Adjust upper limit to accommodate tall bar

# Create bars in both subplots
bars1 = ax1.bar(compositions, conductivities, color=colors)
bars2 = ax2.bar(compositions, conductivities, color=colors)

# Diagonal lines on the breaks
d = .005  # length of diagonal slashes
doff = 1
kwargs = dict(color='gray', clip_on=False)
ax1.plot((-d, +d), (-d, +d), transform=ax1.transAxes, **kwargs)  # top-left diagonal
ax1.plot((doff - d, doff + d), (-d, +d), transform=ax1.transAxes, **kwargs)  # top-right diagonal
kwargs.update(transform=ax2.transAxes)  # switch to the bottom axes
ax2.plot((-d, +d), (doff - d, doff + d), **kwargs)  # bottom-left diagonal
ax2.plot((doff - d, doff + d), (doff - d, doff + d), **kwargs)  # bottom-right diagonal

ax1.spines['bottom'].set_visible(False)
ax2.spines['top'].set_visible(False)

# Formatting axes
ax1.xaxis.set_visible(False)
ax2.xaxis.set_visible(True)

# Labels, title, and tick customization
fig.text(0.04, 0.5, 'Conductivity (S/cm)', va='center', ha='center', rotation='vertical', fontsize=24)
#fig.suptitle('Conductivity vs. Literature', fontsize=24, y=0.95)

plt.xticks(fontsize=24)
ax1.tick_params(axis='y', labelsize=24)
ax2.tick_params(axis='y', labelsize=24)

# Saving figure with adjusted bounding box to include the entire bar within the figure
plt.savefig("literature_conductivity_with_break.pdf", bbox_inches='tight')
plt.show()

