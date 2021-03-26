import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    # Erstellen eines Aliens
    def __init__(self, ai_settings, screen):
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Lädt das Bild des Alien und legt das rect-Attribut fest
        self.image = pygame.image.load('rsc/alien.png')
        self.rect = self.image.get_rect()

        # Platziert jeden neuen Alien oben links auf dem Bildschirm
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Speichert die genaue Position des Alien
        self.x = float(self.rect.x)

    def blitme(self):
        # Zeichnet das Alien an der aktuellen Position
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x