import socket
import os
import time

# Server Configuration
HOST = "0.0.0.0"  # Listening on all network interfaces
PORT = 52870  # Port that the Nicla Vision is using
SAVE_FOLDER = "received_images"

# Create the folder to store images
os.makedirs(SAVE_FOLDER, exist_ok=True)

# Create server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"📡 Server listening on {HOST}:{PORT}...")

while True:
    conn, addr = server_socket.accept()
    print(f"📥 Connection received from {addr}")

    # Create a unique name for the received image
    timestamp = int(time.time())
    filename = os.path.join(SAVE_FOLDER, f"received_{timestamp}.jpg")

    # Receive image data and save it to file
    with open(filename, "wb") as f:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            f.write(data)

    print(f"✅ Image received and stored at: {filename}")
    conn.close()
