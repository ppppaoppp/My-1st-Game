import pygame.font
from pygame.sprite import Group
from ship import Ship

class ScoreBoard:
    """A class to report game scores and stats"""

    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen_rect
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Font settings for scoring information
        self.level_text_color = (128, 234, 255)
        self.score_text_color = (255, 255, 0)
        self.text_color = (255, 0, 0)
        self.font = pygame.font.Font('fonts/computer.ttf', 32)

        # prepare the initial score and level images
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_ships(self):
        """Show how many ships are left"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def check_high_score(self):
        """Check to see if there is a new high score"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_score(self):
        """Turn score into a rendered image"""
        rounded_score = round(self.stats.score, -1)
        score_str = f'{rounded_score:,}'
        self.score_image = self.font.render(score_str, True, self.score_text_color)

        # Display the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.centerx = self.screen_rect.centerx
        self.score_rect.top = self.screen_rect.top + 20

    def prep_high_score(self):
        """Turn high score into a rendered image"""
        rounded_high_score = round(self.stats.high_score, -1)
        rounded_high_score_str = f'HI:{rounded_high_score:,}'
        self.high_score_image = self.font.render(rounded_high_score_str, True, self.text_color)

        # Display the score at the top center of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.right = self.screen_rect.right - 20
        self.high_score_rect.top = 20

    def prep_level(self):
        """Turn level into a rendered image"""
        level_str = f'L: {self.stats.level}'
        self.level_image = self.font.render(level_str, True, self.level_text_color)

        # Display the level below the score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.high_score_rect.right
        self.level_rect.top = self.high_score_rect.bottom + 10

    def show_score(self):
        """Draw the scores and level on the screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)