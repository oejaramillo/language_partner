import speech_recognition as sr
import threading
import sys

# Flag to control the listening loop
listening = True

def listen_continuously():
    # Initialize the recognizer
    r = sr.Recognizer()
    
    # Setup the microphone as the source
    with sr.Microphone() as source:
        # Continuously listen and perform speech recognition
        while listening:
            print("Listening for speech...")
            try:
                # Adjust the recognizer sensitivity to ambient noise
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source, timeout=5)  # Listen for the first phrase and extract it into audio data
                print("Recognizing...")
                try:
                    # Recognize speech using Google Web Speech API
                    text = r.recognize_google(audio)
                    print("You said: " + text)
                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    print(f"Could not request results from Google Speech Recognition service; {e}")
            except sr.WaitTimeoutError:
                pass  # In case of timeout just pass and continue listening

def stop_listening():
    global listening
    input("Press Enter to stop listening...\n")
    listening = False

# Start the listening thread
thread = threading.Thread(target=listen_continuously)
thread.start()

# Wait for the user to press Enter to stop listening
stop_listening()

# Wait for the listening thread to finish
thread.join()

print("Stopped listening.")

