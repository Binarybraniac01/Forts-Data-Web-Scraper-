from selenium import webdriver
from selenium.webdriver.common.by import By
import base64
import requests
import os

# Initialize WebDriver (ensure you have the correct driver for your browser)
driver = webdriver.Chrome()  # Replace with appropriate WebDriver for your browser
driver.get("https://www.google.com/search?q=raigad+fort+images&tbm=isch")  # Open Google Images page

# Locate the first div with images
first_div = driver.find_element(By.XPATH, "/html/body/div[3]/div/div[15]/div/div[2]/div[2]/div/div/div/div/div[1]/div/div/div[1]")

# Find the first img tag within the div
first_img = first_div.find_element(By.XPATH, ".//img")

# Create a directory to save the image
os.makedirs("downloaded_images", exist_ok=True)

# Download the first image
img_src = first_img.get_attribute("src")
if img_src:
    if img_src.startswith("data:image"):  # If the image is Base64 encoded
        # Decode Base64 and save as an image
        base64_data = img_src.split(",")[1]
        with open("downloaded_images/image_1.png", "wb") as file:
            file.write(base64.b64decode(base64_data))
    else:
        # Download the image from the URL
        img_data = requests.get(img_src).content
        with open("downloaded_images/image_1.jpg", "wb") as file:
            file.write(img_data)
    print("First image downloaded.")

# Close the browser
driver.quit()
