
import requests
import speech_recognition as sr
import os

API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
hugging_face_token = os.getenv("HUGGING_FACE_TOKEN")
headers = {"Authorization": f"Bearer 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"}

recognizer = sr.Recognizer()
with sr.Microphone() as source:
    print("Listening...")
    audio = recognizer.listen(source)
    try:
        response = requests.post(API_URL, headers=headers, data=audio)
    except sr.RequestError as e:
         print(f"Error: {e}")
    except sr.UnknownValueError:
          print("Error")
         
print(response)