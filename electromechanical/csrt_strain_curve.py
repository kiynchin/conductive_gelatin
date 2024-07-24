import cv2
import pandas as pd
import numpy as np

def select_and_init_rois(frame):
    # First, display the original high-resolution frame for ROI selection
    rois = cv2.selectROIs("Frame", frame, False, False)
    cv2.destroyWindow("Frame")
    
    trackers = []
    for roi in rois:
        tracker = cv2.TrackerCSRT_create()
        trackers.append(tracker)
    
    return trackers, rois

def downsample_frame(frame, scale_percent):
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

def main(video_path, csv_path, scale_percent=50):
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    if not ret:
        print("Failed to read video")
        return

    # Select ROIs on the original frame, then downsample
    trackers, rois = select_and_init_rois(frame)
    frame = downsample_frame(frame, scale_percent)
    
    # Adjust ROIs for the downscaled frame
    adjusted_rois = [(int(x*scale_percent/100), int(y*scale_percent/100), int(w*scale_percent/100), int(h*scale_percent/100)) for x,y,w,h in rois]
    
    # Initialize trackers with downscaled frame and adjusted ROIs
    for tracker, roi in zip(trackers, adjusted_rois):
        tracker.init(frame, roi)
    
    columns = ['frame_index'] + [f'centroid_{i+1}_{axis}' for i in range(len(rois)) for axis in ['x', 'y']]
    df = pd.DataFrame(columns=columns)

    frame_index = 0
    while ret:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Downsample the frame before processing
        frame = downsample_frame(frame, scale_percent)
        
        centroids = []
        for tracker in trackers:
            success, box = tracker.update(frame)
            if success:
                # Calculate centroids in the context of the downscaled frame
                centroids.append((box[0] + box[2] / 2, box[1] + box[3] / 2))
        
        current_data = [frame_index] + [val for centroid in centroids for val in centroid]
        df = pd.concat([df, pd.DataFrame([current_data], columns=columns)], ignore_index=True)

        frame_index += 1

    # Save the DataFrame to a CSV file
    df.to_csv(csv_path, index=False)
    cap.release()

if __name__ == "__main__":
    for sample in ["g2"]:#, "g3", "h1", "h2", "h3"]:
        video_path = f"cropped_videos/{sample}.mp4"
        csv_path = f"cropped_videos/{sample}_centroids.csv"
        main(video_path, csv_path)

