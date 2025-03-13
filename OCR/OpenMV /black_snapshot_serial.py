import sensor, image, time, pyb, os

# Configure the camera
sensor.reset()
sensor.set_pixformat(sensor.RGB565)  # Use color
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)

black_threshold = [(0, 30, -10, 10, -10, 10)]  # Adjust based on test results

print("Detecting black objects...")

# Initialize the USB in VCP mode
usb_vcp = pyb.USB_VCP()  # Use USB_VCP instead of usb_vcp()

while True:
    img = sensor.snapshot()  # Capture an image

    # Detect blobs (black objects)
    blobs = img.find_blobs(black_threshold, pixels_threshold=50, area_threshold=50)

    if blobs:
        print("Black detected!")

        for blob in blobs:
            img.draw_rectangle(blob.rect(), color=(0, 255, 0))  # Green box
            img.draw_cross(blob.cx(), blob.cy(), color=(255, 0, 0))  # Red cross

        try:
            timestamp = pyb.millis()
            filename = "black_{}.jpg".format(timestamp)  # Name file based on timestamp

            # Save the image in the flash memory (temporary storage)
            img.save(filename)

            # Send the image over USB as raw binary
            with open(filename, "rb") as f:
                # Read the file in chunks and send it over serial
                chunk_size = 256  # Adjust the chunk size as needed
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break  # End of file
                    usb_vcp.write(chunk)  # Send data over USB VCP

            print("Image sent via USB VCP:", filename)

            # Optionally delete the file after sending
            os.remove(filename)

        except Exception as e:
            print("Error saving or sending image:", e)
