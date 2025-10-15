import pygame
import math
import sys

from settings import GameSettings, PlayerSettings, AsteroidSettings
from sprites.spaceship import PlayerSpaceship
from sprites.bullet import PlayerBullet
from sprites.asteroid import Asteroid

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
        self.asteroid_settings = AsteroidSettings()
        
        self.game_over = False
        self.dt = 0

        # Background        
        self.bg = pygame.image.load(self.settings.bg_image).convert_alpha()
        self.bg_width = self.bg.get_width()   
        self.tiles = math.ceil(self.settings.screen_width / self.bg_width) + 1
        self.scroll_speed = self.settings.scroll_speed
        self.scroll = 0

        # Player sprites
        self.player_sprite = PlayerSpaceship(self.screen, self.player_settings)
        self.player_sprites = pygame.sprite.GroupSingle(self.player_sprite)
        self.player_bullets = pygame.sprite.Group()

        # Asteroid sprites
        self.asteroid_sprites = pygame.sprite.Group()

        # Asteroid generation variables
        self.asteroid_cooldown = self.asteroid_settings.cooldown

    def run(self):
        """Start game loop"""
        running = True

        # Game loop
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()

            # Update game state according to player actions
            self.update_game_state(keys)


    def update_game_state(self, keys):
        """Call functions to handle all logic needed"""
        # Time passed since last frame
        self.dt = self.clock.tick(self.settings.fps)

        # Update cooldowns
        self._update_cooldowns()

        # Check for collisions
        self._check_collisions()

        # Handle input
        self.player_sprite.handle_input(keys)

        # Check if new objects need to be spawned
        self._check_spawns()

        # Update sprites    
        self._update_sprites()

        # Draw
        self._draw()         

    def _check_spawns(self):
        """Check if a game object needs to be spawned"""
        # Check if player fired a bullet
        if self.player_sprite.shoot and self.player_sprite.bullet_cooldown <= 0:
            self._spawn_player_bullet()

        # Check if it's time to generate a new asteroid
        if self.asteroid_cooldown <= 0:
            self._spawn_asteroid()
    
    def _update_cooldowns(self):
        # Update cooldowns
        if self.asteroid_cooldown > 0:          
            self.asteroid_cooldown -= self.dt

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

    def _draw(self):
        self._draw_background()
        self._draw_sprites()

        # Update display
        pygame.display.update()

    def _spawn_player_bullet(self):
        """Add player bullet sprite and reset cooldown"""
        new_bullet = PlayerBullet(self.screen, self.player_settings, self.player_sprite.rect)
        self.player_bullets.add(new_bullet)
        self.player_sprite.bullet_cooldown = self.player_sprite.fire_rate

    def _spawn_asteroid(self):
        """Add asteroid and reset cooldown"""
        new_asteroid = Asteroid(self.screen, self.asteroid_settings)
        self.asteroid_sprites.add(new_asteroid)
        self.asteroid_cooldown = self.asteroid_settings.cooldown

    def _update_sprites(self):
        self.player_sprites.update(self.dt)
        self.player_bullets.update()
        self.asteroid_sprites.update()

        # Remove out-of-bounds bullets
        for bullet in self.player_bullets:
            if(bullet.rect.x > self.screen.get_rect().right):
                self.player_bullets.remove(bullet)

        # Remove out-of-bounds asteroids
        for asteroid in self.asteroid_sprites:
            if(asteroid.rect.x > self.screen.get_rect().right):
                self.asteroid_sprites.remove(asteroid)

    def _draw_sprites(self):
        for bullet in self.player_bullets:
            bullet.draw()          
        self.player_sprites.draw(self.screen)
        self.asteroid_sprites.draw(self.screen)

    def _check_collisions(self):
        # Player and asteroid
        if pygame.sprite.spritecollide(self.player_sprite, self.asteroid_sprites, False, pygame.sprite.collide_rect):
            if pygame.sprite.spritecollide(self.player_sprite, self.asteroid_sprites, False, pygame.sprite.collide_mask):
                self.game_over = True