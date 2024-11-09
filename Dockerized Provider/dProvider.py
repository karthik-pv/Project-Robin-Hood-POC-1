import socketio
import base64
import os
from providerUtils import (
    unzip_file,
    execute_notebook_and_convert_to_markdown,
    zip_folder,
)
import shutil

sio = socketio.Client()
url = "http://192.168.0.108:5000"


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
    extractedFilepath = os.path.join(os.getcwd(), "toExecute")
    with open("received.zip", "wb") as f:
        f.write(file)
    print(f"Received directory from server at {os.getcwd()}")
    unzip_file("received.zip", extractedFilepath)
    execute_notebook_and_convert_to_markdown(extractedFilepath, "test.ipynb", "output")
    zip_buffer = zip_folder(extractedFilepath)
    encodedFile = base64.b64encode(zip_buffer.read()).decode("utf-8")
    try:
        print("Emitting returnDirectory event to server")
        sio.emit("returnDirectory", {"file": encodedFile})
        zip_buffer.close()
        shutil.rmtree(extractedFilepath)
        os.remove(os.path.join(os.getcwd(), "received.zip"))
    except Exception as e:
        print(f"Failed to send directory back to server: {str(e)}")


if __name__ == "__main__":
    sio.connect(url)
    sio.wait()
