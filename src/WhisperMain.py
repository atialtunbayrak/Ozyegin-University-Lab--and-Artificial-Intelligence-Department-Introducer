import requests
import json
import time
from groq import Groq
import speech_recognition as sr
from playsound import playsound
import os
from dotenv import load_dotenv, find_dotenv


NEON_GREEN = "\033[92m"
NEON_RED = '\033[91m'
RESET_COLOR = "\033[0m"
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

url = 'http://localhost:3000/conversation'  # URL of the server endpoint
load_dotenv(".env")

transcribeClient = Groq(api_key=os.getenv("GROQ_API_KEY"))

def transcribe_audio(temp_chunk):
        
    filename = temp_chunk

    with open(filename, "rb") as file:
        
        translation = transcribeClient.audio.transcriptions.create(
        file=(filename, file.read()),
        model="whisper-large-v3",
        prompt="Specify context or spelling. Turkish.",
        response_format="json",  
        language="tr",
        temperature=0.0
        )
        return translation.text

def record_until_speech_ends(file_path, playstart = True):
    with sr.Microphone() as source:
        print("Listening:\t")

        if playstart:
            playsound("sounds/siriin.wav")
        recognizer = sr.Recognizer() 
        recognizer.non_speaking_duration
        audio = recognizer.listen(source, timeout = 60)

        with open(file_path, "wb") as f:
            f.write(audio.get_wav_data())        

        print("Speech Recorded")

def main():
    accumulated_transcription = ""
    is_altyaziMK = False
    try:

        while True:
            
            chunk_file = "/tmp/temp_chunk.wav"
            if not is_altyaziMK:
                record_until_speech_ends(chunk_file,not is_altyaziMK)
            else:
                record_until_speech_ends(chunk_file,not is_altyaziMK)
                is_altyaziMK=False
            print("transcribing...")
            transcription = transcribe_audio(chunk_file)
            
            #This if statement differantiates the noise generated by Whispher and the actual transcription for Turkish
            if transcription and transcription.strip() != "Evet." and  transcription.strip() != "Türk." and transcription.strip()!="..." and transcription.strip() != "Türkçe." and transcription.strip()!="Türkçe" and transcription.strip() != "Altyazı M.K" and transcription.strip()!="İzlediğiniz için teşekkür ederim."and transcription.strip() !="İzlediğiniz için teşekkürler." and transcription.strip() != "İzlediğiniz için teşekkürler" and "M.K." not in transcription.strip() and "ABONE OLMAYI UNUTMAYIN" not in transcription.strip():
                
                playsound('sounds/siriout.wav')
                is_altyaziMK=False

                print("Understood and passed Filter:"+ NEON_GREEN + transcription + RESET_COLOR)
                accumulated_transcription += transcription + " "

                
                #Sending the the transcription to the server
                data = {"context":transcription, "time":time.time()}
                print("Sending data to server...")
                response = requests.post(url, json=data)
                
                if response.status_code == 200: #
                    print("Whispher got response from server, continuing to listen...")
                    print(json.dumps(response.json(), indent=4))
                else:
                    pass
                    print(f"Failed to get a response, continuing anyway. Status code: {response.status_code}")
            else:
                print(f"Understood and Filtered: {NEON_RED}{transcription}{RESET_COLOR}")
                is_altyaziMK = True
            os.remove(chunk_file)

    except KeyboardInterrupt:
        print("Stopping...")

    finally:
        print("LOG:" + accumulated_transcription)

if __name__ == "__main__":
    main()