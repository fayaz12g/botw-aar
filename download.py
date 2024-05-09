import sys
import os

def pmtok_download(input_folder, mod_name):
    import requests
    import zipfile
    import shutil
    import getpass

    # URL of the ZIP file
    zip_url = "https://github.com/fayaz12g/aar-files/raw/main/pmtok/Origami.zip"

    username = getpass.getuser()
    directory_path = f"C:/Users/{username}/AppData/Roaming/AnyAspectRatio/perm/pmtok"
    # Check if the directory exists
    if not os.path.exists(directory_path):
        # Create the directory if it doesn't exist
        os.makedirs(directory_path)
        print(f"Directory {directory_path} created successfully.")
    else:
        print(f"Directory {directory_path} already exists.")
    pmtok_folder = f"C:/Users/{username}/AppData/Roaming/AnyAspectRatio/perm/pmtok"
    zip_file_source = os.path.join(pmtok_folder, "Origami.zip")

    if not os.path.isfile(zip_file_source):
        # Download the ZIP file
        print("Downloading zip file. This may take up to 10 seconds.")
        response = requests.get(zip_url)
        print("Zip file downloaded.")
        with open(zip_file_source, "wb") as file:
            print("Writing contents to temp folder.")
            file.write(response.content)

    # Extract the ZIP file
    extract_folder = os.path.join(input_folder, mod_name, 'romfs', 'ui')
    if not os.path.exists(extract_folder):
        os.makedirs(extract_folder)
    print(f"Extracting zip to {extract_folder}. This can also take a few seconds.")
    with zipfile.ZipFile(zip_file_source, "r") as zip_ref:
        zip_ref.extractall(extract_folder)
