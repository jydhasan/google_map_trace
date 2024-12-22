import cv2
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import LineString
import geopandas as gpd
from PIL import Image

# --- CONFIGURATION ---
# Define lat/lon bounding box (you need to adjust these manually)
# Example: Top-Left (lat1, lon1), Bottom-Right (lat2, lon2)
LAT_LON_BOUNDS = {
    "top_left": (37.7749, -122.4194),   # Replace with actual top-left lat/lon
    "bottom_right": (37.7649, -122.4094)  # Replace with actual bottom-right lat/lon
}

# Load the image
# image_path = '/mnt/data/mapImage.jpg'
image_path = 'C:\\Users\\jydhasan\\Desktop\\fields_with_shapes.jpg'
image = cv2.imread(image_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Get image dimensions
img = Image.open(image_path)
width, height = img.size

# Apply Gaussian Blur to reduce noise
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Apply edge detection (Canny)
edges = cv2.Canny(blurred, threshold1=50, threshold2=150)

# Find contours (lines tracing the shapes)
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Function to convert pixel coordinates to latitude and longitude
def pixel_to_latlon(x, y, width, height, bounds):
    lon = bounds["top_left"][1] + (x / width) * (bounds["bottom_right"][1] - bounds["top_left"][1])
    lat = bounds["top_left"][0] - (y / height) * (bounds["top_left"][0] - bounds["bottom_right"][0])
    return lon, lat

# Plot detected lines and map to lat/lon
plt.figure(figsize=(12, 12))
lines = []
for contour in contours:
    if len(contour) > 1:  # Ensure valid contour
        contour = contour[:, 0, :]
        latlon_points = [pixel_to_latlon(x, y, width, height, LAT_LON_BOUNDS) for x, y in contour]
        line = LineString(latlon_points)
        lines.append(line)
        plt.plot(*zip(*latlon_points), color='blue')

plt.title('Traced Plot Shape Lines with Latitude and Longitude')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.axis('equal')
plt.show()

# Export as Shapefile with lat/lon
gdf = gpd.GeoDataFrame(geometry=lines, crs="EPSG:4326")  # WGS84 CRS
gdf.to_file('C:\\Users\\jydhasan\\Desktop\\traced_lines_with_latlon.shp')
