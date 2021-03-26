import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
import game_functions as gf

# Info für mich:
# .rect(pygame) steht für rectangle = rechteck

def run_game():
    
    # Initialisiert das Spiel und erstellt ein screen-Objekt.
    pygame.init()

    ai_settings = Settings() #Instanz von Settings() wird erstellt und in ai_settings gespeichert.

    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Erstellt die Play-Schaltfläche
    play_button = Button(ai_settings, screen, "Play")

    # Erstellt eine Instanz zur Speicherung von Spielstatistiken.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # Erstellt ein Schiff.
    ship = Ship(ai_settings, screen)

    # Erstellt eine Gruppe zur Speicherung der Geschosse.
    bullets = Group()

    # Erstellt eine Gruppe aus Aliens.
    aliens = Group()

    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Startet die Hauptschleife des Spiels.
    while True:
        # Reaktion auf Tastatur- und Maueingaben.
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)

        if stats.game_aktive:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets)

        # Zeichnet den Bildschirm bei jedem Schleifendurchlauf neu.
        # Macht den als Letztes gezeichneten Bildschirm sichtbar.
        gf.update_screen(ai_settings, stats, sb, screen, ship, aliens, bullets, play_button)

run_game()