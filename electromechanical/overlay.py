import cv2
import pandas as pd

def overlay_centroids(video_path, csv_path, output_path):
    # Read the CSV file containing the centroids
    df = pd.read_csv(csv_path)

    # Initialize video capture and get video properties
    cap = cv2.VideoCapture(video_path)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Define the codec and create a VideoWriter object to save the output
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Get the centroids for the current frame
        centroids = df.loc[df['frame_index'] == frame_count]
        num_points = len(centroids.columns)//2
        for index, row in centroids.iterrows():
            for i in range(1, num_points+1): # Assuming 8 centroids as per the initial setup
                # Extract centroid coordinates
                x, y = row[f'centroid_{i}_x'], row[f'centroid_{i}_y']
                # Draw the centroid on the frame
                cv2.circle(frame, (int(x), int(y)), radius=5, color=(0, 255, 0), thickness=-1)

        # Write the frame with centroids overlayed
        out.write(frame)

        frame_count += 1

    # Release everything when job is finished
    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":

    for sample in ["g3"]:#, "g3", "h1", "h2", "h3"]:
        video_path = f'cropped_videos/{sample}.mp4'
        csv_path = f'centroid_trajectories/{sample}_centroids.csv'
        output_path = f'cropped_videos/{sample}_annotated.mp4'
        overlay_centroids(video_path, csv_path, output_path)

