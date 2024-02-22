from openai import OpenAI
import os
import json
import requests
import base64

# OpenAI api request


def openai_call():
    openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    MODEL = "gpt-3.5-turbo"
    try:
        response = openai_client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Knock knock."},
                {"role": "assistant", "content": "Who's there?"},
                {"role": "user", "content": "Orange."},
            ],
            temperature=0,
        )
        reply = response.choices[0].message.content
        print(reply)
    except Exception as e:
        print(f"An error occurred: {e}")


# Stability api request
def stability_call(folder, endpoint):
    api_host = os.getenv('API_HOST', 'https://api.stability.ai')
    url = f"{api_host}/v1/{folder}/{endpoint}"

    api_key = os.getenv("STABILITY_API_KEY")
    if api_key is None:
        raise Exception("Missing Stability API key.")

    response = requests.get(url, headers={
        "Authorization": f"Bearer {api_key}"
    })

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    payload = response.json()
    return payload

# Stability texto a imagen
def texto_a_imagen(prompt, height, width, samples, steps, engine_id):
    api_host = os.getenv('API_HOST', 'https://api.stability.ai')
    api_key = os.getenv("STABILITY_API_KEY")
    
    if api_key is None:
        raise Exception("Missing Stability API key.") 

    response = requests.post(
        f"{api_host}/v1/generation/{engine_id}/text-to-image",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        json={
            "text_prompts": [
                {
                    "text": prompt
                }
            ],
            "cfg_scale": 7,
            "height": height,
            "width": width,
            "samples": samples,
            "steps": steps,
        },)

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))
    print(prompt)

    payload = response.json()
    return payload

def guarda_imagen(payload):
    if not payload['artifacts']:
        raise Exception("No artifacts found in payload.")
    
    # Extrae el texto base64 
    artifacts = payload['artifacts'][0]
    imagen_base64 = artifacts['base64']
    
    # Decode el base64
    imagen = base64.b64decode(imagen_base64)
    
    # Guarda la imagen en un archivo
    with open("imagen.png", "wb") as f:
        f.write(imagen)
    print("Imagen guardada de forma exitosa")

#payload = texto_a_imagen("A duck in a park", 1024, 1024, 1, 30, 'stable-diffusion-v1-6')
#guarda_imagen(payload=payload)
payload = stability_call('engines', 'list')

print(payload)

