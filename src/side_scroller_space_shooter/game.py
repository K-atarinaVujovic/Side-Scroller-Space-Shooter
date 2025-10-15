import pygame
import math
import sys

from settings import GameSettings, PlayerSettings
from spaceship import PlayerSpaceship
from bullet import PlayerBullet

class Game:
    """Class that runs the game"""

    def __init__(self):
        """Initialize class"""
        pygame.init()
        self.clock = pygame.time.Clock()

        # Settings
        self.settings = GameSettings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.player_settings = PlayerSettings()

        # Background        
        self.bg = pygame.image.load(self.settings.bg_image).convert_alpha()
        self.bg_width = self.bg.get_width()   
        self.tiles = math.ceil(self.settings.screen_width / self.bg_width) + 1
        self.scroll_speed = self.settings.scroll_speed
        self.scroll = 0

        # Player
        self.player_sprite = PlayerSpaceship(self.screen, self.player_settings)
        self.player_sprites = pygame.sprite.GroupSingle(self.player_sprite)
        self.player_bullets = pygame.sprite.Group()
        # # Bullet
        # self.bullet = PlayerBullet(self.screen, self.player_settings, self.player_sprite.rect.right, self.player_sprite.rect.centery)
        # self.bullet.draw()

    def run(self):
        """Start game loop"""
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Time passed since last frame
            dt = self.clock.tick(self.settings.fps)

            # Handle key presses
            keys = pygame.key.get_pressed()
            self.player_sprite.handle_input(keys)
            if self.player_sprite.shoot and self.player_sprite.bullet_cooldown <= 0:
                self.add_player_bullet()

            # Re-position sprites    
            self.player_sprites.update(dt)
            self.player_bullets.update()
            # Remove out-of-bounds bullets
            for bullet in self.player_bullets:
                if(bullet.rect.x > self.screen.get_rect().right):
                    self.player_bullets.remove(bullet)

            # Draw background
            self._draw_background()

            # Draw sprites
            for bullet in self.player_bullets:
                bullet.draw()
            self.player_sprites.draw(self.screen)
            

            # Update display
            pygame.display.update()
            

    def _draw_background(self):
        """Draw background"""
        # Clear screen
        self.screen.fill((0, 0, 0))

        # Draw background
        for i in range(0, self.tiles):
            self.screen.blit(self.bg, (i * self.bg_width + self.scroll, 0))
        
        # Scroll background
        self.scroll -= self.scroll_speed
        
        # Reset scroll
        if abs(self.scroll) > self.bg_width:
            self.scroll = 0

    def add_player_bullet(self):
        """Add player bullet sprite and reset cooldown"""
        new_bullet = PlayerBullet(self.screen, self.player_settings, self.player_sprite.rect)
        self.player_bullets.add(new_bullet)
        self.player_sprite.bullet_cooldown = self.player_sprite.fire_rate