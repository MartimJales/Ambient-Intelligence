import sensor, image, time, pyb, os

# Initialize the camera
sensor.reset()
sensor.set_pixformat(sensor.RGB565)  # Use RGB565 for color detection
sensor.set_framesize(sensor.QVGA)    # Set resolution
sensor.skip_frames(time=2000)        # Let the sensor adjust
clock = time.clock()                 # Measure FPS

# Define the color threshold for yellow (adjust as needed)
yellow_threshold = [(60, 100, -10, 10, 40, 80)]  # LAB color space threshold

print("Starting video capture...")

while True:
    clock.tick()
    img = sensor.snapshot()  # Capture an image

    # Find blobs matching yellow color
    blobs = img.find_blobs(yellow_threshold, pixels_threshold=100, area_threshold=100)

    if blobs:
        print("Yellow detected!")

        try:
            timestamp = pyb.millis()  # Unique timestamp
            filename = "/yellow_{}.jpg".format(timestamp)  # Unique filename
            img.save(filename)
            print("Saved:", filename)

            # Check file system space
            stats = os.statvfs("/")
            free_space = stats[0] * stats[3]  # Block size * Available blocks
            print("Free space:", free_space)

            if free_space < 50000:  # If less than 50KB available, warn user
                print("Warning: Low storage space!")

        except Exception as e:
            print("Error saving image:", e)

    print("FPS:", clock.fps())  # Print FPS to monitor performance
    time.sleep_ms(100)  # Reduce CPU usage
