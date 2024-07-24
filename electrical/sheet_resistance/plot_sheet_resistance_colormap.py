import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import matplotlib.cm as cm

def plot_gradient_graph_from_csv(file_path):
    df = pd.read_csv(file_path, skiprows=2)
    points_split = df['Points'].str.split(',', expand=True)
    df['Start'] = points_split[0].astype(int)
    df['End'] = points_split[1].astype(int)
    df['Resistance (Ohm)'] = df['Resistance (Ohm)'].astype(float)

    points_coordinates = {
        1: (0, 0), 2: (1, 0), 3: (2, 0),
        4: (0, -1), 5: (1, -1), 6: (2, -1),
        7: (0, -2), 8: (1, -2), 9: (2, -2),
    }

    min_resistance = df['Resistance (Ohm)'][df['Resistance (Ohm)'] > 0].min()
    max_resistance = df['Resistance (Ohm)'].max()

    # Normalize the resistance values to [0, 1] for color mapping
    norm = mcolors.Normalize(vmin=0, vmax=2)
    scalar_map = cm.ScalarMappable(norm=norm, cmap='viridis')  # Use a red-yellow-green colormap

    fig, ax = plt.subplots(figsize=(7.5,7.5))
    ax.set_xlim(-0.1, 2.1)
    ax.set_ylim(-2.1, 0.1)
    ax.set_aspect('equal')
    ax.axis('off')

    for _, row in df.iterrows():
        if row['Resistance (Ohm)'] > 0:
            start_coord = points_coordinates[row['Start']]
            end_coord = points_coordinates[row['End']]
            color = scalar_map.to_rgba(row['Resistance (Ohm)'])
            ax.plot([start_coord[0], end_coord[0]], [start_coord[1], end_coord[1]], color=color, linewidth=8, zorder=1)

    # Adding points as black dots
    for x, y in points_coordinates.values():
        ax.scatter(x, y, s=700, c='k', zorder=2, alpha=0.9)

    # Adding labels for points
    for point, (x, y) in points_coordinates.items():
        ax.text(x, y-0.01, f'{point}', color='white', ha='center', va='center', fontsize=24, zorder=3)

    # Add a colorbar to the figure to show the resistance scale
    scalar_map.set_array([])
    cbar=fig.colorbar(scalar_map, ax=ax, orientation='vertical', label='Resistance (Ohm)')
    cbar.ax.tick_params(labelsize=18)
    cbar.set_label("Resistance ($\Omega$)",fontsize=24)

    sample = os.path.splitext(file_path)[0]
    plt.title(f"{sample} Sheet Connectivity", fontsize=24)

    plt.savefig(f"{sample}_gradient_graph.png")
    plt.close()

csv_files = [f for f in os.listdir(os.getcwd()) if f.endswith('.csv')]

for csv_file in csv_files:
    plot_gradient_graph_from_csv(csv_file)

