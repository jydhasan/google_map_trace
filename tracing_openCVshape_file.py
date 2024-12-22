import cv2
import numpy as np
import json

# Load the image
image_path = "C:\\Users\\jydhasan\\Desktop\\mapImage.jpg"
image = cv2.imread(image_path)

# Resize the image for faster processing (optional)
scale_percent = 60  # Percentage of original size
width = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)
image = cv2.resize(image, (width, height))

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Edge detection using Canny
edges = cv2.Canny(blurred, 50, 150)

# Find contours
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Extract polygons and save them
polygons = []
for contour in contours:
    # Approximate the contour to reduce the number of points
    epsilon = 0.01 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)
    polygons.append(approx.reshape(-1, 2).tolist())

# Save polygons to a JSON file
output_json_path = "C:\\Users\\jydhasan\\Desktop\\field_shapes.json"
with open(output_json_path, "w") as f:
    json.dump(polygons, f, indent=4)

# Visualize the polygons on the original image
for polygon in polygons:
    pts = np.array(polygon, np.int32)
    pts = pts.reshape((-1, 1, 2))
    cv2.polylines(image, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

# Save the visualized image
output_image_path = "C:\\Users\\jydhasan\\Desktop\\fields_with_shapes.jpg"
cv2.imwrite(output_image_path, image)

output_json_path, output_image_path
