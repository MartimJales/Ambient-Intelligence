import cv2
import pytesseract
from PIL import Image
import numpy as np

# tesseract without image preprocessing
# If on Windows, set the Tesseract path
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def draw_boxes(image_path):
    """Detects numbers in an image, draws bounding boxes, and saves the result."""
    # Load the image
    img = cv2.imread(image_path)

    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Perform OCR to detect numbers and their bounding boxes
    data = pytesseract.image_to_data(gray, config="--psm 6 digits", output_type=pytesseract.Output.DICT)

    # Iterate through detected text
    for i in range(len(data['text'])):
        if data['text'][i].strip().isdigit():  # Check if it's a number
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Draw box
            cv2.putText(img, data['text'][i], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # Save and display the image with boxes
    output_path = "output_detected_numbers.png"
    cv2.imwrite(output_path, img)

    # Show the image
    cv2.imshow("Detected Numbers", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return output_path

if __name__ == "__main__":
    image_path = input("Enter image path: ").strip()
    output_image = draw_boxes(image_path)
    print(f"Processed image saved as: {output_image}")
