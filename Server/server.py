from flask import Flask, request, jsonify
from flask_socketio import SocketIO
import base64

app = Flask(__name__)
socketio = SocketIO(app)

connectedProviders = []
receiverProviderMap = {}


@app.route("/")
def index():
    return "SocketIO server is running."


@socketio.on("connect")
def handleProviderConnection():
    connectedProviders.append(request.sid)
    print("providers")
    print(connectedProviders)


@socketio.on("disconnect")
def removeProviderConnection():
    connectedProviders.remove(request.sid)
    print("providers")
    print(connectedProviders)


@socketio.on("receiverConnect")
def receiverConnect():
    print("here")
    connectedProviders.remove(request.sid)
    socketio.emit("alertReceiver", {"sid": request.sid}, room=request.sid)


@app.route("/uploadDirectory", methods=["POST"])
def upload_directory():
    data = request.get_json()
    if not data or "file" not in data:
        return jsonify({"error": "No file provided"}), 400

    file = data["file"]

    if connectedProviders:
        target_sid = connectedProviders[0]
        connectedProviders.pop(0)

        socketio.emit("receiveDir", {"file": file}, room=target_sid)
        print("Directory forwarded to provider:", target_sid)

        return jsonify({"message": "Directory forwarded to provider."}), 200
    else:
        print("No connected providers available")
        return jsonify({"error": "No connected providers available"}), 404


@socketio.on("returnDirectory")
def returnDir(data):
    print("here")
    connectedProviders.append(request.sid)
    file = data["file"]
    socketio.emit("receiveDir", {"file": file})


if __name__ == "__main__":
    socketio.run(app, host="localhost", port=5000, debug=True)
