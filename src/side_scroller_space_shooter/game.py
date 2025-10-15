import pygame
import math

from settings import Settings

class Game:
    """Class that runs the game"""

    def __init__(self):
        """Initialize class"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        # Background        
        self.bg = pygame.image.load(self.settings.bg_image).convert_alpha()
        self.bg_width = self.bg.get_width()   
        self.tiles = math.ceil(self.settings.screen_width / self.bg_width) + 1
        self.scroll_speed = self.settings.scroll_speed
        self.scroll = 0

    def run(self):
        """Start game loop"""
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            self.draw_background()

            pygame.display.update()
            self.clock.tick(self.settings.fps)

    def draw_background(self):
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