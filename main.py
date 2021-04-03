"""My alien shooter game using classes"""
import pygame
from pygame import mixer
import sys
from time import sleep
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard


class AlienInvasion:
    """A class to run and manage the game"""

    def __init__(self):
        """Initialize the AI class"""
        pygame.init()
        self.settings = Settings()  # Create the settings object

        # Screen parameters
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.screen_rect = self.screen.get_rect()
        self.background_img = pygame.image.load(self.settings.bg_image)
        # FULL SCREEN OPTION
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        # Game window settings
        pygame.display.set_caption(self.settings.caption)
        icon = pygame.image.load(self.settings.icon)
        pygame.display.set_icon(icon)

        # Initialize background music
        mixer.music.load(self.settings.bg_music)
        mixer.music.play(-1)
        self.fire_sound = mixer.Sound(self.settings.fire_sound)
        self.splat_sound = mixer.Sound(self.settings.splat_sound)
        self.die_sound = mixer.Sound(self.settings.die_sound)

        # Create game statistics object and scoreboard object
        self.stats = GameStats(self)
        self.sb = ScoreBoard(self)

        # Create ship, bullets and alien objects
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        # Create the alien fleet
        self._create_fleet()

        # Create play button
        self.play_button = Button(self, "Click or press 'P' to play")

        # Autofire ON!
        self.auto_fire_flag = self.settings.auto_fire_flag
        self.auto_fire = False

    def run_game(self):
        """Main game loop"""
        while True:
            # Check events
            self._check_events()
            # While game is active
            if self.stats.game_active:
                self.ship.update()
                self._check_autofire()
                self._update_aliens()
                self._update_bullets()
            # Update screen
            self._update_screen()

    def _check_events(self):
        """Monitor mouse and keyboard events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_p:
            if not self.stats.game_active:
                self._start_game()
        elif event.key == pygame.K_SPACE:
            if self.auto_fire_flag:
                self.auto_fire = True
            elif not self.auto_fire_flag:
                self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_SPACE:
            if self.auto_fire:
                self.auto_fire = False

    def _check_play_button(self, mouse_pos):
        """Starts new game when player clicks Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self._start_game()

    def _start_game(self):
        # Reset game settings
        self.settings.initialize_dynamic_settings()
        # Reset game stats
        self.stats.reset_stats()
        # Refresh score and level
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()
        # Set game_active to true
        self.stats.game_active = True
        # Remove remaining aliens and bullets
        self.aliens.empty()
        self.bullets.empty()
        # Create a new fleet and center the ship
        self._create_fleet()
        self.ship.center_ship()
        # Hide the mouse cursor
        pygame.mouse.set_visible(False)
        # Pause
        sleep(1.0)

    def _fire_bullet(self):
        """Create bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            self.fire_sound.play()
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _check_autofire(self):
        if self.auto_fire and len(self.bullets) < self.settings.bullets_allowed:
            self.fire_sound.play()
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        """Create fleet of aliens"""
        # Create an alien and find the number of aliens in a row
        # Aliens should be one alien width from each other
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        # Determine the number of aliens in a row
        space_x = self.screen_rect.width
        num_aliens = (space_x + alien_width) // (2 * alien_width)
        # Determine the number of alien rows
        ship_height = self.ship.rect.height
        space_y = self.screen_rect.height - (3 * alien_height) - ship_height
        row_aliens = space_y // (2 * alien_height)
        # Create a row of aliens 'row_aliens' number of times
        for row_number in range(row_aliens):
            for alien_number in range(num_aliens):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in a row"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 1.5 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = (alien_height + 10) + 1.7 * alien_height * row_number
        self.aliens.add(alien)
        # print(alien.x, alien.y)

    def _check_fleet_edges(self):
        """Check if any alien has hit the edge of the screen"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Change fleet direction and drop the fleet"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_aliens(self):
        """Updates positions of all aliens in the fleet"""
        self._check_fleet_edges()
        self.aliens.update()
        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # Look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.screen_rect.bottom:
                self._ship_hit()
                break

    def _ship_hit(self):
        """What happens when an alien hits the ship"""
        # Check for ships remaining
        self.die_sound.play()
        self.aliens.empty()
        if self.stats.ships_left > 0:
            # Decrement ships left and update ship counter
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            # Remove remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()
            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()
            # Pause
            sleep(1.0)
        else:
            self.stats.game_active = False
            self.aliens.empty()
            # Show cursor if game ends
            pygame.mouse.set_visible(True)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets"""
        self.bullets.update()
        # Get rid of bullets that have disappeared
        # for bullet in self.bullets.copy():
        #    if bullet.rect.bottom <= 0:
        #        self.bullets.remove(bullet)
        # print(len(self.bullets))
        # Hit check
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet alien collisions"""
        # Get rid of bullets and aliens that have collided
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        # Update score for any killed alien and check for high score
        if collisions:
            self.splat_sound.play()
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        # Killed 'em all :-)
        if not self.aliens:
            # Destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()

    def _update_screen(self):
        # Redraw the background on each pass
        self.screen.blit(self.background_img, self.screen_rect)
        # Show ship
        self.ship.blit_me()
        # Draw the alien
        self.aliens.draw(self.screen)
        # Show bullets
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # Draw the score and level info
        self.sb.show_score()
        # While game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()
        # Update the screen
        pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
