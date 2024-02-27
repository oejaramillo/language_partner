from gtts import gTTS
import os

text_to_speak = "Hello, this is a response from your language model."
tts = gTTS(text=text_to_speak, lang='en')
tts.save("response.mp3")
os.system("mpg321 response.mp3")
