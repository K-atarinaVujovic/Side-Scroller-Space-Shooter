import pygame
import math
import sys

from side_scroller_space_shooter.settings import GameSettings, PlayerSettings, AsteroidSettings, EnemySettings
from side_scroller_space_shooter.sprites.spaceship import PlayerSpaceship
from side_scroller_space_shooter.managers.sprite_manager import SpriteManager
from side_scroller_space_shooter.managers.draw_manager import DrawManager
from side_scroller_space_shooter.managers.collision_manager import CollisionManager

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
        self.enemy_settings = EnemySettings()
        
        self.game_over = False
        self.dt = 0       

        # Player sprites
        self.player_sprite = PlayerSpaceship(self.screen, self.player_settings)
        self.player_sprites = pygame.sprite.GroupSingle(self.player_sprite)
        self.player_bullets = pygame.sprite.Group()

        # Asteroid sprites
        self.asteroid_sprites = pygame.sprite.Group()

        # Enemy sprites
        self.enemy_sprites = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()

        # Spawn cooldowns
        self.asteroid_spawn_cooldown = self.asteroid_settings.spawn_cooldown
        self.enemy_spawn_cooldown = self.enemy_settings.calculate_spawn_cooldown()

        # Game stats
        self.score = 0
        # Used for rewards in RL
        self.shot_enemy = False

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
                self.draw.draw_game_over()

            else:
                self.draw_game()

            pygame.display.update()


    def update_game_state(self, keys):
        """Call functions to handle all logic needed"""
        # Time passed since last frame
        self.dt = self.clock.tick(self.settings.fps)

        # Update cooldowns
        self._update_spawn_cooldowns()

        # Check for collisions
        self.shot_enemy = self.collision.check_collisions()

        # Handle input
        self.player_sprite.handle_input(keys)

        # Check if new objects need to be spawned
        self.sprites.check_spawns()

        # Update sprites    
        self.sprites.update()


 
    def draw_game(self):
        # Draw
        self.draw.draw()

    def reset(self):
        """Reset game"""
        self.player_sprite.reset()
        self.asteroid_spawn_cooldown = self.asteroid_settings.spawn_cooldown
        self.game_over = False
        self.score = 0

        # Empty sprite groups
        self.player_bullets.empty()
        self.asteroid_sprites.empty()
        self.enemy_bullets.empty()
        self.enemy_sprites.empty()

    def _update_spawn_cooldowns(self):
        """Update spawn cooldowns"""
        # Update asteroid spawn cooldown
        if self.asteroid_spawn_cooldown > 0:          
            self.asteroid_spawn_cooldown -= self.dt

        # Update enemy spawn cooldown
        if self.enemy_spawn_cooldown > 0:
            self.enemy_spawn_cooldown -= self.dt
        