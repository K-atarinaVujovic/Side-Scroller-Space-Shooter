import pygame

class CollisionManager:
    """Manages sprite collisions"""
    def __init__(self, game):
        self.game = game

        # == SPRITES ==
        # Player
        self.player_sprite = game.player_sprite
        self.player_sprites = game.player_sprites
        self.player_bullets = game.player_bullets

        # Asteroids
        self.asteroid_sprites = game.asteroid_sprites

        # Enemies
        self.enemy_sprites = game.enemy_sprites
        self.enemy_bullets = game.enemy_bullets


    def check_collisions(self):
        """Check for collisions and handle game state consequences"""
        # Check if player collided with an asteroid
        has_player_collided_asteroid = self._check_player_to_group_collision(self.asteroid_sprites)
        # Check if player collided with an enemy
        has_player_collided_enemy = self._check_player_to_group_collision(self.enemy_sprites)
        # Check if player was shot
        has_player_collided_bullet = self._check_player_to_group_collision(self.enemy_bullets)
        # Check if player shot an asteroid and remove the bullet
        shot_asteroid = self._check_group_to_group_collision(self.player_bullets, self.asteroid_sprites)
        # Check if player shot an enemy and remove the bullet
        shot_enemy = self._check_group_to_group_collision(self.player_bullets, self.enemy_sprites)

        
        if has_player_collided_asteroid or has_player_collided_enemy or has_player_collided_bullet:
            self.game.game_over = True

        if shot_enemy:
            self.enemy_sprites.remove(shot_enemy)
            self.game.score += 5
    
    def _check_player_to_group_collision(self, group):
        """Check if player collided with a sprite from the group"""
        if pygame.sprite.spritecollide(self.player_sprite, group, False, pygame.sprite.collide_rect):
            if pygame.sprite.spritecollide(self.player_sprite, group, False, pygame.sprite.collide_mask):
                return True
            
        return False
    
    def _check_group_to_group_collision(self, group_1, group_2):
        """Check if any of the bullets collided with a sprite from the group
        
        Returns collided sprite from group_2 if there was a collision, else None.
        """
        for sprite in group_2:
            if pygame.sprite.spritecollide(sprite, group_1, False, pygame.sprite.collide_rect):
                if pygame.sprite.spritecollide(sprite, group_1, True, pygame.sprite.collide_mask):
                    return sprite
                
        return None