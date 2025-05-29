import tkinter as tk
from threading import Thread
import time
import pytesseract
import cv2
import mss
import win32gui
import win32con
import win32api

class OverlayRenderer:
    def __init__(self):
        print("[DEBUG] Initializing Overlay Window...")
        self.root = tk.Tk()
        self.root.title("Real-Time AI Overlay")
        self.root.geometry("800x600+50+50")
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.85)  # Slightly less transparent
        self.root.configure(bg='#2e2e2e')  # Soft Grey Background
        
        print("[DEBUG] Setting up main frame...")
        self.frame = tk.Frame(self.root, bg='#2e2e2e')
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Header Label
        print("[DEBUG] Adding header label...")
        self.header_label = tk.Label(self.frame, text='Live AI Overlay', fg='#FFFFFF', bg='#424242',
                                     font=('Roboto', 16, 'bold'))
        self.header_label.pack(pady=10)

        # Screen OCR Section
        print("[DEBUG] Adding Screen OCR Section...")
        self.ocr_label = tk.Label(self.frame, text='Screen OCR Output', fg='#FFFFFF', bg='#424242',
                                  font=('Roboto', 14, 'bold'))
        self.ocr_label.pack(pady=5)

        self.ocr_text = tk.Text(self.frame, height=8, width=95, bg='#616161', fg='#e0e0e0',
                                font=('Roboto', 12))
        self.ocr_text.pack(pady=5)

        # Audio Transcription Section
        print("[DEBUG] Adding Audio Transcription Section...")
        self.audio_label = tk.Label(self.frame, text='Audio Transcription Output', fg='#FFFFFF', bg='#424242',
                                    font=('Roboto', 14, 'bold'))
        self.audio_label.pack(pady=5)

        self.audio_text = tk.Text(self.frame, height=8, width=95, bg='#616161', fg='#e0e0e0',
                                  font=('Roboto', 12))
        self.audio_text.pack(pady=5)

        print("[DEBUG] Overlay initialized successfully.")
        
        # Set window as click-through and non-capturable
        print("[DEBUG] Setting window to Click-Through and Non-Capturable Mode...")
        self.root.update_idletasks()
        hwnd = win32gui.FindWindow(None, "Real-Time AI Overlay")
        
        # Set window styles
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                               win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) |
                               win32con.WS_EX_LAYERED |
                               win32con.WS_EX_TRANSPARENT |
                               win32con.WS_EX_NOACTIVATE |
                               win32con.WS_EX_TOOLWINDOW)
        
        # Set Display Affinity (Non-Capturable)
        try:
            win32gui.SetWindowDisplayAffinity(hwnd, 1)  # 1 = WDA_MONITOR, makes it non-capturable
            print("[DEBUG] Window set to non-capturable successfully.")
        except Exception as e:
            print(f"[ERROR] Could not set window to non-capturable: {e}")

    def update_ocr_text(self, new_text):
        print("[DEBUG] Updating OCR Text...")
        self.ocr_text.delete('1.0', tk.END)
        self.ocr_text.insert(tk.END, new_text)

    def update_audio_text(self, new_text):
        print("[DEBUG] Updating Audio Transcription Text...")
        self.audio_text.delete('1.0', tk.END)
        self.audio_text.insert(tk.END, new_text)

    def start_ocr_listener(self):
        print("[DEBUG] Starting OCR Listener Thread...")
        ocr_thread = Thread(target=self.listen_ocr)
        ocr_thread.start()

    def listen_ocr(self):
        print("[DEBUG] Listening for OCR Text...")
        with mss.mss() as sct:
            monitor = sct.monitors[1]  # Fullscreen capture
            while True:
                screenshot = sct.grab(monitor)
                img = cv2.cvtColor(screenshot.rgb, cv2.COLOR_BGR2GRAY)
                text = pytesseract.image_to_string(img)
                if text.strip():
                    self.update_ocr_text(text)
                else:
                    self.update_ocr_text("[No Text Detected]")
                time.sleep(2)

    def start(self):
        print("[DEBUG] Starting Main Loop...")
        self.start_ocr_listener()
        self.root.mainloop()
 



