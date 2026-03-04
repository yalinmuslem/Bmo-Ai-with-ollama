import os
import time
import pygame
import torch
import re                    # Tambahkan ini
import numpy as np           # Tambahkan ini
from scipy.io import wavfile # Tambahkan ini
from piper.voice import PiperVoice
from rvc_python.infer import RVCInference

# --- BYPASS SECURITY PYTORCH ---
import torch.serialization
original_load = torch.load
torch.load = lambda *args, **kwargs: original_load(*args, **kwargs, weights_only=False)

# --- CONFIG ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PIPER = os.path.join(BASE_DIR, "models", "en_US-amy-low.onnx")
MODEL_RVC = os.path.join(BASE_DIR, "models", "BMO.pth")
INDEX_RVC = os.path.join(BASE_DIR, "models", "BMO.index")

# Inisialisasi (Hanya sekali)
voice = PiperVoice.load(MODEL_PIPER)
rvc = RVCInference(device="cuda:0")
rvc.load_model(MODEL_RVC, "v2", INDEX_RVC)

def sanitize_bmo_text(text):
    # Menghapus teks di dalam tanda kurung atau tanda bintang (gestur/aksi)
    # Contoh: "Halo! *tersenyum*" -> "Halo!"
    text = re.sub(r'\*.*?\*', '', text)
    text = re.sub(r'\(.*?\)', '', text)
    
    # Menghapus karakter Markdown lainnya (seperti # atau _)
    text = text.replace('#', '').replace('_', '')
    
    # Membersihkan spasi berlebih
    return " ".join(text.split()).strip()

def bmo_speak_piper(text):
    clean_text = sanitize_bmo_text(text)

    if not clean_text:
        return

    print(f"BMO (Original): {text}")
    print(f"BMO (Speaking): {clean_text}")

    input_wav = os.path.join(BASE_DIR, "piper_output.wav")
    final_wav = os.path.join(BASE_DIR, "bmo_final.wav")

    try:
        # 1. GENERATE SUARA DENGAN PIPER (Alternatif Numpy)
        audio_data = []
        for chunk in voice.synthesize(clean_text):
            # Ambil buffer mentah dari objek AudioChunk
            # print(f"Isi chunk: {dir(chunk)}")
            raw_data = chunk.audio_int16_bytes
            
            # Konversi ke numpy array
            data = np.frombuffer(raw_data, dtype=np.int16)
            audio_data.append(data)
        
            
        if not audio_data:
            raise ValueError("Piper tidak menghasilkan data audio.")

        # Gabungkan semua chunk dan simpan sebagai WAV
        final_audio = np.concatenate(audio_data)
        wavfile.write(input_wav, 16000, final_audio)
        
        # Jeda sinkronisasi file sistem
        time.sleep(0.2)

        # 2. RVC CONVERSION
        rvc.f0up_key = 12
        rvc.f0method = "rmvpe"
        rvc.infer_file(input_wav, final_wav)

        # 3. PLAYBACK
        pygame.mixer.init()
        pygame.mixer.music.load(final_wav)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.music.stop()
        pygame.mixer.quit()

    except Exception as e:
        print(f"BMO Error: {e}")