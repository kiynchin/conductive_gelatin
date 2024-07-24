import cv2
import pandas as pd
import numpy as np

def select_rois(frame):
    rois = cv2.selectROIs("Frame", frame, False, False)
    cv2.destroyWindow("Frame")
    centroids = [(x + w / 2, y + h / 2) for x, y, w, h in rois]
    num_points = len(centroids)
    return num_points, np.array(centroids[:num_points], dtype=np.float32).reshape(-1, 1, 2)  # Format for Lucas-Kanade

def main(video_path, csv_path):
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    if not ret:
        print("Failed to read video")
        return

    old_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    num_points, p0 = select_rois(frame)
    
    # Lucas Kanade parameters
    lk_params = dict(winSize=(15, 15), maxLevel=2, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

    columns = ['frame_index'] + [f'centroid_{i+1}_{axis}' for i in range(num_points) for axis in ['x', 'y']]
    df = pd.DataFrame(columns=columns)

    frame_index = 0
    old_xs = [point[0][0] for point in p0]
    while ret:
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # calculate optical flow
        p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
        
        # Select good points
        good_new = p1[st==1]
        for i, _ in enumerate(good_new):
            good_new[i][0] = old_xs[i]

        #good_old = p0[st==1]

        # Update the old points to new points
        p0 = good_new.reshape(-1, 1, 2)

        # Store centroids to DataFrame
        current_data = [frame_index] + [val for pt in good_new for val in pt]
        df = pd.concat([df, pd.DataFrame([current_data], columns=columns)], ignore_index=True)

        old_gray = frame_gray.copy()
        ret, frame = cap.read()
        frame_index += 1

    # Save the DataFrame to a CSV file
    df.to_csv(csv_path, index=False)
    cap.release()

if __name__ == "__main__":
    for sample in ["g3"]:#, "g3", "h1", "h2", "h3"]:
        video_path = f"cropped_videos/{sample}.mp4"
        csv_path = f"centroid_trajectories/{sample}_centroids.csv"
        main(video_path, csv_path)

