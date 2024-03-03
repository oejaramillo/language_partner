from openai import OpenAI
import speech_recognition as sr
import tempfile
from playsound import playsound
import os
import json


# Openai credentials
openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

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
            tmpfile.write(self.audio.get_wav_data())

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
        
def conversar(modelo_escuchar, modelo_pensar, prompt_inicial, modelo_hablar, voz):
    oido = escuchar(modelo_escuchar)
    cerebro = pensar(modelo_pensar, prompt_inicial)
    boca = hablar(modelo_hablar, voz)
    
    while True:
        oido.reconocimiento()
        oido.archivo_temporal()
        oido.transcripcion()

        if oido.respuesta.lower() == "Salir":
            break
        print("Se escucho: ", oido.respuesta) # debug

        cerebro.procesar(oido.respuesta)
        print("El modelo responde: ", cerebro.reply) # debug
        cerebro.memoria()

        boca.procesar(cerebro.reply)
        boca.archivo_temporal()
        boca.hablar()

conversar(modelo_escuchar="whisper-1", modelo_pensar="gpt-3.5-turbo", prompt_inicial='conversacion', modelo_hablar="tts-1", voz="nova")







    







    
