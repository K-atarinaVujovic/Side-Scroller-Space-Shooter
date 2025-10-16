import pygame
from pygame.sprite import Sprite

class AbstractBullet(Sprite):
    """Abstract class for managing bullets"""
    
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
        self.initialize_bullet_position(shooter_rect)   

        # Hitbox
        self.mask = pygame.mask.from_surface(self.image)

    def initialize_bullet_position(self, shooter_rect):
        """Initialize bullet position in relation to shooter"""
        pass

    def update(self):
        """Progress the bullet"""
        pass

    def draw(self):
        """Draw the bullet"""
        pygame.draw.rect(self.screen, self.color, self.rect)


class PlayerBullet(AbstractBullet):
    """Manages player bullets"""
    def __init__(self, screen, settings, shooter_rect):
        super().__init__(screen, settings, shooter_rect)
        
    def update(self):
        """Update player bullet"""
        self.rect.x += self.speed

    def initialize_bullet_position(self, shooter_rect):
        """Initialize bullet position in relation to player"""
        (pos_x, pos_y) = shooter_rect.midright
        pos_x -= 6
        pos_y += 1
        self.rect.center = (pos_x, pos_y)   

class EnemyBullet(AbstractBullet):
    """Manages enemy bullets"""
    def __init__(self, screen, settings, shooter_rect):
        super().__init__(screen, settings, shooter_rect)

    def update(self):
        """Update enemy bullet"""
        self.rect.x -= self.speed

    def initialize_bullet_position(self, shooter_rect):
        """Initialize bullet position in relation to enemy"""
        (pos_x, pos_y) = shooter_rect.midleft
        pos_x -= 6
        self.rect.center = (pos_x, pos_y)   