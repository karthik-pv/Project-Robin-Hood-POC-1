from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import threading

app = Flask(__name__)
socketio = SocketIO(app)

# List to store active client session IDs
clients = []
clients_lock = threading.Lock()  # Lock for thread-safe access to clients list


# Handle WebSocket connection
@socketio.on("connect")
def handle_connect():
    with clients_lock:
        clients.append(request.sid)
        print(f"Client connected: {request.sid}")
        print(f"Current clients: {clients}")


# Handle WebSocket disconnection
@socketio.on("disconnect")
def handle_disconnect():
    with clients_lock:
        if request.sid in clients:
            clients.remove(request.sid)
            print(f"Client disconnected: {request.sid}")
            print(f"Current clients: {clients}")


# HTTP route to send data to all connected clients
@app.route("/sendData", methods=["POST"])
def send_data():
    data = request.json.get("data", "")
    with clients_lock:
        if not clients:
            return jsonify(error="No connected clients"), 503

        for client_id in clients:
            socketio.emit("data_event", {"data": data}, to=client_id)

    print("Data sent to all connected clients")
    return jsonify(message="Data sent to connected clients"), 200


if __name__ == "__main__":
    socketio.run(app, debug=True)
