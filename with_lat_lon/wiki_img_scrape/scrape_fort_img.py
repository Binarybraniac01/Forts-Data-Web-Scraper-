import os
import csv
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

# Setting Options for headless Chromium
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--headless=new")


# Function to download an image
def download_image(url, file_name):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(file_name, "wb") as file:
                file.write(response.content)
            print(f"Image downloaded: {file_name}")
        else:
            print(f"Failed to download image from {url}. HTTP status code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading image: {e}")

# Main function to process CSV and download images
def process_csv_and_download_images(csv_file):
    # Create an 'images' folder if it doesn't exist
    if not os.path.exists("with_lat_lon/images"):
        os.makedirs("with_lat_lon/images")
    
    # Set up the Selenium WebDriver
    driver = webdriver.Chrome(options=options) 
    
    try:
        # Open the CSV file
        with open(csv_file, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                fort_name = row["fort_name"]
                link = row["link"]
                
                # Open the webpage
                print(f"Processing {fort_name} from {link}")
                driver.get(link)
                
                try:
                    # Locate the first image inside the table tag
                    image_element = driver.find_element(By.CSS_SELECTOR, "table img")
                    image_url = image_element.get_attribute("src")
                    
                    # Define the image file path
                    image_file_path = os.path.join("with_lat_lon/images", f"{fort_name}.jpg")
                    
                    # Download the image
                    download_image(image_url, image_file_path)
                except Exception as e:
                    print(f"Failed to process {fort_name}: {e}")
    
    finally:
        # Close the browser
        driver.quit()

# Input CSV file
csv_file = "with_lat_lon/fort_details.csv"

# Call the main function
process_csv_and_download_images(csv_file)


