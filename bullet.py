import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    # Klasse zum managen der Geschosse vom Schiff
    def __init__(self, ai_settings, screen, ship):
        # Erzeugt ein Geschoss an der Position des Schiffs
        super(Bullet, self).__init__()
        self.screen = screen

        #Erstellt ein Geschoss bei (0,0) und die dann die richtige Position fest
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Speichert die Position des Geschosses als Fließkommawert
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        # Aktualisiert die Fließkommaposition des Geschosses
        self.y -= self.speed_factor
        # Aktualisiert die Position des Rechtecks
        self.rect.y = self.y

    def draw_bullet(self):
        # Zeichnet das Geschoss
        pygame.draw.rect(self.screen, self.color, self.rect)
