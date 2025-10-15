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

        self.speed = self.settings.speed
        self.image = pygame.image.load(self.settings.sprite_img).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (POS_X, POS_Y)

        # Movement flags
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        # Spaceship position
        self.pos_x, self.pos_y = float(POS_X), float(POS_Y)
        
    def _move_spaceship(self):
        """Update spaceship position"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.pos_x += self.speed
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.pos_x -= self.speed
        if self.moving_up and self.rect.top > self.screen_rect.top:
            self.pos_y -= self.speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.pos_y += self.speed


        # Update rect
        self.rect.x = self.pos_x
        self.rect.y = self.pos_y

    def update(self):
        """Update spaceship"""
        self._move_spaceship()
        

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
