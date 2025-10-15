import pygame
from pygame.sprite import Sprite

class AbstractBullet(Sprite):
    """Class for managing bullets"""
    
    def __init__(self, screen, settings, shooter_rect):
        super().__init__()
        self.screen = screen
        self.speed = settings.bullet_speed
        self.color = settings.bullet_color
        self.width = settings.bullet_width
        self.height = settings.bullet_height

        # Initialize bullet
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.fill(self.color)
        self.rect = self.image.get_rect()

        # Position bullet
        (pos_x, pos_y) = shooter_rect.midright
        pos_x -= 6
        pos_y += 1
        self.rect.center = (pos_x, pos_y)      

        # Hitbox
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        """Progress the bullet"""
        pass

    def draw(self):
        """Draw the bullet"""
        pygame.draw.rect(self.screen, self.color, self.rect)


class PlayerBullet(AbstractBullet):
    """Class for player bullet"""
    def __init__(self, screen, settings, shooter_rect):
        super().__init__(screen, settings, shooter_rect)
        
    def update(self):
        # Update rect
        self.rect.x += self.speed