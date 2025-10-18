import pygame
from side_scroller_space_shooter.sprites.bullet import PlayerBullet, EnemyBullet
from side_scroller_space_shooter.sprites.asteroid import Asteroid
from side_scroller_space_shooter.sprites.spaceship import EnemySpaceship

# import os
# import sys
# import inspect

# # currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# sys.path.insert(1, os.path.join(sys.path[0], '..'))


class SpriteManager:
    """Manages updating and spawning sprites"""
    def __init__(self, game):
        self.game = game

        # Sprites
        self.player_sprite = game.player_sprite
        self.player_sprites = game.player_sprites
        self.player_bullets = game.player_bullets
        self.asteroid_sprites = game.asteroid_sprites
        self.enemy_sprites = game.enemy_sprites
        self.enemy_bullets = game.enemy_bullets

        # Screen and settings
        self.screen = game.screen
        self.player_settings = game.player_settings
        self.asteroid_settings = game.asteroid_settings
        self.enemy_settings = game.enemy_settings

    def check_spawns(self):
        """Check if a game object needs to be spawned"""
        # Check if player fired a bullet
        if self.player_sprite.shoot and self.player_sprite.bullet_cooldown <= 0:
            self._spawn_bullet(PlayerBullet, self.player_sprite.rect)
            self.player_sprite.bullet_cooldown = self.player_settings.fire_rate

        # Check if an enemy fired a bullet
        for enemy in self.enemy_sprites:
            if enemy.shoot:
                self._spawn_bullet(EnemyBullet, enemy.rect)
                enemy.shoot = False

        # Check if it's time to generate a new asteroid
        if self.game.asteroid_spawn_cooldown <= 0:
            self._spawn_asteroid()

        # # Check if it's time to generate a new enemy
        if self.game.enemy_spawn_cooldown <= 0:
            self._spawn_enemy()



    def update(self):
        """Update sprites and remove out-of-bounds sprites"""
        # Player
        self.player_sprites.update(self.game.dt)
        self.player_bullets.update()

        # Asteroids
        self.asteroid_sprites.update()

        # Enemies
        self.enemy_sprites.update(self.game.dt)
        self.enemy_bullets.update()

        self._clean_up()

    def _spawn_bullet(self, bullet_class, shooter_rect):
        """Spawn player bullet sprite and reset cooldown"""     
        group = None
        settings = None
        if(bullet_class == PlayerBullet):
            group = self.player_bullets
            settings = self.player_settings
        else:
            group = self.enemy_bullets
            settings = self.enemy_settings

        new_bullet = bullet_class(self.screen, settings, shooter_rect)
        group.add(new_bullet)

    def _spawn_asteroid(self):
        """Spawn asteroid and reset cooldown"""
        new_asteroid = Asteroid(self.screen, self.asteroid_settings)
        self.asteroid_sprites.add(new_asteroid)
        self.game.asteroid_spawn_cooldown = self.asteroid_settings.spawn_cooldown

    def _spawn_enemy(self):
        """Spawn enemy"""
        new_enemy = EnemySpaceship(self.screen, self.enemy_settings)
        self.enemy_sprites.add(new_enemy)
        self.game.enemy_spawn_cooldown = self.enemy_settings.calculate_spawn_cooldown()

    def _clean_up(self):
        """Cleans up sprites out of bounds"""
        self._clean_up_group(self.player_bullets)
        self._clean_up_group(self.asteroid_sprites)
        self._clean_up_group(self.enemy_sprites)
        self._clean_up_group(self.enemy_bullets)

    def _clean_up_group(self, group):
        """Cleans up sprites in group out of bounds"""
        for sprite in group:
            if(sprite.rect.x > self.screen.get_rect().right):
                group.remove(sprite)