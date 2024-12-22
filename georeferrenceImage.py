from PIL import Image
import rasterio
from rasterio.transform import from_bounds
import numpy as np

# --- CONFIGURATION ---
# Define image path
image_path = 'C:\\Users\\jydhasan\\Desktop\\mapImage.jpg'
output_path = 'C:\\Users\\jydhasan\\Desktop\\mapImage_georeferenced.tif'

# Define lat/lon bounding box (adjust these manually)
LAT_LON_BOUNDS = {
    "top_left": (37.7749, -122.4194),   # Replace with actual top-left lat/lon
    "bottom_right": (37.7649, -122.4094)  # Replace with actual bottom-right lat/lon
}

# Open the image and get its dimensions
with Image.open(image_path) as img:
    width, height = img.size

# Calculate transformation matrix
transform = from_bounds(
    LAT_LON_BOUNDS['top_left'][1],  # Left (Longitude)
    LAT_LON_BOUNDS['bottom_right'][0],  # Bottom (Latitude)
    LAT_LON_BOUNDS['bottom_right'][1],  # Right (Longitude)
    LAT_LON_BOUNDS['top_left'][0],  # Top (Latitude)
    width,
    height
)

# Write the georeferenced image using rasterio
with rasterio.open(
    output_path,
    'w',
    driver='GTiff',
    height=height,
    width=width,
    count=3,
    dtype='uint8',
    crs='EPSG:4326',  # WGS84 Latitude/Longitude
    transform=transform
) as dst:
    with Image.open(image_path) as img:
        img_data = img.convert('RGB')
        img_array = np.array(img_data)  # Convert to NumPy array
        for i in range(3):  # Write RGB channels
            dst.write(img_array[:, :, i], i + 1)

print("✅ Georeferenced image saved at:", output_path)
