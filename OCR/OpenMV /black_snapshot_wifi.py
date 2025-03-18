import sensor, image, time, network, usocket, pyb, os

# Wi-Fi Credentials (replace with your own)
SSID = "Maria's Galaxy S22"
PASSWORD = "qchq7059"

# Server IP (Replace with your computer's local IP)
SERVER_IP = "192.168.231.167"  # IP do computador onde está o servidor Python
SERVER_PORT = 52870  # Porta do servidor Python

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
sensor.set_pixformat(sensor.RGB565)  # Color mode
sensor.set_framesize(sensor.QVGA)  # 320x240 resolution
sensor.skip_frames(time=2000)

# Define Black Color Threshold (Adjust as needed)
black_threshold = [(0, 30, -10, 10, -10, 10)]

print("Detecting black objects...")


def test_server_connection():
    """Testa se a Nicla Vision consegue conectar-se ao servidor"""
    try:
        print("[INFO] Testing server connection to:", SERVER_IP, SERVER_PORT)
        s = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((SERVER_IP, SERVER_PORT))
        print("[INFO] Server is reachable!")
        s.close()
    except Exception as e:
        print("[ERROR] Server connection failed:", e)

test_server_connection()


def send_image(img):
    """Envia a imagem diretamente para o servidor via socket TCP"""
    try:
        print("[INFO] Converting image to JPEG")
        img_jpeg = img.compress(quality=90)  # Comprime a imagem para reduzir o tamanho

        print("[INFO] Creating socket connection")
        s = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((SERVER_IP, SERVER_PORT))  # Conectar ao servidor

        print("[INFO] Sending image data")
        s.send(img_jpeg)  # Envia os dados da imagem

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
            img.draw_rectangle(blob.rect(), color=(0, 255, 0))
            img.draw_cross(blob.cx(), blob.cy(), color=(255, 0, 0))

        send_image(img)  # Enviar imagem diretamente para o servidor
