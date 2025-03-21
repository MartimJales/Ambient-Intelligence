import os
import time
import cv2
import pytesseract
import pywhatkit as kit
import win32api
import pygame
import easyocr


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# Set up directories
watched_folder = "received_images"
processed_folder = "processed_images"
audio_folder = "audio_files"

def get_latest_image(folder):
    """Returns the latest image file from the folder, or None if no images exist."""
    files = [f for f in os.listdir(folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    if not files:
        return None
    
    latest_file = max(files, key=lambda f: os.path.getctime(os.path.join(folder, f)))
    return os.path.join(folder, latest_file)

# def draw_boxes(image_path):
#     """Detects numbers in an image and returns the detected number."""
#     img = cv2.imread(image_path)
#     if img is None:
#         print(f"[ERROR] Failed to read image: {image_path}")
#         return None

#     # Convert image to grayscale for better OCR accuracy
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     # Perform OCR to detect numbers
#     data = pytesseract.image_to_data(gray, config="--psm 6 digits", output_type=pytesseract.Output.DICT)
#     detected_numbers = [text for text in data['text'] if text.strip().isdigit()]

#     if detected_numbers:
#         detected_number = detected_numbers[0]  # Taking the first detected number
#         print(f"[INFO] Detected number: {detected_number}")
#         return detected_number
#     else:
#         print("[INFO] No numbers detected.")
#         return None

def draw_boxes(image_path):
    """Detects numbers in an image and returns the detected number using EasyOCR."""
    img = cv2.imread(image_path)
    if img is None:
        print(f"[ERROR] Failed to read image: {image_path}")
        return None

    # Initialize the EasyOCR reader (you can specify the language here, e.g., 'en' for English)
    reader = easyocr.Reader(['en'])

    # Perform OCR to detect text
    results = reader.readtext(image_path)

    detected_numbers = []
    for result in results:
        text = result[1]
        if text.isdigit():  # Check if the detected text is a number
            detected_numbers.append(text)

    if detected_numbers:
        detected_number = detected_numbers[0]  # Taking the first detected number
        print(f"[INFO] Detected number: {detected_number}")
        return detected_number
    else:
        print("[INFO] No numbers detected.")
        return None


def play_audio(number):
    audio_path = os.path.join(audio_folder, f"{number}.mp3")
    print(audio_path)

    if os.path.exists(audio_path):
        print(f"[INFO] Playing audio: {audio_path}")
                
                # Initialize the Pygame mixer
        pygame.mixer.init()
                
                # Load the audio file
        pygame.mixer.music.load(audio_path)
                
                # Play the audio
        pygame.mixer.music.play()
                
                # Wait until the audio is done
        while pygame.mixer.music.get_busy():  # Check if the music is still playing
            time.sleep(1)  # Sleep for a second to avoid high CPU usage
    else:
        print(f"[WARNING] No audio file found for number: {number}")



if __name__ == "__main__":
    print(f"📂 Monitoring folder: {watched_folder}")
    
    while True:
        image_path = get_latest_image(watched_folder)
        
        if image_path:
            print(f"🔍 Processing image: {image_path}")
            detected_number = draw_boxes(image_path)

            # Audio
            if detected_number:
                play_audio(detected_number)  # Play corresponding audio

            # Whatsapp message
            numero = "+351913444742"  # Número de telefone do destinatário (com código internacional)
            mensagem = f"Alerta do sistema: o número lido foi {detected_number}!"
            # Envia a mensagem no horário programado
            kit.sendwhatmsg_instantly(numero, mensagem, tab_close=True)

            # Move processed image to 'processed' folder
            new_path = os.path.join(processed_folder, os.path.basename(image_path))
            os.rename(image_path, new_path)

        time.sleep(2)  # Wait 2 seconds before checking again
