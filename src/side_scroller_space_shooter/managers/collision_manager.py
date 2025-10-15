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
        self._check_player_asteroid_collision()
        self._check_bullet_asteroid_collision()

    

    def _check_player_asteroid_collision(self):
        if pygame.sprite.spritecollide(self.player_sprite, self.asteroid_sprites, False, pygame.sprite.collide_rect):
            if pygame.sprite.spritecollide(self.player_sprite, self.asteroid_sprites, False, pygame.sprite.collide_mask):
                self.game.game_over = True
                print("Asteroid collision!")

    def _check_bullet_asteroid_collision(self):
        for bullet in self.player_bullets:
            if pygame.sprite.spritecollide(bullet, self.asteroid_sprites, False, pygame.sprite.collide_rect):
                if pygame.sprite.spritecollide(bullet, self.asteroid_sprites, False, pygame.sprite.collide_mask):
                    print("Bullet collision!")
    