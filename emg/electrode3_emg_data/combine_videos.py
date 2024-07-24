import tkinter as tk
from tkinter import filedialog
from moviepy.editor import VideoFileClip, CompositeVideoClip
import sys

# Function to select a file via file dialog
def select_file(title):
    root = tk.Tk()
    root.withdraw()  # we don't want a full GUI, so keep the root window from appearing
    file_path = filedialog.askopenfilename(title=title, filetypes=[("MP4 files", "*.mp4")])
    return file_path

def select_folder(title):
    root = tk.Tk()
    root.withdraw() 
    file_path = filedialog.askdirectory(title=title)
    return file_path


trial = sys.argv[1]
import good_parameters
parameters = good_parameters.parameters[trial]
# User parameters (modify these as needed)
length = parameters['length']
start_time_experiment = parameters['start_time_experiment']  # start time for experiment_video in seconds
start_time_emg = parameters['start_time_emg']         # start time for emg_data_animation in seconds
placement_x = parameters['placement_x']           # x position of emg_data_animation on experiment_video
placement_y = parameters['placement_y']           # y position of emg_data_animation on experiment_video
scale_factor = parameters['scale_factor']     # scale factor for emg_data_animation (0.5 = 50% of the original size)

end_time_experiment = start_time_experiment + length   # end time for experiment_video in seconds
end_time_emg = start_time_emg+length          # end time for emg_data_animation in seconds

# Select files
folder = trial[:-2] 
experiment_video_path = f"{folder}/experimental_videos/{trial}.mp4"
emg_data_animation_path = f"{folder}/emg_animations/{trial}.mp4"

# Load videos
experiment_video = VideoFileClip(experiment_video_path).subclip(start_time_experiment, end_time_experiment)
emg_data_animation = VideoFileClip(emg_data_animation_path).subclip(start_time_emg, end_time_emg).resize(scale_factor)

# Determine the lowest fps for compatibility
output_fps = min(experiment_video.fps, emg_data_animation.fps)

# Positioning the emg_data_animation on the experiment_video
emg_data_animation = emg_data_animation.set_position((placement_x, placement_y))

# Creating composite video
combined_size = (placement_x + int(emg_data_animation.size[0]*1 + 1), experiment_video.size[1])
print(combined_size)

final_clip = CompositeVideoClip([experiment_video, emg_data_animation], size=combined_size)

# Exporting the video with the determined fps
output = f"output_videos/{trial}.mp4"
final_clip.write_videofile(output, codec="libx264", fps=output_fps)

print(f"Video has been successfully created as {output}")

