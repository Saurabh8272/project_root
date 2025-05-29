import cv2
import pytesseract
import hashlib
import time
import threading

# Set up pytesseract path if needed (Uncomment if necessary)
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Global Variables
last_hash = ""
capture_interval = 0.5  # 500ms
screen_region = (0, 0, 1920, 1080)  # Full HD screen capture

def compute_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()

def capture_screen():
    global last_hash
    while True:
        # Capture the screen
        screenshot = cv2.cvtColor(cv2.imread('screenshot.png'), cv2.COLOR_BGR2GRAY)

        # Extract text
        text = pytesseract.image_to_string(screenshot)

        # Hash the current screen text
        current_hash = compute_hash(text)

        # If hash has changed, display the new text
        if current_hash != last_hash:
            last_hash = current_hash
            print("Text Updated:")
            print(text)
        
        # Wait before next capture
        time.sleep(capture_interval)

# Start the screen capture in a separate thread
t = threading.Thread(target=capture_screen)
t.start()
