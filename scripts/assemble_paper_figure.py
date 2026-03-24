# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 10:04:19 2025

@author: ferfo
"""

from PIL import Image

# Paths to your images
image_paths = [
    'C:/Users/ferfo/OneDrive/Escritorio/div-hum-1.png',
    'C:/Users/ferfo/OneDrive/Escritorio/div-hum-2.png',
    'C:/Users/ferfo/OneDrive/Escritorio/div-hum-3.png',
    'C:/Users/ferfo/OneDrive/Escritorio/div1.png',
    'C:/Users/ferfo/OneDrive/Escritorio/div2.png',
    'C:/Users/ferfo/OneDrive/Escritorio/div3.png',
    
]

# Load the images
images = [Image.open(image_path) for image_path in image_paths]

# Find the maximum width and height
max_width = max(img.size[0] for img in images)
max_height = max(img.size[1] for img in images)

# Resize images to the size of the largest image
resized_images = []
for img in images:
    img_ratio = min(max_width / img.size[0], max_height / img.size[1])
    new_size = (int(img.size[0] * img_ratio), int(img.size[1] * img_ratio))
    resized_img = img.resize(new_size, Image.Resampling.LANCZOS)
    new_img = Image.new("RGB", (max_width, max_height), "white")
    new_img.paste(resized_img, ((max_width - new_size[0]) // 2, (max_height - new_size[1]) // 2))
    resized_images.append(new_img)

# Define grid size (3 columns)
cols = 3
rows = (len(resized_images) + cols - 1) // cols  # Compute needed rows

# Create a new blank image with the required size
combined_width = cols * max_width
combined_height = rows * max_height
combined_image = Image.new('RGB', (combined_width, combined_height), "white")

# Paste images in the grid
for index, img in enumerate(resized_images):
    x_offset = (index % cols) * max_width
    y_offset = (index // cols) * max_height
    combined_image.paste(img, (x_offset, y_offset))

# Save the combined image
combined_image_path = 'humedadytemp.png'
combined_image.save(combined_image_path)

print(f"Image saved to {combined_image_path}")
