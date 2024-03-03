from pathlib import Path
from openai import OpenAI

client = OpenAI()

# Define the path for the output file
speech_file_path = Path(__file__).parent / "speech.mp3"

# Create the audio transcription or synthesis
response = client.audio.speech.create(
  model="tts-1",
  voice="nova",
  input="My beloved people, Today, as we gather under the vast sky that blankets our kingdom, I stand before you not as a ruler towering above, but as a servant among equals, united in purpose and heart. Our land, rich in history and courage, has weathered storms and basked in the glory of dawn, each day woven into the fabric of our shared destiny. We stand on the shoulders of giants, ancestors who sowed the seeds of our prosperity with their sweat and blood. Their whispers in the wind remind us of the resilience that defines us, the strength that courses through our veins, and the collective spirit that has carried us through the ages. But let us not dwell solely on the past, for our gaze must also be fixed on the horizon, toward a future as bright as the stars that guide our night. Our journey is far from over. It is a path we must walk together, hand in hand, forging ahead with unwavering faith in one another. To the farmers who till our land, to the artisans who bring beauty into our world, to the scholars who ignite the flame of knowledge, and to the young ones, our hope and joy—each of you is a pillar upon which our kingdom stands. Your dreams and aspirations fuel our collective journey forward. In times of challenge, let us remember the bonds that unite us—stronger than the mightiest fortress. In moments of doubt, let us recall our shared victories, large and small, that have lit the way through the darkest nights. As your king, I pledge to lead with compassion, to listen with an open heart, and to serve with dedication, honoring the trust you have placed in me. Together, let us build a legacy that will echo through the ages, a testament to what we can achieve when united in purpose and spirit. For we are more than a kingdom; we are a family, bound by love and loyalty, and it is together that we will forge our path to a future resplendent with possibility. Long may our kingdom prosper, and long may the bonds of our brotherhood and sisterhood remain unbreakable. Together, we shall rise."
)

# Assuming the response.content holds the binary data of the generated speech
with open(speech_file_path, 'wb') as file:
    file.write(response.content)

