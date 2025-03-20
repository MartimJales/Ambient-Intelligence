import sensor, image, time, network, usocket, pyb, os

# Wi-Fi Credentials
SSID = "Maria's Galaxy S22"
PASSWORD = "qchq7059"

# Server IP
SERVER_IP = "192.168.231.167"
SERVER_PORT = 52870

# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

print("Connecting to Wi-Fi...")
while not wlan.isconnected():
    time.sleep(1)

print("Connected! IP:", wlan.ifconfig()[0])

# Initialize Camera
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)

# black_threshold = [(0, 30, -10, 10, -10, 10)]
black_threshold = [(50, 70, -10, 10, -50, -30)]  # (L, A, B) values for blue (logo do tecnico)



print("Detecting black objects...")


def send_image(img):
    try:
        img_jpeg = img.compress(quality=90)
        img_size = len(img_jpeg)  # Get the image size

        s = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((SERVER_IP, SERVER_PORT))

        # Send image size first (convert to 4-byte representation)
        s.send(img_size.to_bytes(4, 'big'))

        # Send image data
        s.sendall(img_jpeg)

        print("[INFO] Image sent successfully!")
        s.close()
    except Exception as e:
        print("[ERROR] Error sending image:", e)
        if 's' in locals():
            s.close()



while True:
    print("[INFO] Waiting 10 seconds before taking the next photo...")
    time.sleep(5)  # Espera 10 segundos antes de tirar a próxima foto

    img = sensor.snapshot()
    blobs = img.find_blobs(black_threshold, pixels_threshold=50, area_threshold=50)

    if blobs:
        print("Black detected!")
        # for blob in blobs:
            # img.draw_rectangle(blob.rect(), color=(0, 255, 0))
            # img.draw_cross(blob.cx(), blob.cy(), color=(255, 0, 0))

        send_image(img)  # Enviar imagem diretamente para o servidor
