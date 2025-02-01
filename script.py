import os
import pandas as pd

# Define the base dataset folder
dataset_folder = r"C:\backupds\dataset"

# Initialize a list to store file paths and disease names
data = []

# Walk through the dataset folder and collect image paths and disease names
for root, dirs, files in os.walk(dataset_folder):
    for file in files:
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp')):
            # Extract full file path
            file_path = os.path.join(root, file)
            # Extract the disease name from the subfolder
            disease_name = os.path.basename(root)
            # Add the file path and disease name to the list
            data.append({"File Path": file_path, "Disease Name": disease_name})

# Create a DataFrame and save to a CSV file
output_file = "dataset.csv"
df = pd.DataFrame(data)
df.to_csv(output_file, index=False)

print(f"CSV file '{output_file}' created successfully with {len(data)} entries.")
