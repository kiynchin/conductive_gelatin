import cv2
import numpy as np
import os

def read_and_check_image(image_path):
    """Load an image and check if it is loaded correctly."""
    if not os.path.exists(image_path):
        print(f"Image file {image_path} does not exist.")
        return None
    image = cv2.imread(image_path)
    if image is None:
        print("Failed to load image from:", image_path)
        return None
    return image

def select_points(image_path, num_points):
    """Allow user to select points on an image to mark the scalebar."""
    image = read_and_check_image(image_path)
    if image is None:
        return []

    points = []
    window_title = f"Select {num_points} points. Press 'c' to confirm, 'u' to undo last point"

    def mouse_callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN and len(points) < num_points:
            cv2.circle(image, (x, y), 5, (0, 255, 0), -1)
            points.append((x, y))
            cv2.imshow(window_title, image)

    cv2.namedWindow(window_title)
    cv2.imshow(window_title, image)
    cv2.setMouseCallback(window_title, mouse_callback)

    while True:
        key = cv2.waitKey(1)
        if key == ord('c') and len(points) == num_points:  # Confirm with 'c' if two points are selected
            break
        elif key == ord('u') and points:  # Undo last point with 'u'
            points.pop()
            image = read_and_check_image(image_path)  # Reload image to clear drawings
            for point in points:
                cv2.circle(image, point, 5, (0, 255, 0), -1)
            cv2.imshow(window_title, image)

    cv2.destroyAllWindows()
    if len(points) < num_points:
        print("Not enough points were selected.")
        return []
    return points

def get_scale_transform(image_path, micrometer_distance):
    points = select_points(image_path, 2)
    #if points:
    #    all_points.append({'FileName': image_file, 'Points': points})
    #else:
    #    print(f"Failed to select valid points for {image_file}")

    pix_distance = np.abs(points[0][0]-points[1][0])
    print(pix_distance)
    print(points)
    print(" ")
    pix_to_um = micrometer_distance / pix_distance 
    return pix_to_um

    
def get_base_line(image_path):
    base_points = select_points(image_path, 5)
    # Convert list of tuples to numpy array for easier manipulation
    points_array = np.array(base_points)
    # Fit line using polyfit, degree 1 for a straight line
    line_params = np.polyfit(points_array[:, 0], points_array[:, 1], 1)
    return line_params

def get_thickness(line_params, points, transform):
    thicknesses = []
    # Calculate distance from each point to the line defined by line_params
    for point in points:
        # Distance from a point to a line (ax + by + c = 0)
        a, b = line_params[0], -1
        c = line_params[1]
        x0, y0 = point[0], point[1]
        distance = np.abs(a*x0 + b*y0 + c) / np.sqrt(a**2 + b**2)
        thicknesses.append(distance * transform)  # Convert pixel distance to micrometers

    return thicknesses


def process_images(folder_path):
    """Process all TIFF images in the specified folder."""
    if not os.path.exists(folder_path):
        print(f"Folder {folder_path} does not exist. Please create it and add .tiff files.")
        return []

    images = [f for f in os.listdir(folder_path) if f.lower().endswith(('.tiff', '.tif'))]


    thicknesses = []
    i = 0
    distances = []
    for image_file in images:
        print(f"Processing {image_file}...")
        image_path = os.path.join(folder_path, image_file)
        transform = get_scale_transform(image_path, int(input("Length of scalebar in micrometers:")))
        i= i+1
        base_line = get_base_line(image_path)
        boundary_points = select_points(image_path, 5)
        top_points = select_points(image_path, 5)
        silver_thickness = get_thickness(base_line, boundary_points, transform)
        total_thickness = get_thickness(base_line, top_points, transform)
        thicknesses.append({"Sample": image_path, "Silver thicknesses (um)": silver_thickness, "Total thicknesses (um)": total_thickness})

    return thicknesses
        
        

if __name__ == "__main__":
    folder_path = 'input_images/'
    points_data = process_images(folder_path)
    print("Collected Points Data:", points_data)

