import os
import pygame
from gtts import gTTS
from pydub import AudioSegment
from rvc_python.infer import RVCInference

# Inisialisasi (Letakkan di luar fungsi agar tidak reload model setiap saat)
rvc = RVCInference(device="cuda:0") 
rvc.load_model("models/BMO.pth", "v2", None)

def bmo_speak_rvc(text):
    print(f"BMO: {text}")
    try:
        # 1. Generate TTS dasar
        temp_mp3 = "temp_input.mp3"
        temp_wav = "temp_input.wav"
        output_rvc = "bmo_final.wav"
        
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(temp_mp3)
        
        # 2. Konversi ke WAV murni (Format 16-bit, 22050Hz adalah yang paling stabil untuk RVC)
        audio = AudioSegment.from_mp3(temp_mp3)
        audio = audio.set_frame_rate(22050).set_channels(1) # Paksa ke Mono & Rate standar
        audio.export(temp_wav, format="wav")
        
        # 3. Atur Parameter RVC (Tanpa underscore sesuai hasil dir() Anda)
        rvc.f0up_key = 12
        rvc.f0method = "rmvpe"
        
        # 4. Inferensi (Kirim path file yang sudah dikonversi pydub)
        # Jangan panggil wavfile.read secara manual di sini
        rvc.infer_file(temp_wav, output_rvc)
        
        # 5. Playback
        pygame.mixer.init()
        if os.path.exists(output_rvc):
            pygame.mixer.music.load(output_rvc)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            pygame.mixer.music.stop()
        pygame.mixer.quit()
        
        # Cleanup
        for f in [temp_mp3, temp_wav]:
            if os.path.exists(f): os.remove(f)
            
    except Exception as e:
        print(f"Gagal mengeluarkan suara BMO: {e}")