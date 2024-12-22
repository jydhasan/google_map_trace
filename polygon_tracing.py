import cv2
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
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

# Find contours (polygon boundaries)
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Plot detected polygons
plt.figure(figsize=(12, 12))
for contour in contours:
    if len(contour) > 2:  # Ensure the contour can form a polygon
        contour = contour[:, 0, :]
        polygon = Polygon(contour)
        if polygon.is_valid:
            x, y = np.array(polygon.exterior.xy)
            plt.plot(x, -y, color='green')  # Invert Y-axis for proper plotting

plt.title('Traced Plot Shape Polygons')
plt.axis('equal')
plt.show()

# Export as Polygon Shapefile
polygons = []
for contour in contours:
    if len(contour) > 2:
        contour = contour[:, 0, :]
        try:
            polygon = Polygon(contour)
            if polygon.is_valid:  # Ensure the polygon is valid
                polygons.append(polygon)
        except Exception as e:
            print(f"Skipping invalid polygon: {e}")

# Save as Shapefile
gdf = gpd.GeoDataFrame(geometry=polygons)
gdf.to_file('traced_polygons.shp')
