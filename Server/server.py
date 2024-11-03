from flask import Flask, request
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

connectedProviders = []


@app.route("/")
def index():
    return "SocketIO server is running."


@app.route("/uploadDirectory", methods=["POST"])
def uploadDir():
    socketio.emit("receiveDir", {"data": 123})


@socketio.on("connect")
def handleProviderConnection():
    connectedProviders.append(request.sid)
    print(connectedProviders)


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
