from ckanapi import RemoteCKAN
import json
import os

# Step 1: Read the dataset IDs from the file
file_path = 'dataset_ids.txt'
if not os.path.exists(file_path):
    print(f"Error: {file_path} does not exist.")
    exit(1)

with open(file_path, 'r') as f:
    dataset_ids = [line.strip() for line in f if line.strip()]

# Step 2: Create a CKAN API connection
rc = RemoteCKAN('https://open.canada.ca/data/en/')

# Function to fetch data and save as a JSON file
def fetch_and_save_data(resource_id, output_file):
    try:
        result = rc.action.datastore_search(
            resource_id=resource_id,
            filters={"id": dataset_ids},
        )
        
        with open(output_file, "w") as json_file:
            json.dump(result, json_file)

        print(f"Data from resource_id {resource_id} saved to {output_file}")

    except Exception as e:
        print(f"Error fetching data for resource_id {resource_id}: {e}")

# Step 3: Fetch data for both resource IDs

# First table (visits)
fetch_and_save_data("c14ba36b-0af5-4c59-a5fd-26ca6a1ef6db", "docs/filtered_data_visits.json")

# Second table (downloads)
fetch_and_save_data("4ebc050f-6c3c-4dfd-817e-875b2caf3ec6", "docs/filtered_data_downloads.json")
