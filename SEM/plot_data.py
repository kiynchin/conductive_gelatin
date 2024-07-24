import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator

data = [
    {'Sample': 'input_images/H00_0002.tiff', 'Silver thicknesses (um)': [0,0,0,0,0], 'Total thicknesses (um)': [424.41314426834776, 421.06322910812054, 418.5620579340574, 417.65351685838476, 415.6616005947118]},
    {'Sample': 'input_images/H20_0004.tiff', 'Silver thicknesses (um)': [90.86747783758379, 95.46194746893065, 97.14548676130529, 91.87923977722083, 84.98618186160786], 'Total thicknesses (um)': [431.43346139847785, 433.8408479065298, 434.98276477865363, 433.5607157556191, 431.6094774933443]},
    {'Sample': 'input_images/H40_0002.tiff', 'Silver thicknesses (um)': [96.13050357404494, 95.069854938072, 108.12611156742808, 102.98902088685077, 100.22612222138878], 'Total thicknesses (um)': [326.6746116459764, 336.3076391451691, 331.67439499622697, 328.904459045356, 334.63890418744035]},
    {'Sample': 'input_images/H60_0002.tiff', 'Silver thicknesses (um)': [137.25096304024711, 139.36162047538133, 135.25097611880008, 137.01109460977858, 134.90612522199655], 'Total thicknesses (um)': [437.4082644121537, 434.0259582364721, 431.6318102581011, 432.23261894374286, 432.9838580282676]}
]

#data = [{'Sample': 'input_images/G60_0001.tiff', 'Silver thicknesses (um)': [112.4042550663198, 117.5643937413896, 114.80538772934904, 114.07942821677631, 115.92907222617555], 'Total thicknesses (um)': [515.3170375627463, 516.7026282725782, 513.5534266585386, 515.2853150835327, 514.9213540307097]}, {'Sample': 'input_images/G600002.tiff', 'Silver thicknesses (um)': [107.87167349404034, 107.52050753619167, 94.37471173369354, 106.58911687072641, 105.92762897035485], 'Total thicknesses (um)': [548.9494057406531, 554.959321115406, 545.9386818817106, 549.5784208011111, 557.1095096873956]}, {'Sample': 'input_images/H600001.tiff', 'Silver thicknesses (um)': [129.28699613817693, 126.15884181103917, 126.8328467152552, 125.69553181768737, 130.26607797608509], 'Total thicknesses (um)': [424.46482828620447, 424.3500220599489, 423.3872818135807, 420.3821038893579, 419.8233363937468]}, {'Sample': 'input_images/pristinesheet_0009.tiff', 'Silver thicknesses (um)': [149.07893643077892, 149.02161047720708, 149.30097755067197, 148.60658535614655, 149.61699169990783], 'Total thicknesses (um)': [298.3628994941697, 297.8126080895226, 297.4637434283256, 298.068220333324, 298.2246894320106]}]


# Extract and process data, and generate all plots
times, silver_thickness_means, silver_thickness_stds, total_thickness_means, total_thickness_stds, ratio_means, ratio_stds = [], [], [], [], [], [], []
times = [0, 20, 40, 60]

for entry in data:
    silver_thickness = np.array(entry['Silver thicknesses (um)'])
    mean = np.mean(silver_thickness)
    std = np.std(silver_thickness)
    silver_thickness_means.append(mean)
    silver_thickness_stds.append(std)

    
    ratios = []
    total_thickness = np.array(entry['Total thicknesses (um)'])
    for silver, total in zip(silver_thickness, total_thickness):  
        ratio = silver/total
        ratios.append(ratio)
    
    ratio_mean = np.mean(ratios)
    ratio_std = np.std(ratios) 
    ratio_means.append(ratio_mean)
    ratio_stds.append(ratio_std)
    #print(entry['Sample'])
    #print(f"{mean} +/- {std}")
    #print(f"{ratio_mean} +/- {ratio_std}")
# Plotting with consolidated axes
plt.figure(figsize=(8, 4))
#fmt='o-',
# Silver thickness
plt.errorbar(times, np.array(silver_thickness_means), fmt="o-",linewidth=3.0, yerr=np.array(silver_thickness_stds),  label='Silver Thickness', capsize=10)
plt.xlabel('Sedimentation Time (minutes)', fontsize=24)
plt.ylabel('Conductive Layer\nThickness (um)', fontsize=24)
plt.tick_params(axis='y', labelsize=24)
plt.xticks([0,20,40,60])
#plt.yaxis.set_major_locator(MaxNLocator(5))
#ax1.set_title('Conductive Layer', fontsize=20)
plt.yticks(fontsize=24)
plt.xticks(fontsize=24)
plt.tight_layout()
plt.savefig("conductive_thickness.pdf")
plt.show()

plt.figure(figsize=(8, 4))
# Ratio of silver to total thickness

plt.errorbar(times, np.array(ratio_means), linewidth=3.0,fmt="o-", yerr=np.array(ratio_stds),  label='Proportion', capsize=10)
plt.ylabel('Conductive Layer\nThickness Ratio', fontsize=24)
plt.tick_params(axis='y')
plt.yticks([0, 0.1, 0.2, 0.3])
plt.yticks(fontsize=24)
plt.xticks([0,20,40,60])
plt.xticks(fontsize=24)
plt.xlabel('Sedimentation Time (minutes)', fontsize=24)
# Show the plot
plt.tight_layout()
plt.savefig("conductive_proportion.pdf")
plt.show()
