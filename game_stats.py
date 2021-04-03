class GameStats:
    """A class to track the game statistics"""

    def __init__(self, ai_game):
        """Initialize statistics"""
        self.settings = ai_game.settings
        self.reset_stats()
        # Start game in an active state
        self.game_active = False

        # High score (not to be reset)
        self.high_score = 0



    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
