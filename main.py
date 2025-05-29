import cv2
import pytesseract
import hashlib
import time
import threading
import speech_recognition as sr
import mss
import numpy as np

# Set up pytesseract path if needed (Uncomment if necessary)
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Global Variables
last_hash = ""
capture_interval = 0.5  # 500ms
recognizer = sr.Recognizer()
microphone = sr.Microphone()
transcription_interval = 0.5  # 500ms
silence_threshold = 1.5  # 1.5 seconds of silence triggers the end of transcription
last_transcription = ""

def compute_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()

def capture_screen():
    global last_hash
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Primary monitor
        while True:
            # Capture the screen
            screenshot = np.array(sct.grab(monitor))
            gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

            # Extract text
            text = pytesseract.image_to_string(gray)

            # Hash the current screen text
            current_hash = compute_hash(text)

            # If hash has changed, display the new text
            if current_hash != last_hash:
                last_hash = current_hash
                print("Screen Text Updated:")
                print(text)
            
            # Wait before next capture
            time.sleep(capture_interval)

def listen_microphone():
    global last_transcription
    with microphone as source:
        print("Calibrating microphone... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=2)
        print("Microphone calibrated. Listening...")

    while True:
        with microphone as source:
            print("Listening for speech...")
            try:
                audio = recognizer.listen(source, timeout=5)
                print("Processing audio...")
                transcription = recognizer.recognize_google(audio)
                
                # Only update if the transcription is new
                if transcription != last_transcription:
                    last_transcription = transcription
                    print(f"Audio Transcription Updated: {transcription}")

            except sr.WaitTimeoutError:
                print("Listening timed out. No speech detected.")
            except sr.UnknownValueError:
                print("Could not understand audio.")
            except Exception as e:
                print(f"Error during transcription: {e}")
        
        # Small delay before the next listen cycle
        time.sleep(transcription_interval)

# Initialize threads for screen capture and audio transcription
screen_thread = threading.Thread(target=capture_screen)
audio_thread = threading.Thread(target=listen_microphone)

# Start both threads
print("Starting Real-Time Screen Capture and Audio Transcription...")
screen_thread.start()
audio_thread.start()

# Join threads to keep the main thread alive
screen_thread.join()
audio_thread.join()