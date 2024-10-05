import os
import requests

# Base URL for the IRC download page
BASE_DOWNLOAD_URL = "https://uscode.house.gov/download/releasepoints/us/pl/118/90/"

# Directory where the files will be stored
DATA_DIR = "data/raw/irc"

# Download all titles (1 to 54)
TITLES = [f"{i:02d}" for i in range(1, 55)]

def download_irc_files():
    """
    Downloads the XML zip files for all IRC titles.
    """
    for title in TITLES:
        # Construct the download URL for each title
        zip_filename = f"xml_usc{title}@118-90.zip"
        url = BASE_DOWNLOAD_URL + zip_filename

        # Download the file
        download_file(url, DATA_DIR, zip_filename)

def download_file(url, dest_folder, filename):
    """
    Downloads a file from the given URL to the destination folder.
    """
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    
    file_path = os.path.join(dest_folder, filename)
    
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            print(f"Downloaded {file_path}")
        else:
            print(f"Failed to download {url} - Status Code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

if __name__ == "__main__":
    download_irc_files()