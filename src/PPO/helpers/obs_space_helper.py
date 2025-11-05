import numpy as np
from PPO.utils.utils import normalize

class ObsSpaceHelper:
    """Class with helper functions for updating observation space"""
    def __init__(self, game, max_agent_bullets, max_enemies, max_enemy_bullets, max_asteroids):
        self.game = game
        self.max_agent_bullets = max_agent_bullets
        self.max_enemy_bullets = max_enemy_bullets
        self.max_enemies = max_enemies
        self.max_asteroids = max_asteroids

    def update_obs(self):
        """Update observation space variables from game info"""
        self._agent_location = np.array([normalize(self.game.player_sprite.rect.centerx, self.game.settings.screen_width), normalize(self.game.player_sprite.rect.centery, self.game.settings.screen_height)], dtype=np.float32)

        self._agent_bullets = self._fill_sprite_positions_array(list(self.game.player_bullets), self.max_agent_bullets)
        self._enemy_locations = self._fill_sprite_positions_array(list(self.game.enemy_sprites), self.max_enemies)
        self._enemy_bullets = self._fill_sprite_positions_array(list(self.game.enemy_bullets), self.max_enemy_bullets)
        self._asteroid_locations = self._fill_sprite_positions_array(list(self.game.asteroid_sprites), self.max_asteroids)

    def _fill_sprite_positions_array(self, sprites, max_len, default=-1.0):
        """Fill array with sprite coordinates, and fill with default values up to max array size"""
        arr = np.full((max_len, 2), default, dtype=np.float32)
        for i, sprite in enumerate(sprites[:max_len]):
            arr[i, 0] = normalize(sprite.rect.centerx, self.game.settings.screen_width)
            arr[i, 1] = normalize(sprite.rect.centery, self.game.settings.screen_height)
        return arr