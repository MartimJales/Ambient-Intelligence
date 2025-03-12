# ------------- Receive image and Save 
import serial
import numpy as np
import cv2

# Open serial connection (adjust port if needed)
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=5)  # Change to "COM3" for Windows

# Read image data
data = ser.read(320 * 240)  # Adjust based on resolution

# Convert to an image
img = np.frombuffer(data, dtype=np.uint8).reshape((240, 320))

# Save the image
cv2.imwrite("bus.jpg", img)

# Show the image
cv2.imshow("Captured Bus", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# ------------ Run Tesseract OCR 
import cv2
import pytesseract

# Load the image
img = cv2.imread("bus.jpg")

# Convert to grayscale (if not already)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply thresholding to enhance text
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY, 11, 2)

# Save the processed image
cv2.imwrite("bus_processed.jpg", thresh)

# Run OCR
text = pytesseract.image_to_string(thresh, config="--psm 7")
print("Bus Number:", text.strip())
