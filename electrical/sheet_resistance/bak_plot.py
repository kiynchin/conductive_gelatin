import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

def plot_gradient_graph_from_csv(file_path):
    # Read the CSV file, skipping the first two rows
    df = pd.read_csv(file_path, skiprows=2)
    # Split the 'Points' column into 'Start' and 'End', converting to integers
    points_split = df['Points'].str.split(',', expand=True)
    df['Start'] = points_split[0].astype(int)
    df['End'] = points_split[1].astype(int)
    df['Resistance (Ohm)'] = df['Resistance (Ohm)'].astype(float)

    # Define the coordinates for each point in the 3x3 grid
    points_coordinates = {
        1: (0, 0), 2: (1, 0), 3: (2, 0),
        4: (0, -1), 5: (1, -1), 6: (2, -1),
        7: (0, -2), 8: (1, -2), 9: (2, -2),
    }

    # Determine the range of nonzero resistances
    min_resistance = df['Resistance (Ohm)'][df['Resistance (Ohm)'] > 0].min()
    max_resistance = df['Resistance (Ohm)'].max()

    # Prepare a colormap
    norm = mcolors.Normalize(vmin=0.7, vmax=2)
    cmap = mcolors.LinearSegmentedColormap.from_list("", ["green", "blue"])

    fig, ax = plt.subplots()
    ax.set_xlim(-0.1, 2.1)
    ax.set_ylim(-2.1, 0.1)
    ax.set_aspect('equal')
    ax.axis('off')  # Hide axes
    ax.legend()

    for _, row in df.iterrows():
        if row['Resistance (Ohm)'] > 0:
            start_coord = points_coordinates[row['Start']]
            end_coord = points_coordinates[row['End']]
            color = cmap(norm(row['Resistance (Ohm)']))
            ax.plot([start_coord[0], end_coord[0]], [start_coord[1], end_coord[1]], color=color, linewidth=2)

    # Adding points as red dots
    for x, y in points_coordinates.values():
        ax.scatter(x, y, s=300, c='k')

    # Adding labels for points
    for point, (x, y) in points_coordinates.items():
        ax.text(x, y, f'{point}', color='white', ha='center', va='center', fontsize=14)

    plt.savefig(f"{os.path.splitext(file_path)[0]}_gradient_graph.png")
    plt.close()

# Get all CSV files in the current directory
csv_files = [f for f in os.listdir(os.getcwd()) if f.endswith('.csv')]

# Process each CSV file to generate and save a gradient graph
for csv_file in csv_files:
    plot_gradient_graph_from_csv(csv_file)

