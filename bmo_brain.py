import speech_recognition as sr
import ollama
import pyttsx3
import torch
from bmo_speak import bmo_speak
from bmo_speak_piper import bmo_speak_piper
from bmo_speak_piper import bmo_speak_piper

# Tambahkan class fairseq ke daftar aman PyTorch
try:
    from fairseq.data.dictionary import Dictionary
    from fairseq.models.hubert.hubert import HubertModel
    torch.serialization.add_safe_globals([Dictionary, HubertModel])
except Exception:
    # Jika import gagal, gunakan cara radikal (tidak disarankan untuk produksi, tapi oke untuk lokal)
    import torch.serialization
    torch.load = lambda *args, **kwargs: torch.serialization.load(*args, **kwargs, weights_only=False)

# Inisialisasi Suara (Mulut BMO)
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# Pilih suara yang agak tinggi/anak-anak jika ada, atau biarkan default
engine.setProperty('rate', 180) 

def listen_to_user():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n[BMO sedang mendengarkan...]")
        audio = r.listen(source)
        try:
            # Menggunakan Google Speech Recognition (cepat) 
            # atau ganti ke whisper lokal jika ingin 100% offline
            text = r.recognize_google(audio, language="id-ID")
            print(f"Kamu: {text}")
            return text
        except:
            return None

def chat_with_bmo():
    bmo_speak_piper("Halo! Aku BMO. Mau main bareng?")
    
    while True:
        user_input = listen_to_user()
        
        if user_input:
            if "dadah" in user_input.lower() or "bye" in user_input.lower():
                bmo_speak_piper("Sampai jumpa teman! Aku mau main video game dulu.")
                break
                
            # Mengirim input ke Ollama (Pastikan sudah create bmo-model sebelumnya)
            response = ollama.chat(model='bmo-model', messages=[
                {'role': 'user', 'content': user_input},
            ])
            
            bmo_answer = response['message']['content']
            bmo_speak_piper(bmo_answer)

if __name__ == "__main__":
    chat_with_bmo()