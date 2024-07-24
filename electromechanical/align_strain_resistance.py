import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt 
import tkinter as tk
from tkinter import filedialog
import sys

def plot_curves(sample, alignment):
    root = tk.Tk()
    root.withdraw()
    strain_path = f"strain_curves/{sample}_strain.csv"
    resistance_path = f"resistance_curves/{sample}_resistance.txt"
    strain = pd.read_csv(strain_path, header=None)
    resistance = pd.read_csv(resistance_path, header=None)
    sns.set_theme(style="darkgrid")
    plt.figure(figsize=(10,6))
    strain_endtime = strain[0][len(strain[0])-1]
    resistance_endtime = resistance[0][len(resistance[0])-1]
    #alignment = resistance_endtime - strain_endtime
    sns.lineplot(x=strain[0], y=strain[1])
    sns.lineplot(x=resistance[0]-alignment, y=resistance[1])
    plt.ylim((0, 100))
    plt.xlim(left=0, right=None)
    plt.show()


plot_curves(sys.argv[1], float(sys.argv[2]))
