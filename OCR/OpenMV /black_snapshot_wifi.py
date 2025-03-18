import sensor, image, time, network, usocket, pyb, os

# Wi-Fi Credentials (replace with your own)
SSID = "Maria's Galaxy S22"
PASSWORD = "qchq7059"

# Server IP (Replace with your computer's local IP)
SERVER_IP = "192.168.231.167"
SERVER_PORT = 5000

# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)
print("Wifi Status: ", wlan.status())

print("Connecting to Wi-Fi...")
while not wlan.isconnected():
    time.sleep(1)

print("Wifi Status 2: ", wlan.status())
print("Connected! IP:", wlan.ifconfig()[0])

# Initialize Camera
sensor.reset()
sensor.set_pixformat(sensor.RGB565)  # Color mode
sensor.set_framesize(sensor.QVGA)  # 320x240 resolution
sensor.skip_frames(time=2000)

# Define Black Color Threshold (Adjust as needed)
black_threshold = [(0, 30, -10, 10, -10, 10)]

print("Detecting black objects...")


def test_server_connection():
    try:
        print("[INFO] Testing server connection to:", SERVER_IP, SERVER_PORT)
        s = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
        s.settimeout(20)
        s.connect((SERVER_IP, SERVER_PORT))
        print("[INFO] Server is reachable!")
        s.close()
    except Exception as e:
        print("[ERROR] Server connection failed:", e)

test_server_connection()


def send_image(filename):
    """Sends an image to the server via HTTP."""
    try:
        print("[INFO] Opening image:", filename)

        # Open image file
        with open(filename, "rb") as f:
            img_data = f.read()

        print("[INFO] Image size:", len(img_data), "bytes")

        # Criar socket
        print("[INFO] Connecting to server:", SERVER_IP, "on port", SERVER_PORT)
        s = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
        s.settimeout(20)  # Set timeout to avoid blocking

        try:
            s.connect((SERVER_IP, SERVER_PORT))
            print("[INFO] Connected successfully!")
        except Exception as e:
            print("[ERROR] Could not connect to server:", e)
            s.close()
            return

        # Criar o corpo do pedido HTTP
        boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
        body = (
            "--{}\r\n"
            'Content-Disposition: form-data; name="file"; filename="{}"\r\n'
            "Content-Type: image/jpeg\r\n"
            "\r\n".format(boundary, filename)
        ).encode() + img_data + ("\r\n--{}--\r\n".format(boundary)).encode()

        headers = (
            "POST /upload HTTP/1.1\r\n"
            "Host: {}:{}\r\n"
            "Content-Length: {}\r\n"
            "Content-Type: multipart/form-data; boundary={}\r\n"
            "\r\n".format(SERVER_IP, SERVER_PORT, len(body), boundary)
        )

        print("[INFO] Sending request headers...")
        s.send(headers.encode())

        print("[INFO] Sending image data...")
        s.send(body)

        print("[INFO] Image sent successfully!")
        s.close()

    except Exception as e:
        print("[ERROR] Error sending image:", e)
        if 's' in locals():
            s.close()




while True:
    img = sensor.snapshot()
    blobs = img.find_blobs(black_threshold, pixels_threshold=50, area_threshold=50)

    if blobs:
        print("Black detected!")

        for blob in blobs:
            img.draw_rectangle(blob.rect(), color=(0, 255, 0))  # Green box
            img.draw_cross(blob.cx(), blob.cy(), color=(255, 0, 0))  # Red cross

        try:
            timestamp = pyb.millis()
            filename = "black_{}.jpg".format(timestamp)  # Save in root directory
            img.save(filename)

            # Send the image to the server
            send_image(filename)

        except Exception as e:
            print("Error saving/sending image:", e)
