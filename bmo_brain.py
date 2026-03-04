import time
import speech_recognition as sr
import ollama
import threading
from bmo_visual import BMOFace
from bmo_speak_piper import bmo_speak_piper

# 1. Satu-satunya Inisialisasi Wajah
face = BMOFace()
face_thread = threading.Thread(target=face.draw_loop, daemon=True)
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


def ai_logic_thread():
    """Fungsi ini berjalan di background agar tidak mengganggu visual"""
    time.sleep(2) # Beri waktu Pygame untuk muncul dulu
    bmo_speak_piper("Hello Friend! BMO is ready to play.", face)
    
    while True:
        # 1. Listen
        face.set_state("LISTENING")
        r = sr.Recognizer()
        r.pause_threshold = 0.5 # Sesuai keinginan Anda untuk respons cepat
        
        with sr.Microphone() as source:
            try:
                audio = r.listen(source, timeout=10)
                face.set_state("IDLE")
                user_input = r.recognize_google(audio, language="id-ID")
                print(f"User: {user_input}")
                
                # 2. Think
                face.set_state("THINKING")
                response = ollama.chat(model='bmo-model', messages=[
                    {'role': 'user', 'content': user_input},
                ])
                
                # 3. Speak
                bmo_answer = response['message']['content']
                bmo_speak_piper(bmo_answer, face)
                
            except Exception as e:
                face.set_state("IDLE")
                continue
                
if __name__ == "__main__":
    # Jalankan AI di BACKGROUND
    brain_thread = threading.Thread(target=ai_logic_thread, daemon=True)
    brain_thread.start()

    # Jalankan VISUAL di MAIN THREAD (Ini yang bikin tidak Not Responding)
    try:
        face.draw_loop()
    except KeyboardInterrupt:
        face.running = False
        print("BMO is shutting down...")