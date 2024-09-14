import os
import requests

# Function to read IDs from a file
def read_ids_from_file(file_path):
    with open(file_path, 'r') as file:
        ids = [line.strip() for line in file.readlines() if line.strip()]
    return ids

# Function to download the .atom file for each ID
def download_files(ids, output_folder):
    base_url = "https://open.canada.ca/data/en/feeds/dataset/{}.atom"
    
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for dataset_id in ids:
        url = base_url.format(dataset_id)
        response = requests.get(url)
        
        if response.status_code == 200:
            # Save the file in the /docs folder
            file_name = f"{dataset_id}.atom"
            file_path = os.path.join(output_folder, file_name)
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded {file_name} to {output_folder}")
        else:
            print(f"Failed to download {dataset_id}: {response.status_code}")

# Main function
def main():
    # Path to the dataset IDs file
    file_path = "dataset_ids.txt"
    
    # Folder where the files will be saved
    output_folder = "docs"
    
    # Read IDs from the file
    ids = read_ids_from_file(file_path)
    
    # Download the files
    download_files(ids, output_folder)

# Run the script
if __name__ == "__main__":
    main()
