import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Lädt das Bild des Schiffes und ruft dessen umgebendes Rechteck ab.
        self.image = pygame.image.load('rsc/ship.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Platziert jedes neue Schiff mittig am unteren Bildschirmrand.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Speichert einen FLießkommawert für den Schiffmittelpunkt
        self.center = float(self.rect.centerx)

        # Bewegungsflag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        # Aktualisierung der Schiff-Position.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # Aktualisiert das rect-Objekt auf der Grundlage von self.center.
        self.rect.centerx = self.center

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.center = self.screen_rect.centerx

