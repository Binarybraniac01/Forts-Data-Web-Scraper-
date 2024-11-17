from selenium import webdriver
from selenium.webdriver.common.by import By
import csv


# # Initialize the WebDriver 
# Setting Options for headless Chromium
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--headless=new")

driver = webdriver.Chrome(options=options) 

# Function to scrape data and save to CSV
def scrape_wikipedia_forts(district_name, url):
    # Open the Wikipedia page
    driver.get(url)
    
    # Find the div with id "mw-pages"
    mw_pages_div = driver.find_element(By.ID, "mw-pages")
    
    # Find all elements with the class "mw-category-group" within mw-pages div
    category_groups = mw_pages_div.find_elements(By.CLASS_NAME, "mw-category-group")
    
    # Prepare data for CSV
    data = []
    
    # Loop through each category group and extract fort name and link
    for group in category_groups:
        # Get all <a> tags inside each mw-category-group
        fort_links = group.find_elements(By.TAG_NAME, "a")
        for fort in fort_links:
            fort_name = fort.text
            fort_link = fort.get_attribute("href")
            data.append([district_name, fort_name, fort_link])
    
    # Append data to CSV file
    with open("forts_data.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Check if the file is empty, if yes, write the header
        if file.tell() == 0:
            writer.writerow(["district_name", "fort_name", "link"])  # Write header only if file is empty
        writer.writerows(data)  # Write rows
    
    print(f"Data saved to forts_data.csv")

# Get district name from the user
district_name = input("Enter the district name: ")
wikipedia_url = input("Enter the Wikipedia URL: ")

# Call the function
scrape_wikipedia_forts(district_name, wikipedia_url)

# Close the driver
driver.quit()
