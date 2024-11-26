# title             imgbb-upload.py
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
import pyperclip
from PIL import ImageGrab
from io import BytesIO
from InquirerPy import inquirer

def upload_to_imgbb(image_data, expiration=345600):
    url = "https://api.imgbb.com/1/upload"
    payload = {
        "key": "YOUR_API_KEY",  # Replace "YOUR_API_KEY" with your actual API key
        "image": image_data,
        "expiration": expiration 
    }

    headers = {
        "Content-type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, data=payload, headers=headers)

    # Print the entire API response
    # print("Full API Response:")
    # print(response.text)  # Raw string output of the etire response


    if response.status_code == 200:
        response_json = response.json()
        image_url = response_json['data']['url']
        delete_url = response_json['data']['delete_url']
        expire = response_json['data']['expiration']
        expire_days = expire / (24 * 60 * 60)
        print("""
Image uploaded successfully and copied to clipboard.

Image URL: {}         
Expire: {} seconds or {} day(s)           
Delete URL: {}
""".format(image_url, expire, expire_days, delete_url))
        pyperclip.copy(image_url)    
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
    # InquirerPy Options for the expiration time
    options = [
        "1 Day = 86400",
        "2 Days = 172800",
        "3 Days = 259200",
        "7 Days = 604800",
        "30 Days = 2592000",
        "90 Days = 15552000",
        "No Expiration = None",  # Special case to set expiration_seconds to None
        "Custom Input"           # Option to manually enter seconds
    ]
    
    # InquirerPy interactive prompt
    selected_option = inquirer.select(
        message="Enter expiration time (in seconds 60-15552000):",
        choices=options,
        default="3 Days = 259200",
    ).execute()

    # Check if the user selected the "Custom Input" option
    if selected_option == "Custom Input":
        # Prompt the user to manually input seconds
        expiration_seconds = inquirer.text(
            message="Enter the expiration time in seconds (0 for no expiration, 60-15552000):",
            validate=lambda result: result.isdigit() and (result == "0" or 60 <= int(result) <= 15552000),
            invalid_message="Please enter 0 or a number between 60 and 15552000."
        ).execute()
        
        # Convert the input to integer
        expiration = int(expiration_seconds)
        
        # If the input is 0, set expiration_seconds to None
        if expiration_seconds == 0:
            expiration = None
    else:
        # Check if the selected option is "No Expiration"
        if selected_option == "No Expiration = None":
            expiration = None
        else:
            # Extract the seconds from the selected option
            expiration = int(selected_option.split('=')[1].strip())

    # Display the final result
    if expiration is None:
        print("You selected no expiration.")
    else:
        print(f"You selected expiration time in seconds: {expiration}")


    image_data = get_clipboard_image_base64()
    if image_data:
        upload_to_imgbb(image_data, expiration)
