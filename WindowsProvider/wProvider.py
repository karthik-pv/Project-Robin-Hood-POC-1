import socketio
import base64
import os
from providerUtils import (
    unzip_file,
    execute_notebook_and_convert_to_markdown,
    zip_folder,
)

sio = socketio.Client()
url = "http://localhost:5000"
execution_completed = False


@sio.event()
def connect():
    print("Provider connected to the server")


@sio.event()
def disconnect():
    print("Provider disconnected from the server")


@sio.on("receiveDir")
def receiveDirectory(data):
    global execution_completed
    if execution_completed:
        print("Execution already completed, skipping re-processing.")
        return  # Exit if already executed

    encodedFile = data["file"]
    file = base64.b64decode(encodedFile)
    extractedFilepath = os.path.join(os.getcwd(), "toExecute")

    # Write and extract the incoming zip only once
    with open("received.zip", "wb") as f:
        f.write(file)

    print(f"Received directory from server at {os.getcwd()}")
    unzip_file("received.zip", extractedFilepath)

    # Execute notebook and convert to markdown
    execute_notebook_and_convert_to_markdown(extractedFilepath, "test.ipynb", "output")

    # Zip the processed directory for return
    zip_buffer = zip_folder(extractedFilepath)
    encodedFile = base64.b64encode(zip_buffer.read()).decode("utf-8")

    try:
        print("Emitting returnDirectory event to server")
        sio.emit("returnDirectory", {"file": encodedFile})
        execution_completed = True  # Set flag to avoid re-execution
    except Exception as e:
        print(f"Failed to send directory back to server: {str(e)}")


if __name__ == "__main__":
    sio.connect(url)
    sio.wait()
