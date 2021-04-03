import pygame.font


class Button():
    """A class to make and manage a button"""

    def __init__(self, ai_game, msg):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen_rect

        # Set the dimensions and properties of the button
        self.width, self.height = 300, 40
        self.button_color = (0, 138, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.Font('fonts/computer.ttf', 32)

        # Build the button's rect object and center it
        self.rect = pygame.Rect((0, 0), (self.width, self.height))
        self.rect.center = self.screen_rect.center

        # Prepare button message (run once)
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turns msg into rendered image and center text on the button"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Draw blank button then image
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
