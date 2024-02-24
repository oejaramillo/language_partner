import os
import json
import requests
import base64

api_host = os.getenv('API_HOST', 'https://api.stability.ai')
api_key = os.getenv("STABILITY_API_KEY")

# Stability api request
def stability_call(folder, endpoint):
    url = f"{api_host}/v1/{folder}/{endpoint}"

    if api_key is None:
        raise Exception("No hay clave para la API")

    response = requests.get(url, headers={
        "Authorization": f"Bearer {api_key}"
    })

    if response.status_code != 200:
        raise Exception("Respuesta no exitosa, !=200: " + str(response.text))

    payload = response.json()
    return payload

def guarda_imagen(payload):
    for i, imagen in enumerate(payload['artifacts']):
        with open(f"imagen_{i}.png", "wb") as f:
            f.write(base64.b64decode(imagen["base64"]))
    
    print("Imagen guardada de forma exitosa")

# Stability texto a imagen
def texto_a_imagen(prompt, height, width, samples, steps, engine_id):    
    if api_key is None:
        raise Exception("No hay clave para la API") 

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
        raise Exception("Respuesta no exitosa, !=200: " + str(response.text))

    payload = response.json()
    guarda_imagen(payload=payload)
    balance = stability_call("user", "balance")
    print("Quedan ", balance['credits'], " créditos.")

print("¿Qué imágen quieres generar?\n")
prompt = input()

texto_a_imagen(prompt=prompt, height=1024, width=1024, samples=1, steps=30, engine_id="stable-diffusion-v1-6")