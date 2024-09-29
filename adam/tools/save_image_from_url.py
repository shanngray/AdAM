import requests
import os

# Function to save image from URL
def save_image_from_url(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Image saved successfully to {save_path}")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")