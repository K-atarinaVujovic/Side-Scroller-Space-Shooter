import pygame
from pygame.sprite import Sprite
import random

PLAYER_INIT_POSITION_MARGIN = 25
MARGIN = 3

class AbstractSpaceship(Sprite):
    """Abstract class for managing spaceships"""
    def __init__(self, screen, settings):
        """Initialize spaceship"""
        super().__init__()
        self.screen_rect = screen.get_rect()
        self.settings = settings

        self.speed = self.settings.speed

        # Initialize spaceship    
        self.image = pygame.image.load(self.settings.sprite_img).convert_alpha()
        self.rect = self.image.get_rect()

        # Position spaceship
        self.init_position()

        # Hitbox
        self.mask = pygame.mask.from_surface(self.image)

        # Movement flags
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        # Bullet 
        self.shoot = False
        self.bullet_cooldown = 0
        
    def move_spaceship(self):
        """Update spaceship position"""
        pass

    def update(self, dt):
        """Update spaceship"""
        pass

    def init_position(self):
        """Position spaceship to initial position"""
        pass

    

class PlayerSpaceship(AbstractSpaceship):
    """Manages player spaceship"""
    def __init__(self, screen, settings):
        super().__init__(screen, settings)
        self.fire_rate = settings.fire_rate

    def handle_input(self, keys):
        """Set movement flags based on key state"""
        self.moving_right = keys[pygame.K_RIGHT]
        self.moving_left = keys[pygame.K_LEFT]
        self.moving_up = keys[pygame.K_UP]
        self.moving_down = keys[pygame.K_DOWN]

        self.shoot = keys[pygame.K_SPACE]

    def reset(self):
        """Reset position and stats"""
        self.init_position()

    def update(self, dt):
        """Update spaceship"""
        self.move_spaceship()
        if self.bullet_cooldown > 0:
            self.bullet_cooldown -= dt

    def move_spaceship(self):
        """Move player spaceship"""
        pos_x = self.rect.x
        pos_y = self.rect.y

        if self.moving_right and self.rect.right < (self.screen_rect.right - MARGIN):
            pos_x += self.speed
        if self.moving_left and self.rect.left > MARGIN:
            pos_x -= self.speed
        if self.moving_up and self.rect.top > MARGIN:
            pos_y -= self.speed
        if self.moving_down and self.rect.bottom < (self.screen_rect.bottom - MARGIN):
            pos_y += self.speed

        # Update rect
        self.rect.x = pos_x
        self.rect.y = pos_y

    def init_position(self):
        """Position player spaceship to starting position"""
        self.rect.x = PLAYER_INIT_POSITION_MARGIN
        self.rect.centery = self.screen_rect.centery

class EnemySpaceship(AbstractSpaceship):
    """Manages enemy spaceship"""
    def __init__(self, screen, settings):
        super().__init__(screen, settings)
        self.screen_rect = screen.get_rect()
        self.settings = settings

        # Initialize attribute
        self.direction_cooldown = 0
        # Set attribute
        self._reset_direction_cooldown()

        # Initialize movement
        self.moving_up = True
        self.moving_left = True

        self.bullet_cooldown = settings.calculate_bullet_cooldown()

    def init_position(self):
        """Position enemy spaceship to random position on the right"""
        self.rect.x = self.screen_rect.right
        self.rect.y = random.randint(MARGIN, self.screen_rect.height - self.rect.height - MARGIN)

    def move_spaceship(self):
        pos_x = self.rect.x
        pos_y = self.rect.y

        if self.moving_left:
            pos_x -= self.speed
        if self.moving_up and self.rect.top > MARGIN:
            pos_y -= self.speed
        if self.moving_down and self.rect.bottom < (self.screen_rect.bottom - MARGIN):
            pos_y += self.speed

        # Update rect
        self.rect.x = pos_x
        self.rect.y = pos_y

    def update(self, dt):
        """Update enemy spaceship"""

        # Update direction
        if self.rect.top <= MARGIN or self.rect.bottom >= self.screen_rect.bottom - MARGIN or self.direction_cooldown <= 0:
            self._toggle_direction()

        if self.direction_cooldown > 0:
            self.direction_cooldown -= dt    

        # Update bullet cooldown
        if self.bullet_cooldown > 0:
            self.bullet_cooldown -= dt

        # Check if it's time for enemy to shoot
        if self.bullet_cooldown <= 0:
            self.shoot = True
            self.bullet_cooldown = self.settings.calculate_bullet_cooldown()

        # Move
        self.move_spaceship()


    def _toggle_direction(self):
        """Change direction and reset cooldown"""
        if(self.moving_up):
            self.moving_up = False
            self.moving_down = True
        else:
            self.moving_up = True
            self.moving_down = False

        self._reset_direction_cooldown()

    def _reset_direction_cooldown(self):
        """Reset direction cooldown to random amount of time"""
        self.direction_cooldown = self.settings.calculate_direction_cooldown()

