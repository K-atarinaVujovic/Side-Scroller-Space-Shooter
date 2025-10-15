import pygame
import math

class DrawManager:
    """Manages drawing game objects"""
    def __init__(self, game):
        self.game = game

        # Imported from game
        self.scroll_speed = game.settings.scroll_speed
        self.screen = game.screen
        self.player_bullets = game.player_bullets
        self.asteroid_sprites = game.asteroid_sprites
        self.player_sprites = game.player_sprites
        self.settings = game.settings

        # Background        
        self.bg = pygame.image.load(self.settings.bg_image).convert_alpha()
        self.bg_width = self.bg.get_width()   
        self.tiles = math.ceil(self.settings.screen_width / self.bg_width) + 1

        # Scroll
        self.scroll = 0

    def draw(self):
        """Draw background and sprites"""
        self._draw_background()
        self._draw_sprites()

        # Update display
        pygame.display.update()



    def _draw_sprites(self):
        """Draw sprites"""
        for bullet in self.player_bullets:
            bullet.draw()          
        self.player_sprites.draw(self.screen)
        self.asteroid_sprites.draw(self.screen)
    
    def _draw_background(self):
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