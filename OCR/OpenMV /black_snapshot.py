import sensor, image, time, pyb, os

sensor.reset()
sensor.set_pixformat(sensor.RGB565)  # Use color
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)

black_threshold = [(0, 30, -10, 10, -10, 10)]  # Adjust based on test results

print("Detecting black objects...")

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
            pyb.sync()  # Force sync to USB storage
            print("Saved:", filename)

        except Exception as e:
            print("Error saving image:", e)
