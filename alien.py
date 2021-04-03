import random
import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to represent a single alien  in the fleet"""
    def __init__(self, ai_game):
        """Initialize the alien and its starting position"""
        super().__init__()
        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen_rect

        # Load the alien image and set its rect attribute
        x = random.randint(0, 6)
        image_string = f'images/aliens/alien{x}.png'
        self.image = pygame.image.load(image_string)
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen
        # self.rect.x = self.rect.width
        # self.rect.y = self.rect.height

        # Store aliens x coordinate as a float
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return true if alien hits the edge"""
        return self.rect.right >= self.screen_rect.right or self.rect.left <= self.screen_rect.left

    def update(self):
        """Move alien to the left or right"""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x
