from flask import Flask, request, jsonify
from flask_socketio import SocketIO
import base64

app = Flask(__name__)
socketio = SocketIO(
    app, ping_timeout=6000, ping_interval=25000, max_http_buffer_size=10000000
)


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
    if request.sid in connectedProviders:
        connectedProviders.remove(request.sid)
    print("providers")
    print(connectedProviders)


@socketio.on("receiverConnect")
def receiverConnect():
    connectedProviders.remove(request.sid)
    socketio.emit("alertReceiver", {"sid": request.sid}, room=request.sid)


@socketio.on("returnDirectory")
def returnDir(data):
    print("here")
    connectedProviders.append(request.sid)
    file = data["file"]
    sidToEmit = receiverProviderMap[request.sid]
    socketio.emit("obtainComputedDirectory", {"file": file}, room=sidToEmit)


@app.route("/uploadDirectory", methods=["POST"])
def upload_directory():
    data = request.get_json()
    if not data or "file" not in data:
        return jsonify({"error": "No file provided"}), 400

    file = data["file"]
    mySid = data["sid"]

    if connectedProviders:
        target_sid = connectedProviders[0]
        connectedProviders.pop(0)
        receiverProviderMap[target_sid] = mySid
        socketio.emit("receiveDir", {"file": file}, room=target_sid)
        print("Directory forwarded to provider:", target_sid)

        return jsonify({"message": "Directory forwarded to provider."}), 200
    else:
        print("No connected providers available")
        return jsonify({"error": "No connected providers available"}), 404


if __name__ == "__main__":
    socketio.run(app, host="localhost", port=5000, debug=True)
