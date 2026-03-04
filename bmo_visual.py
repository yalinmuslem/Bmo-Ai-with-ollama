import pygame
import random
import threading
import time

class BMOFace:
    def __init__(self):
        pygame.init()
        # Resolusi standar layar kecil (bisa disesuaikan)
        self.screen = pygame.display.set_mode((800, 480))
        pygame.display.set_caption("BMO Face")
        self.bg_color = (145, 201, 171) # Teal BMO
        self.eye_color = (30, 30, 30)
        self.state = "IDLE" # IDLE, THINKING, SPEAKING
        self.running = True
        self.mouth_open = 0

    def set_state(self, new_state):
        self.state = new_state
        
    def draw(self):
        last_blink = time.time()
        blink_duration = 0.15
        is_blinking = False

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill(self.bg_color)
            now = time.time()

            # Logika Auto-Blink
            if not is_blinking and now - last_blink > random.randint(3, 7):
                is_blinking = True
                blink_start = now
            
            if is_blinking:
                if now - blink_start > blink_duration:
                    is_blinking = False
                    last_blink = now
                self._draw_eyes(closed=True)
            else:
                self._draw_eyes(closed=False)

            # Logika Mulut (Lip-Sync Sederhana)
            if self.state == "SPEAKING":
                # Animasi mulut buka tutup cepat
                self.mouth_open = (self.mouth_open + 1) % 5
                self._draw_mouth(size=self.mouth_open * 10)
            else:
                self._draw_mouth(size=0)

            pygame.display.flip()
            time.sleep(0.05) # ~20 FPS cukup untuk wajah simpel

    def _draw_eyes(self, closed=False):
        if closed:
            # Mata garis saat berkedip
            pygame.draw.rect(self.screen, self.eye_color, (220, 180, 80, 10))
            pygame.draw.rect(self.screen, self.eye_color, (500, 180, 80, 10))
        else:
            # Mata oval normal
            pygame.draw.ellipse(self.screen, self.eye_color, (230, 140, 60, 100))
            pygame.draw.ellipse(self.screen, self.eye_color, (510, 140, 60, 100))

    def _draw_mouth(self, size=0):
        if size > 0:
            # Mulut terbuka (semakin besar size, semakin lebar)
            rect = (350, 300, 100, 20 + size)
            pygame.draw.ellipse(self.screen, self.eye_color, rect)
        else:
            # Mulut garis datar
            pygame.draw.line(self.screen, self.eye_color, (360, 320), (440, 320), 8)

# Inisialisasi global
face = BMOFace()