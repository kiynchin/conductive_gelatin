import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import sys
import numpy as np


def plot_curve(sample, cutoff, legend_visible, ax):
    plt.rcParams.update({'font.size': 30})
    sample_name = {'p': 'PG-C', 'h': 'CG-C', 'g': 'GG-C'}
    all_data = pd.read_csv(f"combined_data/{sample}_combined_data.csv")
    all_data.drop(all_data.tail(cutoff).index, inplace=True)
    all_data['Time'] = all_data.index * (1000/30)
    all_data['Time'] = (all_data['Time'] - all_data['Time'].min()) / (all_data['Time'].max() - all_data['Time'].min())
    

    all_data['Strain'] = all_data['Strain'].apply(lambda x : x *100)
    # Create the plot
    sns.lineplot(ax=ax, x='Strain', y='dR/r0', data=all_data, linewidth=2, sort=False, color='gray')
    sizes = 10*np.ones(len(all_data))

    scatter=sns.scatterplot(ax=ax, legend=legend_visible,data=all_data, x='Strain', y='dR/r0', s=200,  hue='Time', palette='crest', alpha=1)
    if legend_visible:
        handles, labels = scatter.get_legend_handles_labels()
        desired_handles = [handles[0],handles[int(len(handles)/2.1)],handles[-1]]
        desired_labels = [labels[0], labels[int(len(labels)/2.1)],labels[-1]]
        formatted_labels = [f"{float(label)*100:.0f}%" for label in desired_labels]  # Format and round labels
  
        scatter.legend(desired_handles, formatted_labels, labelspacing=0.1,frameon=False, alignment='left', title="Time Progression", title_fontsize=28, loc="upper left", handlelength=0.1, fontsize=28, markerscale=1)
 #all_data.plot(x='Strain', y='dR/r0', kind='line', ax=plt.gca())

    # Customize the plot
    specimen, number = sample[0], sample[1]
    limits = {"p":(-0.5,4.5), "h":(-1,9), "g":(-1,40)}
    ax.set_ylim(limits[specimen])
    #plt.title(f'$\Delta R / R_0$ vs. Strain ({sample_name[specimen]}{number})', fontsize=22)
    ax.set_title(f'{sample_name[specimen]}', fontsize=28)
    ax.set_xlabel('Strain (%)', fontsize=28)
    ax.set_ylabel('$\Delta R / R_0 $', fontsize=28)
    ax.tick_params(labelsize=28)


    
    #plt.ylim((-1,50))
    # Show the plot

param_list = [
        ("g1", 100, True),#131 #91
        ("g2", 80, False),#111 #71
        ("g3", 147, False),#171 #141
        ("h1", 3, False),
        ("h2", 0, False),
        ("h3", 0, False),
        ("p1", 1, False),
        ("p2", 3, False),
        ("p3", 3, False)]

#fig, axes = plt.subplots(3,3, figsize = (25,13.5))

param_list = [
        ("g3", 147, True),
        ("h3", 0, False),
        ("p3", 3, False)]
fig,axes = plt.subplots(1,3, figsize = (25, 7))

axes = axes.flatten()
for ax, params in zip(axes,param_list):
    plot_curve(*params, ax=ax)
    plt.suptitle("Electromechanical Coupling", fontsize=28)


plt.tight_layout()
fig.savefig("final_graphs/electromechanical_response_grid.pdf", bbox_inches='tight')
plt.show()
