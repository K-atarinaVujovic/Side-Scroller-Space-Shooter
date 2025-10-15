import pygame

class CollisionManager:
    """Manages sprite collisions"""
    def __init__(self, game):
        self.game = game

        # Sprites
        self.player_sprite = game.player_sprite
        self.player_sprites = game.player_sprites
        self.player_bullets = game.player_bullets
        self.asteroid_sprites = game.asteroid_sprites

    def check_collisions(self):
        """Check for collisions and handle game state consequences"""
        # Player and asteroid
        if pygame.sprite.spritecollide(self.player_sprite, self.asteroid_sprites, False, pygame.sprite.collide_rect):
            if pygame.sprite.spritecollide(self.player_sprite, self.asteroid_sprites, False, pygame.sprite.collide_mask):
                self.game.game_over = True
                print("Asteroid collision!")

    