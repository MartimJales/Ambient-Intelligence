import sensor, image, time, sys

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)

img = sensor.snapshot()
img.compress(quality=90)  # Compress the image for transfer

# Send image size first
size = img.size()
sys.stdout.write(size.to_bytes(4, 'big'))  # Send size as 4-byte integer

# Send actual image data
sys.stdout.buffer.write(img.bytearray())

print("Image sent over USB.")
