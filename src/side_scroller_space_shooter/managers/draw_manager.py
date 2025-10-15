import pygame
import math

class DrawManager:
    """Manages drawing game objects"""
    def __init__(self, game):
        self.game = game

        # Imported from game
        self.scroll_speed = game.settings.scroll_speed
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
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
        """Draw background, score and sprites"""
        margin = 8
        self._draw_background()
        self._draw_sprites()
        self.draw_score(margin, margin)

    def draw_text(self, text, x, y, center = False, bg_color = None, font = None, text_color = None):
        """Draw text on screen
        
        If font and text_color aren't provided, their default settings are chosen.
        """
        if font == None:
            font = self.settings.default_font
        if text_color == None:
            text_color = self.settings.default_font_color

        img = font.render(text, False, text_color, bg_color)
        img_rect = img.get_rect()

        # Center
        if center:
            img_rect.center = (x, y)
        else:
            img_rect.x, img_rect.y = (x, y)

        self.screen.blit(img, img_rect)

    def draw_score(self, x, y):
        """Draw score on screen"""
        self.draw_text(f"{self.game.score}", x, y)

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