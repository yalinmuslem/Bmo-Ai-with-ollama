import pygame
import random
import time

class BMOFace:
    def __init__(self):
        pygame.init()
        # Resolusi standar layar kecil
        self.screen = pygame.display.set_mode((800, 480))
        pygame.display.set_caption("BMO Face")
        self.bg_color = (145, 201, 171) 
        self.eye_color = (30, 30, 30)
        self.state = "IDLE" 
        self.running = True
        self.mouth_open = 0
        self.clock = pygame.time.Clock() # Tambahkan Clock

    def set_state(self, new_state):
        self.state = new_state
        
    def draw_loop(self): # <--- Pastikan namanya draw_loop
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

            # Logika Mulut & Ekspresi
            if self.state == "SPEAKING":
                self.mouth_open = (self.mouth_open + 1) % 5
                self._draw_mouth(size=self.mouth_open * 10)
            elif self.state == "THINKING":
                self._draw_mouth(size=0) # Akan digambar bulat kecil di _draw_mouth
            else:
                self._draw_mouth(size=0)

            pygame.display.flip()
            self.clock.tick(30) # Kunci di 30 FPS agar CPU stabil

    def _draw_eyes(self, closed=False):
        if self.state == "LISTENING":
            # Mata membesar saat mendengar agar terlihat antusias
            pygame.draw.circle(self.screen, (255, 255, 255), (260, 190), 55)
            pygame.draw.circle(self.screen, self.eye_color, (260, 190), 45)
            pygame.draw.circle(self.screen, (255, 255, 255), (540, 190), 55)
            pygame.draw.circle(self.screen, self.eye_color, (540, 190), 45)
        elif closed:
            pygame.draw.rect(self.screen, self.eye_color, (220, 180, 80, 10))
            pygame.draw.rect(self.screen, self.eye_color, (500, 180, 80, 10))
        else:
            pygame.draw.ellipse(self.screen, self.eye_color, (230, 140, 60, 100))
            pygame.draw.ellipse(self.screen, self.eye_color, (510, 140, 60, 100))

    def _draw_mouth(self, size=0):
        if self.state == "SPEAKING":
            rect = (350, 300, 100, 20 + size)
            pygame.draw.ellipse(self.screen, self.eye_color, rect)
        elif self.state == "THINKING":
            pygame.draw.circle(self.screen, self.eye_color, (400, 320), 15)
        else:
            pygame.draw.arc(self.screen, self.eye_color, (350, 280, 100, 40), 3.14, 0, 5)