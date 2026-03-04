import speech_recognition as sr
import ollama
import threading
from bmo_visual import BMOFace
from bmo_speak_piper import bmo_speak_piper

# 1. Satu-satunya Inisialisasi Wajah
face = BMOFace()
face_thread = threading.Thread(target=face.draw, daemon=True)
face_thread.start()

def listen_to_user():
    r = sr.Recognizer()
    r.energy_threshold = 400 
    r.dynamic_energy_threshold = True
    r.pause_threshold = 0.5 # Respons cepat
    
    with sr.Microphone() as source:
        face.set_state("LISTENING") # Wajah antusias mendengar
        print("\n[BMO sedang mendengarkan...]")
        try:
            audio = r.listen(source, timeout=5)
            face.set_state("IDLE")
            text = r.recognize_google(audio, language="id-ID")
            print(f"Kamu: {text}")
            return text
        except:
            face.set_state("IDLE")
            return None

def chat_with_bmo():
    bmo_speak_piper("Hello Friend! I am BMO.", face)
    
    while True:        
        user_input = listen_to_user()
        
        if user_input:
            if "dadah" in user_input.lower() or "bye" in user_input.lower():
                bmo_speak_piper("See you friends!", face)
                break
                
            # Berpikir
            face.set_state("THINKING") # Wajah mikir
            response = ollama.chat(model='bmo-model', messages=[
                {'role': 'user', 'content': user_input},
            ])
            
            bmo_answer = response['message']['content']
            # Bicara
            bmo_speak_piper(bmo_answer, face)

if __name__ == "__main__":
    chat_with_bmo()