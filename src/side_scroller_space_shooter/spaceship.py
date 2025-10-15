import pygame
from pygame.sprite import Sprite

POS_X = 100
POS_Y = 100

class AbstractSpaceship(Sprite):
    """Abstract class for managing spaceships"""
    def __init__(self, screen, settings):
        super().__init__()
        self.screen_rect = screen.get_rect()
        self.settings = settings

        # Draw ship
        self.speed = self.settings.speed
        self.image = pygame.image.load(self.settings.sprite_img).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (POS_X, POS_Y)

        # Hitbox
        self.mask = pygame.mask.from_surface(self.image)

        # Movement flags
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        # Bullet 
        self.shoot = False
        self.fire_rate = settings.fire_rate
        self.bullet_cooldown = 0
        
    def _move_spaceship(self):
        """Update spaceship position"""
        pos_x = self.rect.x
        pos_y = self.rect.y

        if self.moving_right and self.rect.right < self.screen_rect.right:
            pos_x += self.speed
        if self.moving_left and self.rect.left > self.screen_rect.left:
            pos_x -= self.speed
        if self.moving_up and self.rect.top > self.screen_rect.top:
            pos_y -= self.speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            pos_y += self.speed


        # Update rect
        self.rect.x = pos_x
        self.rect.y = pos_y

    def update(self, dt):
        """Update spaceship"""
        self._move_spaceship()
        if self.bullet_cooldown > 0:
            self.bullet_cooldown -= dt
        

class PlayerSpaceship(AbstractSpaceship):
    """Class for managing player spaceship"""
    def __init__(self, screen, settings):
        super().__init__(screen, settings)

    def handle_input(self, keys):
        """Set movement flags based on key state"""
        self.moving_right = keys[pygame.K_RIGHT]
        self.moving_left = keys[pygame.K_LEFT]
        self.moving_up = keys[pygame.K_UP]
        self.moving_down = keys[pygame.K_DOWN]

        self.shoot = keys[pygame.K_SPACE]
