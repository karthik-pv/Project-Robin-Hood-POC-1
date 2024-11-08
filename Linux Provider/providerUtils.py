import zipfile
import subprocess
import os
import io
import sys


def install_requirements():
    requirements_file = "requirements.txt"

    if os.path.exists(requirements_file):
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "-r", requirements_file]
            )
            print("Dependencies installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error installing dependencies: {e}")
    else:
        print("requirements.txt file not found.")


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
    originalDirectory = os.getcwd()
    os.chdir(directory)
    print(f"Changed directory to {os.getcwd()}")
    os.environ["HOME"] = "/tmp"
    install_requirements()
    execute_command = [
        "jupyter",
        "nbconvert",
        "--to",
        "notebook",
        "--execute",
        "--inplace",
        notebook_file,
    ]

    convert_command = [
        "jupyter",
        "nbconvert",
        "--to",
        "markdown",
        "--output",
        output_file,
        notebook_file,
    ]

    try:
        subprocess.run(execute_command, check=True, cwd=directory)
        subprocess.run(convert_command, check=True, cwd=directory)
        print(f"Notebook executed and converted to markdown: {output_file}.md")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during execution: {e}")
    finally:
        os.chdir(originalDirectory)
