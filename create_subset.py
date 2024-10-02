import json
import os
import sys

# Path to the commits.json file in the /docs/ folder
COMMITS_FILE = './docs/commits.json'
OUTPUT_DIR = './docs/subsets'  # Directory to save the filtered subsets

# Function to create a subset of commits for a specific file
def create_commit_subset(file_name):
    # Check if commits.json exists
    if not os.path.exists(COMMITS_FILE):
        print(f"Error: {COMMITS_FILE} does not exist. Please run the fetch_commits process first.")
        sys.exit(1)

    # Read commits.json
    with open(COMMITS_FILE, 'r') as f:
        commits = json.load(f)

    # Filter commits that modified the given file
    filtered_commits = [
        commit for commit in commits if any(file['filename'].endswith(file_name) for file in commit['files'])
    ]

    if not filtered_commits:
        print(f"No commits found where {file_name} was modified.")
        return

    # Ensure the output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Define output file path
    output_file_name = f"filtered_commits_{os.path.splitext(file_name)[0]}.json"
    output_file_path = os.path.join(OUTPUT_DIR, output_file_name)

    # Save filtered commits to a new file
    with open(output_file_path, 'w') as f:
        json.dump(filtered_commits, f, indent=2)

    print(f"Filtered commits for {file_name} saved to {output_file_path}")

# Main function to run the script
if __name__ == "__main__":
    # Ensure the user has provided a file name argument
    if len(sys.argv) < 2:
        print("Usage: python create_subset.py <filename>")
        sys.exit(1)

    # Get the file name from the command-line arguments
    file_name = sys.argv[1]
    create_commit_subset(file_name)
