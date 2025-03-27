import socket
import os
import time
import struct

# Server Configuration
HOST = "0.0.0.0"  
PORT = 52870  
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

    # Read the first 4 bytes to get image size
    img_size_data = conn.recv(4)
    if not img_size_data:
        # print("❌ Error: No image size received.")
        conn.close()
        continue
    
    img_size = struct.unpack(">I", img_size_data)[0]  # Convert bytes to integer
    # print(f"📏 Expected image size: {img_size} bytes")

    # Create a unique name for the received image
    timestamp = int(time.time())
    filename = os.path.join(SAVE_FOLDER, f"received_{timestamp}.jpg")

    # Receive image data
    with open(filename, "wb") as f:
        received_bytes = 0
        while received_bytes < img_size:
            data = conn.recv(min(1024, img_size - received_bytes))
            if not data:
                break
            f.write(data)
            received_bytes += len(data)

    print(f"✅ Image received and stored at: {filename} ({received_bytes} bytes)")
    conn.close()

