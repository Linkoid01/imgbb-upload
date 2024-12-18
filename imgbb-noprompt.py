# title             imgbb-noprompt.py
# description:      Use this script upload your taken screenshot from clipboard to imgbb.com.
# author:           Linkoid01
# date              2024-11-26
# version           1.0
# usage             Place your API Key under the payload section, then python imgbb-upload.py
# copyright         Code can be freely used as long as credit is given.
# history
# 2024-11-26        V1.0 released

import requests
import base64
from PIL import ImageGrab
from io import BytesIO

def upload_to_imgbb(image_data):
    url = "https://api.imgbb.com/1/upload"
    payload = {
        "key": "YOUR_API_KEY",  # Replace "YOUR_API_KEY" with your actual API key
        "image": image_data,
        "expiration": 300  # Expiration in seconds, remove if you want no expiration
    }

    headers = {
        "Content-type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, data=payload, headers=headers)

    if response.status_code == 200:
        response_json = response.json()
        image_url = response_json['data']['url']
        print("Image uploaded successfully:", image_url)
        return image_url
    else:
        print("Upload failed:", response.text)
        return None

def get_clipboard_image_base64():
    image = ImageGrab.grabclipboard()  # Get the image from clipboard
    if image is not None:
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")
    else:
        print("No image found in clipboard.")
        return None

if __name__ == "__main__":
    image_data = get_clipboard_image_base64()
    if image_data:
        upload_to_imgbb(image_data)
