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


@sio.event()
def connect():
    print("Provider connected to the server")


@sio.event()
def disconnect():
    print("Provider disconnected from the server")


@sio.on("receiveDir")
def receiveDirectory(data):
    encodedFile = data["file"]
    file = base64.b64decode(encodedFile)
    with open("received.zip", "wb") as f:
        f.write(file)
    filepath = os.path.join(os.getcwd(), "received.zip")
    extractedFilepath = os.path.join(os.getcwd(), "toExecute")
    print(f"Received directory from server - " + os.getcwd())
    unzip_file(filepath, extractedFilepath)
    execute_notebook_and_convert_to_markdown(extractedFilepath, "test.ipynb", "output")
    zip_buffer = zip_folder(extractedFilepath)
    encodedFile = base64.b64encode(zip_buffer.read()).decode("utf-8")
    try:
        sio.emit("obtainComputedDirectory", {"file": encodedFile})
    except:
        print("Failed to send directory back to server")


if __name__ == "__main__":
    sio.connect(url)
    sio.wait()
