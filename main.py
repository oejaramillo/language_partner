from openai import OpenAI
import speech_recognition as sr
import tempfile
from playsound import playsound
import os
import json


# Openai credentials
openai_client = OpenAI(api_key='')

class escuchar:
    def __init__(self, modelo, reconocedor=sr.Recognizer()):
        self.modelo = modelo
        self.reconocedor = reconocedor

    def reconocimiento(self):
        with sr.Microphone() as source:
            print("Escuchando...") # debug
            self.audio = self.reconocedor.listen(source=source)        

    def archivo_temporal(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmpfile:
            self.tmpfile_nombre = tmpfile.name
            tmpfile.write(self.audio)

    def transcripcion(self):
        with open(self.tmpfile_nombre, 'rb') as audio_file:
            self.respuesta = openai_client.audio.transcriptions.create(
                model=self.modelo,
                file=audio_file,
                response_format="text"
            )
        os.remove(self.tmpfile_nombre)


class pensar:
    def __init__(self, modelo, texto, temperatura=0):
        self.texto = f'conversaciones/{texto}.json'
        with open(self.texto, 'r') as file:
            prompts = json.load(file)
        
        self.prompts = prompts
        self.modelo = modelo
        self.temperatura = temperatura

    def procesar(self, user_prompt):
        if openai_client is None:
            raise Exception("Fallo en el cliente, revisar la clave de la API")
        
        self.prompts.append({"role":"user", "content": f"{user_prompt}"})
        self.respuesta = openai_client.chat.completions.create(
            model=self.modelo,
            messages=self.prompts,
            temperature=self.temperatura
        )

        self.reply = self.respuesta.choices[0].message.content
        self.respuesta = {"role":"assistant", "content": f"{self.reply}"}
        self.prompts.append(self.respuesta)

    def memoria(self):
        with open(self.texto, 'w') as file:
            json.dump(self.prompts, file, indent=4)

class hablar:
    def __init__(self, modelo, voz):
        self.modelo = modelo
        self.voz = voz

    def procesar(self, reply):
        self.respuesta = openai_client.audio.speech.create(
            model=self.modelo,
            voice=self.voz,
            input=reply
        )

    def archivo_temporal(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmpfile:
            self.tmpfile_nombre = tmpfile.name
            tmpfile.write(self.respuesta.content)

    def hablar(self):
        playsound(self.tmpfile_nombre)

    




    







    
