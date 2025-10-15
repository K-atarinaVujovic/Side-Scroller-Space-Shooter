import pygame
from pygame.sprite import Sprite

class AbstractBullet(Sprite):
    """Class for managing"""
    
    def __init__(self, screen, settings, shooter_rect):
        super().__init__()
        self.screen = screen
        self.speed = settings.bullet_speed
        self.color = settings.bullet_color
        self.width = settings.bullet_width
        self.height = settings.bullet_height

        # Create bullet
        (pos_x, pos_y) = shooter_rect.midright
        pos_x -= 6
        pos_y += 1
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (pos_x, pos_y)      

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