import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, sosfilt, iirnotch, tf2sos
import pandas as pd
from datetime import datetime
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter.simpledialog import askinteger

# Butterworth Bandpass Filter
def butter_bandpass(lowcut, highcut, fs, order=4):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    sos = butter(order, [low, high], analog=False, btype='band', output='sos')
    return sos

# Notch Filter
def notch_filter(freq, fs, Q=30):
    nyq = 0.5 * fs
    w0 = freq / nyq
    b,a = iirnotch(w0, Q)
    sos = tf2sos(b, a)
    return sos

# Apply Filters
def apply_filters(data, fs):
    lowcut = 5.0
    highcut = 50.0
    filtered_data = data

    # Apply bandpass filter
    sos_bandpass = butter_bandpass(lowcut, highcut, fs)
    filtered_data = sosfilt(sos_bandpass, filtered_data)

    # Apply notch filters at 50Hz and 60Hz
    for freq in [50, 60]:
        sos_notch = notch_filter(freq, fs)
        filtered_data = sosfilt(sos_notch, filtered_data)

    return filtered_data

# Plotting function
def plot_data(times, data, title):
    plt.figure(figsize=(12, 6))
    plt.plot(times, data, label=title)
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.title(title)
    plt.legend()
    plt.show()

# Function to select the file
def select_file():
    root = Tk()
    root.withdraw()  # Suppress the Tkinter root window
    filename = askopenfilename()  # Show an "Open" dialog box and return the path to the selected file
    root.destroy()  # Close the Tkinter root window
    return filename


def query_channel():
    root = Tk()
    root.withdraw()  # Suppress the Tkinter root window
    channel = askinteger("Input", "Choose a channel (0-7):")
    root.destroy()
    return channel

def process_and_plot():
    filename = select_file()
    if not filename:
        print("No file selected.")
        return

    df = pd.read_csv(filename, skiprows=4)
    starttime = pd.to_datetime(df[' Timestamp (Formatted)'].iloc[0])
    df['Elapsed time (s)'] = df[' Timestamp (Formatted)'].apply(lambda x: (pd.to_datetime(x) - starttime).total_seconds())
    times = df['Elapsed time (s)']
    
    fs = 250  # Sampling frequency

    # Display static graphs before querying the user
    for i in range(1, 9):
        channel_data = df.iloc[:, i].values
        filtered_data = apply_filters(channel_data, fs)
        plot_data(times, filtered_data, f'EXG Channel {i-1} Filtered')

    chosen_channel = query_channel()
    if chosen_channel is None or chosen_channel < 0 or chosen_channel > 7:
        print("Invalid channel selection.")
        return

    channel_data = df.iloc[:, chosen_channel + 1].values
    time_data = times.values
    filtered_data = apply_filters(channel_data, fs)
    plot_data(times, filtered_data, f'Filtered EMG Response')
    #filtered_df = pd.concat([times,channel_data], axis=1)
    filtered_df.to_csv(f"{filename[:-4]}.csv")

process_and_plot()

