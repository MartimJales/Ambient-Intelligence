import sensor, image, time, sys

sensor.reset()
sensor.set_pixformat(sensor.RGB565)  # Use sensor.GRAYSCALE if needed
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)  # Let camera adjust

time.sleep(3)  # Wait before capturing
img = sensor.snapshot()

# Send image to PC
sys.stdout.write(img.compress(quality=90))  # Compress & send
print("Image sent to PC")
