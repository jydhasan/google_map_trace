import cv2
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import LineString
import geopandas as gpd

# Load the image
# image_path = '/mnt/data/mapImage.jpg'
image_path = 'C:\\Users\\jydhasan\\Desktop\\fields_with_shapes.jpg'
image = cv2.imread(image_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian Blur to reduce noise
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Apply edge detection (Canny)
edges = cv2.Canny(blurred, threshold1=50, threshold2=150)

# Find contours (lines tracing the shapes)
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Plot detected lines
plt.figure(figsize=(12, 12))
for contour in contours:
    if len(contour) > 1:  # Ensure the contour has enough points
        contour = contour[:, 0, :]  # Simplify contour array
        plt.plot(contour[:, 0], -contour[:, 1], color='blue')  # Invert Y-axis for proper plotting

plt.title('Traced Plot Shape Lines')
plt.axis('equal')
plt.show()

# Export as LineString Shapefile
lines = []
for contour in contours:
    if len(contour) > 1:
        contour = contour[:, 0, :]
        line = LineString(contour)
        lines.append(line)

# Save as Shapefile
gdf = gpd.GeoDataFrame(geometry=lines)
# gdf.to_file('/mnt/data/traced_lines.shp')
gdf.to_file('C:\\Users\\jydhasan\\Desktop\\traced_lines.shp')
