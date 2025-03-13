import serial

# Open the serial port (make sure to select the correct port)
ser = serial.Serial('/dev/ttyS1', 115200)  # Replace 'COM_PORT' with your actual port

# Prepare to receive the image
with open("received_image.jpg", "wb") as f:
    while True:
        data = ser.read(256)  # Read 256 bytes at a time
        if not data:
            break  # Exit when no more data is available
        f.write(data)  # Write the received data to the file

print("Image received and saved.")
