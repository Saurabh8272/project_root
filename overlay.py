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
        self.root.title("Real-Time AI Overlay Manager")
        self.root.geometry("300x400+100+100")
        self.root.configure(bg='#2e2e2e')
        
        print("[DEBUG] Setting up main frame...")
        self.frame = tk.Frame(self.root, bg='#2e2e2e')
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Header Label
        self.header_label = tk.Label(self.frame, text='Overlay Manager', fg='#FFFFFF', bg='#424242',
                                     font=('Roboto', 16, 'bold'))
        self.header_label.pack(pady=10)

        # Start Overlay Button
        self.start_button = tk.Button(self.frame, text='Start Overlay', command=self.start_overlay,
                                      fg='#FFFFFF', bg='#424242', font=('Roboto', 12, 'bold'))
        self.start_button.pack(pady=10)

        # Stop Overlay Button
        self.stop_button = tk.Button(self.frame, text='Stop Overlay', command=self.stop_overlay,
                                     fg='#FFFFFF', bg='#424242', font=('Roboto', 12, 'bold'))
        self.stop_button.pack(pady=10)

        # Settings Button
        self.settings_button = tk.Button(self.frame, text='Settings', command=self.open_settings,
                                         fg='#FFFFFF', bg='#424242', font=('Roboto', 12, 'bold'))
        self.settings_button.pack(pady=10)

        # Status Label
        self.status_label = tk.Label(self.frame, text='Status: Stopped', fg='#FFFFFF', bg='#2e2e2e',
                                     font=('Roboto', 12))
        self.status_label.pack(pady=20)

        # Overlay Instance
        self.overlay_window = None

    def start_overlay(self):
        if not self.overlay_window:
            self.overlay_window = Thread(target=self.launch_overlay)
            self.overlay_window.start()
            self.status_label.config(text="Status: Running")
            print("[DEBUG] Overlay started.")

    def stop_overlay(self):
        if self.overlay_window:
            print("[DEBUG] Stopping overlay...")
            win32api.PostMessage(win32gui.FindWindow(None, "Real-Time AI Overlay"), win32con.WM_CLOSE, 0, 0)
            self.overlay_window = None
            self.status_label.config(text="Status: Stopped")

    def open_settings(self):
        print("[DEBUG] Opening settings window...")
        # Placeholder for settings window

    def launch_overlay(self):
        print("[DEBUG] Launching Overlay...")
        overlay = tk.Toplevel(self.root)
        overlay.title("Real-Time AI Overlay")
        overlay.geometry("800x600+150+150")
        overlay.attributes('-topmost', True)
        overlay.attributes('-alpha', 0.85)
        overlay.configure(bg='#2e2e2e')
        
        # Header
        header = tk.Label(overlay, text='Live AI Overlay', fg='#FFFFFF', bg='#424242',
                          font=('Roboto', 16, 'bold'))
        header.pack(pady=10)

        # Screen OCR Section
        ocr_label = tk.Label(overlay, text='Screen OCR Output', fg='#FFFFFF', bg='#424242',
                             font=('Roboto', 14, 'bold'))
        ocr_label.pack(pady=5)

        ocr_text = tk.Text(overlay, height=8, width=95, bg='#616161', fg='#e0e0e0',
                           font=('Roboto', 12))
        ocr_text.pack(pady=5)

        # Audio Transcription Section
        audio_label = tk.Label(overlay, text='Audio Transcription Output', fg='#FFFFFF', bg='#424242',
                               font=('Roboto', 14, 'bold'))
        audio_label.pack(pady=5)

        audio_text = tk.Text(overlay, height=8, width=95, bg='#616161', fg='#e0e0e0',
                             font=('Roboto', 12))
        audio_text.pack(pady=5)

        overlay.mainloop()

    def start(self):
        print("[DEBUG] Starting Main Manager Window...")
        self.root.mainloop()
