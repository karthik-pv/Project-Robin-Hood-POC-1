import socketio

sio = socketio.Client()


@sio.event
def connect():
    print("Provider connecting to the server")
    sio.connect()


@sio.event
def disconnect():
    print("Provider disconnected from the server")


@sio.on("receiveDir")
def receiveDirectory(data):
    print(f"Received directory from server: {data}")


sio.connect("http://localhost:5000")
sio.wait()
