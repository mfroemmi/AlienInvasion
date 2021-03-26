import sys
from time import sleep
import pygame

from bullet import Bullet
from alien import Alien

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def fire_bullet(ai_settings, screen, ship, bullets):
    # Erstellt ein neues Geschoss und fügt es der Gruppe bullets hinzu.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    # Reaktion auf Tastatur- und Maueingaben.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    if play_button.rect.collidepoint(mouse_x, mouse_y):
        button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
        if button_clicked and not stats.game_aktive:
            # Setzt Spieleinstellungen zurück
            ai_settings.initialize_dynamic_settings()

            # Blendet den Mauzeiger aus
            pygame.mouse.set_visible(False)
            # Setzt die Spielstatistiken zurück
            stats.reset_stats()
            stats.game_aktive = True

            # Setzt die Bilder der Anzeigetafel zurück
            sb.prep_score()
            sb.prep_high_score()
            sb.prep_level()
            sb.prep_ships()

            # Leert die Liste der Invasionschiffe und Geschosse
            aliens.empty()
            bullets.empty()

            # Erstellt eine neue Flotte und zentriert das eigene Schiff
            create_fleet(ai_settings, screen, ship, aliens)
            ship.center_ship()

def update_screen(ai_settings, stats, sb, screen, ship, aliens, bullets, play_button):
    # Zeichnet den Bildschirm bei jedem Schleifendurchlauf neu.
    screen.fill(ai_settings.bg_color)

    # Zeichnet alle Geschosse hinter dem Shiff und den Außerirdischen neu.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # Zeichnet den Punktestand
    sb.show_score()

    # Zeichnet die Play-Schaltfläche nur bei inaktivem Spiel
    if not stats.game_aktive:
        play_button.draw_button()

    # Macht den zuletzt gezeichneten Bildschirm sichtbar.
    pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # Aktualisiert die Geschossposition.
    bullets.update()

    # Entfernt die verschwundenen Geschosse.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):

    # Prüft, ob irgendwelche Geschosse ein Alien getroffen hat.
    # Wenn ja, werden das Geschoss und das Alien entfernt.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        #Zerstört alle vorhandenen Geschosse und erstellt eine neue Flotte.
        bullets.empty()
        ai_settings.increase_speed()

        # Setzt das Level herauf
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)

def get_number_aliens_x(ai_settings, alien_width):
    # Erstellt ein Alien und ermittelt die zur Verfügung stehende Breite.
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = (ai_settings.screen_height - (1 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 1 * alien.rect.height * row_number + 30
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    # Erstellt ein Alien und platziert es in der Reihe.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    # Erstellt die erste Reihe von Aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets):
    # Veringert die Anzahl der verbleibenden Schiffe.
    if stats.ships_left > 0:
        stats.ships_left -= 1
        sb.prep_ships()

        # Leert die Liste der Aliens und Geschosse.
        aliens.empty()
        bullets.empty()

        # Erstellt neue Aliens und zentriert das eigene Schiff.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause.
        sleep(0.5)
    else:
        stats.game_aktive = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)

def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Prüft auf Kollision zwischen Aliens und dem eigenen Schiff.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)

    check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets)

def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()