import pandas as pd
import numpy as np
import sys

def calculate_strain(csv_path, output_path, sample):
    distances = {"p1":26.71,"p2":23.78, "p3":24.38,
            "h1":24.56,"h2":24.07, "h3":21.83,
            "g1":24.29, "g2":23.84, "g3":23.14}
    
    centroids = pd.read_csv(csv_path)
    rows = len(centroids)
    fps = 30
    strain_curve = np.empty((rows,2))
    ratio_known = False
    ratio = 1
    initial_distance_mm = distances[sample] 
    for index, row in centroids.iterrows():
        time = index/30
        pixel_distance = row["centroid_8_y"] - row["centroid_2_y"]
        if not ratio_known:
            ratio = initial_distance_mm / pixel_distance
            ratio_known = True
        distance_in_mm = pixel_distance * ratio

        strain_curve[index, :] = time, (distance_in_mm-initial_distance_mm)/initial_distance_mm
    np.savetxt(output_path, strain_curve, delimiter=",")

sample = sys.argv[1]
csv_path = f"centroid_trajectories/{sample}_centroids.csv"
output_path = f"strain_curves/{sample}_strain.csv"
calculate_strain(csv_path, output_path, sample)
