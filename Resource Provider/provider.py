import socket

SERVER_HOST = "localhost"
SERVER_PORT = 6000


def main():
    # Create a socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as provider_socket:
        # Attempt to connect to the server
        provider_socket.connect((SERVER_HOST, SERVER_PORT))
        print(f"Connected to server at {SERVER_HOST}:{SERVER_PORT}")

        # Continuously listen for data from the server
        try:
            while True:
                # Receive data from the server
                data = provider_socket.recv(1024)
                if not data:
                    break  # Exit if no data is received

                # Handle received data (e.g., save to file, print, etc.)
                print(f"Received data from server: {data.decode()}")
                with open("received_file", "ab") as f:
                    f.write(data)

        finally:
            print("Connection closed by the server")


if __name__ == "__main__":
    main()
