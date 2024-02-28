from pathlib import Path
from openai import OpenAI

client = OpenAI()

# Define the path for the output file
speech_file_path = Path(__file__).parent / "speech.mp3"

# Create the audio transcription or synthesis
response = client.audio.speech.create(
  model="tts-1",
  voice="nova",
  input="Today is a wonderful day to build something people love!"
)

# Assuming the response.content holds the binary data of the generated speech
with open(speech_file_path, 'wb') as file:
    file.write(response.content)

