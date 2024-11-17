# This generates fort details csv usning fort_lat_long.gpx ,fort_details.csv, fort_names.csv

# step 1
import xml.etree.ElementTree as ET
import csv

# Paths to the input and output files
input_file_path = 'fort_lat_long.gpx'
fort_data_csv_path = 'fort_details.csv'
fort_names_csv_path = 'fort_names.csv'

# Parse the GPX file
tree = ET.parse(input_file_path)
root = tree.getroot()

# Extract relevant data and write to fort_data.csv
fort_data = []
unique_forts = set()  # To track unique fort names

for wpt in root.findall('.//{*}wpt'):
    lat = wpt.get('lat')
    lon = wpt.get('lon')
    name = wpt.find('{*}name')
    link = wpt.find('{*}link')
    
    fort_name = name.text if name is not None else ''
    link_text = link.get('href') if link is not None else ''
    
    # Check for duplicates by fort_name
    if fort_name not in unique_forts:
        unique_forts.add(fort_name)
        fort_data.append([fort_name, lat, lon, link_text])

# Write to fort_data.csv
with open(fort_data_csv_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['fort_name', 'lat', 'lon', 'link'])
    writer.writerows(fort_data)

# Write to fort_names.csv with only unique fort names
fort_names = [[row[0]] for row in fort_data]  # Extract only fort_name column
with open(fort_names_csv_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['fortname'])
    writer.writerows(fort_names)

print("CSV files generated successfully without duplicates.")


#step 2

import pandas as pd

# Load the two CSV files
fort_names_df = pd.read_csv('fort_names.csv')
fort_details_df = pd.read_csv('fort_details.csv')

# Check if the 'district' column exists in fort_names.csv
if 'district' not in fort_names_df.columns:
    raise ValueError("The 'district' column is not present in fort_names.csv")

# Extract the 'district' column from fort_names.csv
district_column = fort_names_df['district']

# Insert the 'district' column at the beginning of fort_details_df
fort_details_df.insert(0, 'district', district_column)

# Save the modified fort_details.csv
fort_details_df.to_csv('fort_details.csv', index=False)

print("New column 'district' added to fort_details.csv successfully.")

