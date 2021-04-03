import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""

    def __init__(self, ai_game):
        """Create a bullet object from ship's current position"""
        super().__init__()
        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.color = self.settings.bullet_color

        # Create bullet rect at (0, 0) and set correct position
        self.rect = pygame.Rect((0, 0), (self.settings.bullet_width, self.settings.bullet_height))
        self.rect.midtop = ai_game.ship.rect.midtop

        # Store bullet's position as a float
        self.y = float(self.rect.y)

    def update(self):
        """Moves the bullet up the screen and removes them at the top of the screen"""
        # Update the position of the bullet
        self.y -= self.settings.bullet_speed
        # Update bullet rect position and truncate it back to an int
        self.rect.y = self.y
        # "Kill" off-screen bullets
        if self.rect.bottom < 0:
            self.kill()

    def draw_bullet(self):
        """Draw bullet on screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
