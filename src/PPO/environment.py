import gymnasium as gym
import numpy as np
from typing import Optional
import pygame
import sys
from side_scroller_space_shooter.game import Game

MAX_ENEMIES = 4
MAX_ASTEROIDS = 4
MAX_AGENT_BULLETS = 7
MAX_ENEMY_BULLETS = 7
MAX_STEPS = 2000

class Environment(gym.Env):
    """Gym environment"""
    def __init__(self, dont_draw):
        metadata = {"render_modes": ["human"]}
        self.game = Game()
        self.screen_width = self.game.settings.screen_width
        self.screen_height = self.game.settings.screen_height
        
        # Actions:
        # [up down left right shoot]
        self.action_space = gym.spaces.MultiBinary(5)

        # Initialize observation space
        self._agent_location = np.array([-1.0, -1.0], dtype=np.float32)
        self._agent_bullets = np.full((MAX_AGENT_BULLETS, 2), -1.0, dtype=np.float32)
        self._asteroid_locations = np.full((MAX_ASTEROIDS, 2), -1.0, dtype=np.float32)
        self._enemy_locations = np.full((MAX_ENEMIES, 2), -1.0, dtype=np.float32)
        self._enemy_bullets = np.full((MAX_ENEMY_BULLETS, 2), -1.0, dtype=np.float32)

        self.observation_space = gym.spaces.Dict(
            {
                # Agent: centerx, centery
                "agent": gym.spaces.Box(low=-1, high=1, shape=(2,)),
                # Agent bullets: centerx, centery
                "agent_bullets": gym.spaces.Box(low=-1, high=1, shape=(MAX_AGENT_BULLETS, 2)),
                # Asteroid: centerx, centery
                "asteroids": gym.spaces.Box(low=-1, high=1, shape=(MAX_ASTEROIDS, 2)),
                # Enemy: centerx, centery
                "enemies": gym.spaces.Box(low=-1, high=1, shape=(MAX_ENEMIES, 2)),
                # Enemy bullets: centerx, centery
                "enemy_bullets": gym.spaces.Box(low=-1, high=1, shape=(MAX_ENEMY_BULLETS, 2))
            }
        )

        self.step_count = 0
        self.no_action = np.zeros(5, dtype=int)

        # For render and info logging
        self.episode_reward = 0
        self.episode = 0
        self.total_reward = 0
        self.dont_draw = dont_draw
        self.episode_steps = 0
        self.total_steps = 0

    def render(self, mode="human"):
        """Render the environment"""
        if mode == "human":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.game.draw_game()
            self._draw_info()
            pygame.display.update()

    def reset(self, seed: Optional[int] = None, options: Optional[dict] = None):
        """Start a new episode"""
        super().reset(seed=seed)

        self.episode += 1
        self.episode_reward = 0

        self.game.reset()
        self.step_count = 0

        observation = self._get_obs()
        info = self._get_info()

        return observation, info

    def step(self, action):
        """Execute one timestep within the environment"""
        self.step_count += 1
        self.total_steps += 1

        keys = self._action_to_keys(action)

        self.game.update_game_state(keys)

        # Update observation variables
        self._update_obs()

        # Terminate episode if agent died
        terminated = self.game.game_over

        # Check if it's time to end the episode
        truncated = self.step_count >= MAX_STEPS

        # Calculate reward
        reward = self._calculate_reward(action)
        # For render
        self.episode_reward += reward
        self.total_reward += reward

        observation = self._get_obs()
        info = self._get_info()

        if not self.dont_draw:
            self.render()

        return observation, reward, terminated, truncated, info

    def _draw_info(self):
        info_font = pygame.font.SysFont("Arial", 15)
        # Write current episode info
        text = f"Ep: {self.episode}    Rew: {self.episode_reward:10.3f}    Steps: {self.step_count:6}"
        x, y = self.game.settings.screen_width - 8, 8
        self.game.draw.draw_text(text, x, y, topright=True, font=info_font)
        # Write total info
        text = f"Total rew: {self.total_reward:20.3f}    Total steps: {self.total_steps:10}"
        x, y = self.game.settings.screen_width - 8, self.game.settings.screen_height - 8
        self.game.draw.draw_text(text, x, y, bottomright=True, font=info_font)

    def _calculate_reward(self, action):
        """Calculate reward.
        
        Rewards for shooting enemies and shooting close to enemies.
        Punishes for standing still and losing the game.
        """
        reward = 0
        # Reward for shooting enemy
        if self.game.shot_enemy:
            reward += 500.0

        # Reward for bullet close to enemy
        if self.game.enemy_sprites:
            min_bullet_to_enemy_distance = self._get_min_bullet_to_enemy_distance()
            normalized_distance = self._normalize(min_bullet_to_enemy_distance, 'x')
            reward += 0.05 / (1 + normalized_distance)**2

        # Punish for losing
        if self.game.game_over:
            reward -= 700.0

        return reward

    def _normalize(self, value, axis):
        """Return normalized value"""
        if axis=='x':
            return value / self.screen_width
        elif axis=='y':
            return value / self.screen_height
        else:
            return None

    def _update_obs(self):
        """Update observation space variables from game info"""
        self._agent_location = np.array([self._normalize(self.game.player_sprite.rect.centerx, 'x'), self._normalize(self.game.player_sprite.rect.centery, 'y')], dtype=np.float32)
        
        # Helper function
        def fill_array(sprites, max_len, default=-1.0):
            """Fill array with sprite coordinates, and fill with default values up to max array size"""
            arr = np.full((max_len, 2), default, dtype=np.float32)
            for i, sprite in enumerate(sprites[:max_len]):
                arr[i, 0] = self._normalize(sprite.rect.centerx, 'x')
                arr[i, 1] = self._normalize(sprite.rect.centery, 'y')
            return arr

        self._agent_bullets = fill_array(list(self.game.player_bullets), MAX_AGENT_BULLETS)
        self._enemy_locations = fill_array(list(self.game.enemy_sprites), MAX_ENEMIES)
        self._enemy_bullets = fill_array(list(self.game.enemy_bullets), MAX_ENEMY_BULLETS)
        self._asteroid_locations = fill_array(list(self.game.asteroid_sprites), MAX_ASTEROIDS)

    def _get_min_bullet_to_enemy_distance(self):
        """Calculate smallest distance between player bullets and an enemy"""
        bullets = self.game.player_bullets
        enemies = self.game.enemy_sprites

        # Initialize min distance
        min_distance = self.screen_width

        # If no bullets are shot or no enemies are on screen, return max distance
        if not bullets or not enemies:
            return min_distance

        for bullet in bullets:
            for enemy in enemies:
                dx = bullet.rect.centerx - enemy.rect.centerx
                dy = bullet.rect.centery - enemy.rect.centery
                distance = (dx**2 + dy**2)**0.5

                if distance < min_distance:
                    min_distance = distance

        return min_distance

    def _get_info(self):
        """Get info, NOT IMPLEMENTED"""
        return {}

    def _get_obs(self):
        """Convert internal state to observation format.

        Returns:
            dict: Observation with agent and target positions
        """
        return {"agent": self._agent_location,
                "agent_bullets": self._agent_bullets,
                "asteroids": self._asteroid_locations,
                "enemies": self._enemy_locations,
                "enemy_bullets": self._enemy_bullets}

    def _action_to_keys(self, action):
        """Convert MultiBinary action to pygame key state dict"""
        # Initialize all keys as not pressed
        keys = {
            pygame.K_UP: False,
            pygame.K_DOWN: False,
            pygame.K_LEFT: False,
            pygame.K_RIGHT: False,
            pygame.K_SPACE: False,
        }

        # Map each action bit to its key
        if action[0]:
            keys[pygame.K_UP] = True
        if action[1]:
            keys[pygame.K_DOWN] = True
        if action[2]:
            keys[pygame.K_LEFT] = True
        if action[3]:
            keys[pygame.K_RIGHT] = True
        if action[4]:
            keys[pygame.K_SPACE] = True

        return keys
