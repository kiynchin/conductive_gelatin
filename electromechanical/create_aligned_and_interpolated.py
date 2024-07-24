import numpy as np
import pandas as pd

alignment = {
        "p1": 13.47,
        "p2": 10.2,
        "p3": 5.97,
        "h1": 4.38,
        "h2": 4.07,
        "h3": 3.27,
        "g1": 4.5,
        "g2": 3.2,
        "g3": 4.59
        }

samples = ["p1", "p2", "p3", "h1", "h2", "h3", "g1", "g2", "g3"]

for sample in samples:
    strain_path = f"strain_curves/{sample}_strain.csv"
    resistance_path = f"resistance_curves/{sample}_resistance.txt"
    strain = pd.read_csv(strain_path, header=None)
    resistance = pd.read_csv(resistance_path, header=None)

    resistance[0] = resistance[0] - alignment[sample]
    resistance_aligned = resistance[resistance[0]>=0].reset_index(drop=True)

    resistance_last_time = resistance_aligned[0].iloc[-1]
    strain_last_time = strain[0].iloc[-1]
    resistance_cropped = resistance_aligned[resistance_aligned[0] <= strain_last_time]
    strain_cropped = strain[strain[0] <= resistance_last_time].reset_index(drop=True)

    time_points = np.array(resistance_cropped[0])
    interped_strain = np.interp(time_points, np.array(strain_cropped[0]), np.array(strain_cropped[1]))
    strain_interpolated = pd.DataFrame(np.column_stack((time_points,interped_strain)))
    r0 = resistance_cropped.loc[0,1]
    print(r0)
    print(resistance_cropped[1])
    resistance_normalized = pd.DataFrame({'Resistance':(resistance_cropped[1] - r0) / r0})
    all_data = pd.DataFrame({"Time":strain_interpolated[0], "Strain":strain_interpolated[1],"dR/r0":resistance_normalized['Resistance']})

    csv_file_path = f"combined_data/{sample}_combined_data.csv"
    all_data.to_csv(csv_file_path, index=False)
    print(all_data)

