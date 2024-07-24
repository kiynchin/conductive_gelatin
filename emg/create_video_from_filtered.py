import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os

def animate(i, times, fs, data, line, window=5):
    start = i / fs
    end = start + window
    if end > times.iloc[-1]:
        end = times.iloc[-1]
        start = end - window
    plt.xlim(start, end)
    plt.ylim(np.min(data), np.max(data))
    line.set_data(times, data)
    return line,


def plot()
    # Filtering for the chosen channel
    filtered_data = apply_filters(channel_data, fs)
    
    # Animation setup
    fig, ax = plt.subplots()
    line, = ax.plot([], [], lw=2)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Amplitude')
    ax.set_title(f'EXG Channel {chosen_channel} Filtered')

    # Adjusting the frames and interval for real-time playback
    frame_rate = 30  # Adjust if necessary for smoother playback
    interval = 1000 / frame_rate  # milliseconds per frame

    def init():
        ax.set_xlim(0, 5)
        ax.set_ylim(0.2*np.min(filtered_data), 0.2*np.max(filtered_data))
        return line,

    ani = FuncAnimation(fig, animate, init_func=init, frames=len(times),
                        fargs=(times, fs, filtered_data, line, 5),
                        blit=True, interval=interval, repeat=False)
    
    # Save animation
    video_dir = os.path.join(os.path.dirname(filename), 'videos')
    os.makedirs(video_dir, exist_ok=True)
    video_filename = os.path.splitext(os.path.basename(filename))[0] + f'_channel{chosen_channel}.mp4'
    video_path = os.path.join(video_dir, video_filename)
    ani.save(video_path, writer='ffmpeg', fps=frame_rate)

    print(f"Animation saved to {video_path}")


