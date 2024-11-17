import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import base64
import requests
import os
import time  # For adding delay if needed

# Read fort names from the CSV file
forts = []
with open("with_lat_lon/fort_names.csv", "r") as file:
    reader = csv.DictReader(file)  # Read as dictionary to access 'fortname' field by name
    for row in reader:
        forts.append(row['fortname'])

# Setting Options for headless Chromium
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--headless=new") 
# Set up the Selenium WebDriver
driver = webdriver.Chrome(options=options) 

# Create a directory to save images
os.makedirs("with_lat_lon/google_scraper/downloaded_images", exist_ok=True)

# Iterate through each fort and download the first image
for index, fort in enumerate(forts, start=1):
    # Create a search query URL
    query = f"{fort} images"
    driver.get(f"https://www.google.com/search?q={query}&tbm=isch")

    try:
        # Locate the first div with images
        first_div = driver.find_element(By.XPATH, "/html/body/div[3]/div/div[15]/div/div[2]/div[2]/div/div/div/div/div[1]/div/div/div[1]")

        # Find the first img tag within the div
        first_img = first_div.find_element(By.XPATH, ".//img")

        # Download the first image
        img_src = first_img.get_attribute("src")
        if img_src:
            if img_src.startswith("data:image"):  # If the image is Base64 encoded
                # Decode Base64 and save as an image
                base64_data = img_src.split(",")[1]
                with open(f"with_lat_lon/google_scraper/downloaded_images/{fort}.png", "wb") as file:
                    file.write(base64.b64decode(base64_data))
            else:
                # Download the image from the URL
                img_data = requests.get(img_src).content
                with open(f"with_lat_lon/google_scraper/downloaded_images/{fort}.jpg", "wb") as file:
                    file.write(img_data)
            print(f"Image for '{fort}' downloaded successfully.")
        else:
            print(f"No image found for '{fort}'.")
    except Exception as e:
        print(f"Error processing '{fort}': {e}")

    # Optional delay to avoid being flagged as a bot
    time.sleep(2)

# Close the browser
driver.quit()
