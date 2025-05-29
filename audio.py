import speech_recognition as sr
import threading
import time

# Global Variables
recognizer = sr.Recognizer()
microphone = sr.Microphone()
transcription_interval = 0.5  # 500ms
silence_threshold = 1.5  # 1.5 seconds of silence triggers the end of transcription
last_transcription = ""

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
                    print(f"Transcription Updated: {transcription}")

            except sr.WaitTimeoutError:
                print("Listening timed out. No speech detected.")
            except sr.UnknownValueError:
                print("Could not understand audio.")
            except Exception as e:
                print(f"Error during transcription: {e}")
        
        # Small delay before the next listen cycle
        time.sleep(transcription_interval)

# Start the transcription in a separate thread
t = threading.Thread(target=listen_microphone)
t.start()
