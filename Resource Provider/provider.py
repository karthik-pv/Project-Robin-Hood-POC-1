import socketio
import base64
import os

sio = socketio.Client()
url = "http://localhost:5000/provider"


@sio.event
def connect():
    print("Provider connected to the server")


@sio.event
def disconnect():
    print("Provider disconnected from the server")


@sio.on("receiveDir")
def receiveDirectory(data):
    encodedFile = data["file"]
    file = base64.b64decode(encodedFile)
    with open("received.zip", "wb") as f:
        f.write(file)
    filepath = os.path.join(os.getcwd(), "received.zip")
    print(f"Received directory from server - " + filepath)


if __name__ == "__main__":
    sio.connect(url)
    sio.wait()
