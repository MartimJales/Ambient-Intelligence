import os
import time
import cv2
import pytesseract
import pywhatkit as kit
# import win32api
import contextlib
with open(os.devnull, 'w') as fnull:
    with contextlib.redirect_stdout(fnull), contextlib.redirect_stderr(fnull):
        import pygame
        import easyocr
import sqlite3

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# Set up directories
watched_folder = "received_images"
processed_folder = "processed_images"
audio_folder = "audio_files"
box_folder = os.path.join(processed_folder, "Box")

# Ensure 'Box' directory exists
os.makedirs(box_folder, exist_ok=True)

def get_latest_image(folder):
    """Returns the latest image file from the folder, or None if no images exist."""
    files = [f for f in os.listdir(folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    if not files:
        return None

    latest_file = max(files, key=lambda f: os.path.getctime(os.path.join(folder, f)))
    return os.path.join(folder, latest_file)

def draw_boxes(image_path, iteration=1):
    """Detects numbers in an image, draws bounding boxes, and saves a new image in 'Box' folder."""
    img = cv2.imread(image_path)
    if img is None:
        print(f"[ERROR] Failed to read image: {image_path}")
        return None

    # Initialize the EasyOCR reader (you can specify the language here, e.g., 'en' for English)
    with open(os.devnull, 'w') as fnull:
        with contextlib.redirect_stdout(fnull), contextlib.redirect_stderr(fnull):
            reader = easyocr.Reader(['en'])
    results = reader.readtext(image_path)

    detected_numbers = []

    for result in results:
        bbox, text, confidence = result
        if text.isdigit():
            detected_numbers.append(text)
            # Draw bounding box
            (top_left, top_right, bottom_right, bottom_left) = bbox
            top_left = tuple(map(int, top_left))
            bottom_right = tuple(map(int, bottom_right))
            cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 2)
            cv2.putText(img, text, (top_left[0], top_left[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    if detected_numbers:
        detected_number = detected_numbers[0]  # Taking the first detected number
        print(f"[INFO] Detected number: {detected_number}")

        # Save the processed image with the bounding box in 'Box' folder
        new_image_name = f"{detected_number}_{iteration}.jpg"
        new_image_path = os.path.join(box_folder, new_image_name)
        cv2.imwrite(new_image_path, img)

        return detected_number, new_image_path
    else:
        print("[INFO] No numbers detected.")
        return None, None



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

def obter_numeros_da_base_dados(caminho_db="contactos.db"):
    conn = sqlite3.connect(caminho_db)
    cursor = conn.cursor()
    cursor.execute("SELECT numero FROM contactos")
    resultados = cursor.fetchall()
    conn.close()
    return [numero[0] for numero in resultados]

def enviar_mensagem_para_contactos(detected_number, caminho_db="contactos.db"):
    """Envia mensagem apenas para contactos interessados no autocarro detectado."""
    try:
        conn = sqlite3.connect(caminho_db)
        cursor = conn.cursor()
        cursor.execute("SELECT nome, numero, autocarros FROM contactos")
        contactos = cursor.fetchall()
        conn.close()

        for nome, numero, autocarros_str in contactos:
            if not autocarros_str:
                continue  # se estiver vazio, ignora

            autocarros = [x.strip() for x in autocarros_str.split(',')]
            if str(detected_number) not in autocarros:
                continue  # este contacto não está interessado neste autocarro

            mensagem = f"Hello {nome}, the bus number *{detected_number}* is arriving at IST :)"
            print(f"[INFO] Sending message to {nome} ({numero})")

            with open(os.devnull, 'w') as fnull:
                with contextlib.redirect_stdout(fnull), contextlib.redirect_stderr(fnull):
                    kit.sendwhatmsg_instantly(numero, mensagem, tab_close=True)

    except Exception as e:
        print(f"[ERRO] Falha ao enviar mensagens: {e}")


    except Exception as e:
        print(f"[ERRO] Falha ao enviar mensagens: {e}")

if __name__ == "__main__":
    print(f"📂 Monitoring folder: {watched_folder}")

    iteration = 1  # Track the number of processed images

    while True:
        image_path = get_latest_image(watched_folder)

        if image_path:
            print(f"🔍 Processing image: {image_path}")
            detected_number, boxed_image_path = draw_boxes(image_path, iteration)

            if detected_number:
                play_audio(detected_number)
                enviar_mensagem_para_contactos(detected_number)

            # Move original image to processed folder
            new_path = os.path.join(processed_folder, os.path.basename(image_path))
            os.rename(image_path, new_path)

            iteration += 1  # Increment iteration for unique filenames

        time.sleep(2)
