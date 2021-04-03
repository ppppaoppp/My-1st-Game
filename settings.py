"""Settings module for Alien Invasion"""


class Settings:
    """A class to store the settings for AlienInvasion"""

    def __init__(self):
        # Screen settings
        self.screen_width = 800
        self.screen_height = 600
        # self.bg_color = (115, 215, 255)
        self.caption = 'Invaders !!!'
        self.icon = 'images/ship.png'
        self.bg_image = 'images/background.png'

        # Sound settings
        self.bg_music = 'sounds/bg_music.ogg'
        self.fire_sound = 'sounds/fire.wav'
        self.splat_sound = 'sounds/alien_splat.wav'
        self.die_sound = 'sounds/die.wav'

        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullets_allowed = 5
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = (255, 0, 0)
        # Autofire
        self.auto_fire_flag = False

        # Alien settings
        self.fleet_drop_speed = 10

        # How quickly the game speeds up
        self.speedup_scale = 1.05

        # How quicly the points rack up
        self.score_scale = 1.2

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game"""
        self.ship_speed = 0.4
        self.bullet_speed = 1.0
        self.alien_speed = 0.1
        self.fleet_direction = 1  # 1 = right, -1 = left
        self.alien_points = 10

    def increase_speed(self):
        """Initialize settings that change throughout the game"""
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        # self.bullet_speed *= self.speedup_scale
        # self.ship_speed *= self.speedup_scale
        # self.fleet_direction *= self.speedup_scale