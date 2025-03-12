import serial
import struct

# Open serial connection to OpenMV (change COM port if needed)
ser = serial.Serial('COM9', 115200, timeout=5)  # Windows: 'COMx', Linux/Mac: '/dev/ttyUSB0' or '/dev/ttyACM0'

# Read image size first (4 bytes)
size_data = ser.read(4)
size = struct.unpack('>I', size_data)[0]  # Convert bytes to integer

# Read the image data
image_data = ser.read(size)

# Save the image
with open("Ambientes_Inteligentes.jpg", "wb") as f:
    f.write(image_data)

print("Image saved as 'Ambientes_Inteligentes.jpg'")
