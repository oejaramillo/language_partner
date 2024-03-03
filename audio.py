import speech_recognition as sr
import os
import tempfile
from openai import OpenAI

client = OpenAI(
  #api_key=os.environ['OPENAI_API_KEY'],  # this is also the default, it can be omitted
)

recognizer = sr.Recognizer()
with sr.Microphone() as source:
    print("Listening...")
    audio = recognizer.listen(source)

    # Save the audio to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmpfile:
        tmpfile_name = tmpfile.name
        # Write the WAV data to the file
        tmpfile.write(audio.get_wav_data())
    
    try:
        # Now, use the OpenAI client to create a transcription
        with open(tmpfile_name, 'rb') as audio_file:
            response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )
        # Print the transcription text
        print(response)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Clean up the temporary file
        os.remove(tmpfile_name)
