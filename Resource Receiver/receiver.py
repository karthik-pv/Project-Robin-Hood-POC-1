import os
import socketio
import base64
import requests
import threading
from receiverUtils import zip_folder, unzip_file

sio = socketio.Client()
mySid = None
url = "http://127.0.0.1:5000"
folder_to_zip = "D:\\AIML\\End to End Machine Learning Project"


@sio.on("alertReceiver")
def receiver_connect(data):
    global mySid
    mySid = data["sid"]
    print(f"Connected with SID: {mySid}")


@sio.on("obtainComputedDirectory")
def obtain_post_processing(data):
    encoded_file = data["file"]
    file = base64.b64decode(encoded_file)
    with open("processedNReceived.zip", "wb") as f:
        f.write(file)
    unzip_file("processedNReceived.zip", folder_to_zip)
    print("File received and unzipped successfully.")
    os.remove(os.path.join(os.getcwd(), "processedNReceived.zip"))


def send_folder_to_server(folder_path, server_url, sid):
    zip_buffer = zip_folder(folder_path)
    encoded_file = base64.b64encode(zip_buffer.read()).decode("utf-8")

    data = {"file": encoded_file, "filename": "folder.zip", "sid": sid}

    try:
        response = requests.post(f"{server_url}/uploadDirectory", json=data)
        if response.status_code == 200:
            print("Folder sent successfully.")
        else:
            print(
                f"Failed to send the folder. Status code: {response.status_code}, Response: {response.text}"
            )
    except requests.exceptions.RequestException as e:
        print(f"Failed to send the folder: {str(e)}")


def prompt_send_folder():
    global mySid
    while True:
        user_input = input("Type 'yes' to send the folder or 'exit' to quit: ")
        if user_input.lower() == "yes":
            user_input = ""
            if mySid:
                send_folder_to_server(folder_to_zip, url, mySid)
            else:
                print("SID not yet assigned. Waiting for WebSocket connection...")
        elif user_input.lower() == "exit":
            break


if __name__ == "__main__":
    sio.connect(url)
    sio.emit("receiverConnect")
    threading.Thread(target=prompt_send_folder, daemon=True).start()
    sio.wait()
