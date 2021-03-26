class GameStats():
    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()

        # Startet das Spiel im inaktiven Modus
        self.game_aktive = False

        # Der Highscore darf nie zurückgesetzt werden
        self.high_score = 0

    def reset_stats(self):
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 0