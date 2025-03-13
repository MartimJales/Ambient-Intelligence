import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565)  # Keep color format
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)

print("Point at a black object and check the LAB values.")

while True:
    img = sensor.snapshot()
    img.draw_string(10, 10, "Point at black", color=(255, 255, 255))  # White text

    for blob in img.find_blobs([(0, 100, -128, 127, -128, 127)], pixels_threshold=10, area_threshold=10):
        img.draw_rectangle(blob.rect(), color=(0, 255, 0))  # Green box
        cx, cy = blob.cx(), blob.cy()  # Get center of blob
        l_value, a_value, b_value = img.get_pixel(cx, cy)  # Read LAB color

        print("L:", l_value, "A:", a_value, "B:", b_value)
