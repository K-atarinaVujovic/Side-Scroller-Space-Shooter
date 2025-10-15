import pygame
from sprites.bullet import PlayerBullet
from sprites.asteroid import Asteroid

class SpriteManager:
    """Manages updating and spawning sprites"""
    def __init__(self, game):
        self.game = game

        # Sprites
        self.player_sprite = game.player_sprite
        self.player_sprites = game.player_sprites
        self.player_bullets = game.player_bullets
        self.asteroid_sprites = game.asteroid_sprites

        # Screen and settings
        self.screen = game.screen
        self.player_settings = game.player_settings
        self.asteroid_settings = game.asteroid_settings

    def check_spawns(self):
        """Check if a game object needs to be spawned"""
        # Check if player fired a bullet
        if self.player_sprite.shoot and self.player_sprite.bullet_cooldown <= 0:
            self._spawn_player_bullet()

        # Check if it's time to generate a new asteroid
        if self.game.asteroid_cooldown <= 0:
            self._spawn_asteroid()

    def update(self):
        """Update sprites and remove out-of-bounds sprites"""
        self.player_sprites.update(self.game.dt)
        self.player_bullets.update()
        self.asteroid_sprites.update()

        self._clean_up()

    def _spawn_player_bullet(self):
        """Add player bullet sprite and reset cooldown"""
        new_bullet = PlayerBullet(self.screen, self.player_settings, self.player_sprite.rect)
        self.player_bullets.add(new_bullet)
        self.player_sprite.bullet_cooldown = self.player_sprite.fire_rate

    def _spawn_asteroid(self):
        """Add asteroid and reset cooldown"""
        new_asteroid = Asteroid(self.screen, self.asteroid_settings)
        self.asteroid_sprites.add(new_asteroid)
        self.game.asteroid_cooldown = self.asteroid_settings.cooldown

    def _clean_up(self):
        """Cleans up sprites out of bounds"""
        self._clean_up_bullets()
        self._clean_up_asteroids()

    def _clean_up_bullets(self):
        """Clean up bullets out of bounds"""
        for bullet in self.player_bullets:
            if(bullet.rect.x > self.screen.get_rect().right):
                self.player_bullets.remove(bullet)

    def _clean_up_asteroids(self):
        """Clean up asteroids out of bounds"""
        for asteroid in self.asteroid_sprites:
            if(asteroid.rect.x > self.screen.get_rect().right):
                self.asteroid_sprites.remove(asteroid)