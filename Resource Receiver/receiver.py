import os
import zipfile
import io
import requests


def zip_folder(folder_path):
    """Zip the contents of a folder"""
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, start=folder_path)
                zipf.write(file_path, arcname)
    zip_buffer.seek(0)
    return zip_buffer


def send_folder_to_server(folder_path, server_url):
    """Send zipped folder to the server"""
    zip_buffer = zip_folder(folder_path)
    files = {"file": ("folder.zip", zip_buffer, "application/zip")}

    try:
        response = requests.post(server_url, files=files)
        print(f"Server response: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Failed to send the folder: {str(e)}")


if __name__ == "__main__":
    folder_to_zip = "D:\AIML\End to End Machine Learning Project"
    server_api_url = "http://127.0.0.1:5000/uploadFolder"

    send_folder_to_server(folder_to_zip, server_api_url)
