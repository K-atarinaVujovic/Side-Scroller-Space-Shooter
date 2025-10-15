import pygame
import math
import sys

from settings import GameSettings, PlayerSettings, AsteroidSettings
from sprites.spaceship import PlayerSpaceship
from sprites.bullet import PlayerBullet
from sprites.asteroid import Asteroid
from managers.sprite_manager import SpriteManager
from managers.draw_manager import DrawManager
from managers.collision_manager import CollisionManager

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

        # Player sprites
        self.player_sprite = PlayerSpaceship(self.screen, self.player_settings)
        self.player_sprites = pygame.sprite.GroupSingle(self.player_sprite)
        self.player_bullets = pygame.sprite.Group()

        # Asteroid sprites
        self.asteroid_sprites = pygame.sprite.Group()

        # Asteroid generation variables
        self.asteroid_cooldown = self.asteroid_settings.cooldown

        # Game stats
        self.score = 0

        # Initialize managers
        self.sprites = SpriteManager(self)
        self.draw = DrawManager(self)
        self.collision = CollisionManager(self)

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

            # Reset if R was pressed
            if keys[pygame.K_r]:
                self.reset()

            if not self.game_over:
                # Update game state according to player actions
                self.update_game_state(keys)           

            # Handle game over
            if self.game_over:
                self.draw.draw_text("Game over", self.screen.get_rect().centerx, self.screen.get_rect().centery, True)

            pygame.display.update()


    def update_game_state(self, keys):
        """Call functions to handle all logic needed"""
        # Time passed since last frame
        self.dt = self.clock.tick(self.settings.fps)

        # Update cooldowns
        self._update_cooldowns()

        # Check for collisions
        self.collision.check_collisions()

        # Handle input
        self.player_sprite.handle_input(keys)

        # Check if new objects need to be spawned
        self.sprites.check_spawns()

        # Update sprites    
        self.sprites.update()

        # Draw
        self.draw.draw()     
  
    def reset(self):
        self.player_sprite.reset()
        self.asteroid_cooldown = self.asteroid_settings.cooldown
        self.game_over = False

        # Empty sprite groups
        self.player_bullets.empty()
        self.asteroid_sprites.empty()


    def _update_cooldowns(self):
        # Update cooldowns
        if self.asteroid_cooldown > 0:          
            self.asteroid_cooldown -= self.dt