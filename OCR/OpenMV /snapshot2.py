import sensor, image, time

# Initialize the camera
sensor.reset()
sensor.set_pixformat(sensor.RGB565)  # RGB or Grayscale (sensor.GRAYSCALE)
sensor.set_framesize(sensor.QVGA)  # QVGA (320x240) or other
sensor.skip_frames(time=2000)  # Let the camera adjust

print("Recording...")
time.sleep(3)  # Wait for 3 seconds

print("Capturing Image...")
img = sensor.snapshot()
img.save("5555.jpg")

print("Image saved as image.jpg")
