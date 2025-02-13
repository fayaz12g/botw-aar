import sys
import os

def BOTW_download(input_folder, mod_name):
    import requests
    import zipfile
    import shutil
    import getpass

    # URL of the ZIP file
    zip_url = "https://github.com/fayaz12g/aar-files/raw/main/botw/champion.zip"

    username = getpass.getuser()
    directory_path = f"C:/Users/{username}/AppData/Roaming/AnyAspectRatio/perm/botw"
    # Check if the directory exists
    if not os.path.exists(directory_path):
        # Create the directory if it doesn't exist
        os.makedirs(directory_path)
        print(f"Directory {directory_path} created successfully.")
    else:
        print(f"Directory {directory_path} already exists.")
    BOTW_folder = f"C:/Users/{username}/AppData/Roaming/AnyAspectRatio/perm/botw"
    zip_file_source = os.path.join(BOTW_folder, "champion.zip")

    if not os.path.isfile(zip_file_source):
        # Download the ZIP file
        print("Downloading zip file. Please wait...")
        response = requests.get(zip_url)
        print("Zip file downloaded.")
        with open(zip_file_source, "wb") as file:
            print("Writing contents to temp folder.")
            file.write(response.content)

    # Extract the ZIP file
    extract_folder = os.path.join(input_folder, mod_name)
    if not os.path.exists(extract_folder):
        os.makedirs(extract_folder)
    print(f"Extracting zip to {extract_folder}. This can also take a few seconds.")
    with zipfile.ZipFile(zip_file_source, "r") as zip_ref:
        zip_ref.extractall(extract_folder)
