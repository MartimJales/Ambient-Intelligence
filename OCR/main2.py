# import cv2
# import pytesseract
# import numpy as np
# import os
# import time

# # Set Tesseract path if needed (Windows users)
# # pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# # Directory to monitor
# watched_folder = "/mnt/c/Users/Maria/OneDrive - Universidade de Lisboa/Ambiente de Trabalho/MEIC/1º ANO/Ambientes Inteligentes/received_images"

# def get_latest_image(folder):
#     """Returns the latest image file from the folder, or None if no images exist."""
#     files = [f for f in os.listdir(folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
#     if not files:
#         return None
    
#     latest_file = max(files, key=lambda f: os.path.getctime(os.path.join(folder, f)))
#     return os.path.join(folder, latest_file)

# def preprocess_image(img):
#     """Preprocess the image for better OCR results."""
#     # Convert the image to grayscale
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     # Thresholding (Adaptive thresholding works better for varying lighting)
#     thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

#     # Noise removal using GaussianBlur
#     blurred = cv2.GaussianBlur(thresh, (5, 5), 0)

#     # Dilation to strengthen the numbers (optional)
#     kernel = np.ones((3, 3), np.uint8)
#     dilated = cv2.dilate(blurred, kernel, iterations=1)

#     return dilated

# def draw_boxes(image_path):
#     """Detects numbers in an image, draws bounding boxes, and prints the detected numbers."""
#     # Load the image
#     img = cv2.imread(image_path)
#     if img is None:
#         print(f"[ERROR] Failed to read image: {image_path}")
#         return

#     # Preprocess the image for better OCR accuracy
#     preprocessed_img = preprocess_image(img)

#     # Perform OCR to detect numbers and their bounding boxes
#     data = pytesseract.image_to_data(preprocessed_img, config="--psm 6 digits", output_type=pytesseract.Output.DICT)

#     detected_numbers = []

#     # Iterate through detected text
#     for i in range(len(data['text'])):
#         if data['text'][i].strip().isdigit():  # Check if it's a number
#             x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
#             cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Draw box
#             cv2.putText(img, data['text'][i], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
#             detected_numbers.append(data['text'][i])

#     # Save the processed image
#     output_path = "output_detected_numbers.png"
#     cv2.imwrite(output_path, img)

#     # Print detected numbers
#     if detected_numbers:
#         print(f"[INFO] Detected numbers: {', '.join(detected_numbers)}")
#     else:
#         print("[INFO] No numbers detected.")

#     return output_path

# if __name__ == "__main__":
#     print(f"📂 Monitoring folder: {watched_folder}")
    
#     while True:
#         image_path = get_latest_image(watched_folder)
        
#         if image_path:
#             print(f"🔍 Processing image: {image_path}")
#             draw_boxes(image_path)

#             # Optional: Delete or move processed image to avoid reprocessing
#             # os.remove(image_path)  # Deletes the image
#             # os.rename(image_path, "processed/" + os.path.basename(image_path))  # Moves to 'processed' folder

#         time.sleep(2)  # Wait 2 seconds before checking again

import cv2
import easyocr
import numpy as np
import os
import time

# Directory to monitor
watched_folder = "/mnt/c/Users/Maria/OneDrive - Universidade de Lisboa/Ambiente de Trabalho/MEIC/1º ANO/Ambientes Inteligentes/received_images"

def get_latest_image(folder):
    """Returns the latest image file from the folder, or None if no images exist."""
    files = [f for f in os.listdir(folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    if not files:
        return None
    
    latest_file = max(files, key=lambda f: os.path.getctime(os.path.join(folder, f)))
    return os.path.join(folder, latest_file)

def preprocess_image(img):
    """Preprocess the image for better OCR results."""
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Thresholding (Adaptive thresholding works better for varying lighting)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

    # Noise removal using GaussianBlur
    blurred = cv2.GaussianBlur(thresh, (5, 5), 0)

    # Dilation to strengthen the numbers (optional)
    kernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(blurred, kernel, iterations=1)

    return dilated

def draw_boxes(image_path):
    """Detects numbers in an image, draws bounding boxes, and prints the detected numbers using EasyOCR."""
    # Load the image
    img = cv2.imread(image_path)
    if img is None:
        print(f"[ERROR] Failed to read image: {image_path}")
        return

    # Preprocess the image for better OCR accuracy
    preprocessed_img = preprocess_image(img)

    # Initialize EasyOCR reader
    reader = easyocr.Reader(['en'])

    # Perform OCR with EasyOCR
    results = reader.readtext(preprocessed_img)

    detected_numbers = []

    # Iterate through detected text
    for (bbox, text, prob) in results:
        if text.strip().isdigit():  # Check if it's a number
            # Draw bounding box
            top_left = (int(bbox[0][0]), int(bbox[0][1]))
            bottom_right = (int(bbox[2][0]), int(bbox[2][1]))
            cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 2)
            # Put the text on the image
            cv2.putText(img, text, (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            detected_numbers.append(text)

    # Save the processed image
    output_path = "output_detected_numbers_easyocr.png"
    cv2.imwrite(output_path, img)

    # Print detected numbers
    if detected_numbers:
        print(f"[INFO] Detected numbers: {', '.join(detected_numbers)}")
    else:
        print("[INFO] No numbers detected.")

    return output_path

if __name__ == "__main__":
    print(f"📂 Monitoring folder: {watched_folder}")
    
    while True:
        image_path = get_latest_image(watched_folder)
        
        if image_path:
            print(f"🔍 Processing image: {image_path}")
            draw_boxes(image_path)

            # Optional: Delete or move processed image to avoid reprocessing
            # os.remove(image_path)  # Deletes the image
            # os.rename(image_path, "processed/" + os.path.basename(image_path))  # Moves to 'processed' folder

        time.sleep(2)  # Wait 2 seconds before checking again
