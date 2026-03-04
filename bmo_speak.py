from gtts import gTTS
import pygame
import os
import time

def bmo_speak(text):
    print(f"BMO: {text}")
    try:
        # 1. Buat file suara
        tts = gTTS(text=text, lang='en')
        filename = f"bmo_{int(time.time())}.mp3" # Nama file unik agar tidak konflik
        tts.save(filename)
        
        # 2. Inisialisasi audio
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        
        # 3. Tunggu sampai selesai bicara
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        # 4. HENTIKAN & UNLOAD (Penting agar suara selanjutnya bisa bunyi)
        pygame.mixer.music.stop()
        pygame.mixer.quit() 
        
        # 5. Hapus file sementara
        if os.path.exists(filename):
            os.remove(filename)
    except Exception as e:
        print(f"Gagal mengeluarkan suara: {e}")