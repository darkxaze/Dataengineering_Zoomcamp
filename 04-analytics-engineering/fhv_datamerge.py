import os
import requests
import pandas as pd
from zipfile import ZipFile
from io import BytesIO

# Base URL for FHV taxi data
BASE_URL = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/"
OUTPUT_DIR = "fhv_data"
MERGED_FILE = "fhv_2019_combined.csv"

# Ensure the output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Download and extract files
csv_files = []
for month in range(1, 13):
    filename = f"fhv_tripdata_2019-{month:02d}.csv.gz"
    url = f"{BASE_URL}{filename}"
    
    print(f"Downloading {filename}...")
    response = requests.get(url)
    
    if response.status_code == 200:
        file_path = os.path.join(OUTPUT_DIR, filename)
        with open(file_path, "wb") as f:
            f.write(response.content)
        csv_files.append(file_path)
    else:
        print(f"Failed to download {filename}")

# Merge CSV files
print("Merging files...")
df_list = [pd.read_csv(f) for f in csv_files]
merged_df = pd.concat(df_list, ignore_index=True)

# Save merged CSV file
merged_df.to_csv(MERGED_FILE, index=False)
print(f"Merged file saved as {MERGED_FILE}")
