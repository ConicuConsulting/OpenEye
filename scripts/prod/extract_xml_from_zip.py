import os
import zipfile

DATA_DIR = "data/raw/irc"
EXTRACT_DIR = "data/processed/irc"

def extract_zip_files():
    """
    Extract all zip files from the raw data folder into the processed folder.
    """
    if not os.path.exists(EXTRACT_DIR):
        os.makedirs(EXTRACT_DIR)

    for file_name in os.listdir(DATA_DIR):
        file_path = os.path.join(DATA_DIR, file_name)
        if file_name.endswith(".zip"):
            try:
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(EXTRACT_DIR)
                print(f"Extracted {file_name}")
            except zipfile.BadZipFile:
                print(f"Error: {file_name} is not a valid zip file and will be skipped.")
        else:
            print(f"{file_name} is not a zip file and will be skipped.")

if __name__ == "__main__":
    extract_zip_files()