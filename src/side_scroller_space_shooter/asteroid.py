import pygame
from pygame.sprite import Sprite
import random

MARGIN = 3

class Asteroid(Sprite):
    """Class for managing asteroids"""
    def __init__(self, screen, settings):
        """Initialize asteroid"""
        super().__init__()
        self.screen_rect = screen.get_rect()
        self.settings = settings

        self.speed = self.settings.speed

        # Initialize asteroid
        self.image = pygame.image.load(self.settings.sprite_img).convert_alpha()
        self.rect = self.image.get_rect()

        # Position asteroid
        pos_x = self.screen_rect.right
        pos_y = random.randint(MARGIN, self.screen_rect.height - self.rect.height - MARGIN)
        self.rect.x, self.rect.y = pos_x, pos_y

        # Hitbox
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        """Update asteroid position"""
        self.rect.x -= self.speed