from openai import OpenAI
import os
import json

# OpenAI api request
openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
MODEL = "gpt-3.5-turbo"

conversacion = 'conversacion.json'

with open(conversacion, 'r') as file:
    prompts = json.load(file)


def openai_call(prompts):
    if openai_client is None:
        raise Exception("Fallo en el cliente, revisar la clave para la API")
    
    response = openai_client.chat.completions.create(
        model=MODEL,
        messages=prompts,
        temperature=0,
    )
    
    reply = response.choices[0].message.content
    respuesta = {"role":"assistant", "content": f"{reply}"}
    prompts.append(respuesta)
    print("IA: ", reply)

print("Empieza la conversacion: \n")
while True:
    mensaje = input("Tu: ")
    if mensaje.lower() == 'salir':
        break

    nuevo_mensaje = {"role": "user", "content": f"{mensaje}"}
    prompts.append(nuevo_mensaje)

    openai_call(prompts=prompts)

conversacion = 'conversacion.json'
with open(conversacion, 'w') as file:
    json.dump(prompts, file, indent=4)
