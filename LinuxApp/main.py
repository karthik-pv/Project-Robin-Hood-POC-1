import subprocess
import os


def execute_notebook_and_convert_to_markdown(directory, notebook_file, output_file):
    # Navigate to the target directory
    os.chdir(directory)
    print(f"Changed directory to {os.getcwd()}")

    # Construct the command to execute the Jupyter notebook and convert it to Markdown
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
        # Execute the command
        subprocess.run(command, check=True)
        print(f"Notebook executed and converted to markdown: {output_file}.md")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during execution: {e}")


# Example usage
directory_path = "D:\AIML\End to End Machine Learning Project"
notebook_filename = "test.ipynb"
output_markdown_filename = "output_results"

# Call the function with the given parameters
execute_notebook_and_convert_to_markdown(
    directory_path, notebook_filename, output_markdown_filename
)
