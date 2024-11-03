import zipfile
import subprocess
import os
import io


def zip_folder(folder_path):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, start=folder_path)
                zipf.write(file_path, arcname)
    zip_buffer.seek(0)
    return zip_buffer


def unzip_file(zip_path, extract_to="."):
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Extracted all files to {extract_to}")


def execute_notebook_and_convert_to_markdown(directory, notebook_file, output_file):
    os.chdir(directory)
    print(f"Changed directory to {os.getcwd()}")

    command = [
        "jupyter",
        "nbconvert",
        "--to",
        "markdown",
        "--execute",
        "--output",
        output_file,
        notebook_file,
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Notebook executed and converted to markdown: {output_file}.md")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during execution: {e}")
