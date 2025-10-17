from side_scroller_space_shooter.game import Game
import gymnasium as gym
import numpy as np
from typing import Optional
import pygame

MAX_ENEMIES = 4
MAX_ASTEROIDS = 4
MAX_AGENT_BULLETS = 7
MAX_ENEMY_BULLETS = 7
MAX_STEPS = 2000

class Environment(gym.Env):
    """Gym environment"""
    def __init__(self):
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
                "agent": gym.spaces.Box(low=0, high=1, shape=(2,)),
                # Agent bullets: centerx, centery
                "agent_bullets": gym.spaces.Box(low=0, high=1, shape=(MAX_AGENT_BULLETS, 2)),
                # Asteroid: centerx, centery
                "asteroids": gym.spaces.Box(low=0, high=1, shape=(MAX_ASTEROIDS, 2)),
                # Enemy: centerx, centery
                "enemies": gym.spaces.Box(low=0, high=1, shape=(MAX_ENEMIES, 2)),
                # Enemy bullets: centerx, centery
                "enemy_bullets": gym.spaces.Box(low=0, high=1, shape=(MAX_ENEMY_BULLETS, 2))
            }
        )

        self.step_count = 0
        self.previous_action = np.zeros(5, dtype=int)
        self.no_action = np.zeros(5, dtype=int)

    def reset(self, seed: Optional[int] = None, options: Optional[dict] = None):
        """Start a new episode"""
        super().reset(seed=seed)

        self.game.reset()
        self.step_count = 0

        observation = self._get_obs()
        info = self._get_info()

        return observation, info

    def step(self, action):
        """Execute one timestep within the environment"""
        self.step_count += 1

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
        
        self.previous_action = action

        observation = self._get_obs()
        info = self._get_info()

        return observation, reward, terminated, truncated, info



    def _calculate_reward(self, action):
        """Calculate reward.
        
        Rewards for shooting enemies and shooting close to enemies.
        Punishes for standing still and losing the game.
        """
        reward = 0
        # Reward for shooting enemy
        if self.game.shot_enemy:
            reward += 1.0

        # Reward for bullet close to enemy
        min_bullet_to_enemy_distance = self._get_min_bullet_to_enemy_distance()
        normalized_distance = self._normalize(min_bullet_to_enemy_distance, 'x')
        reward += 1 / (1 + normalized_distance)
        
        # Discourage standing still
        if np.array_equal(action, self.no_action):
            reward -= 0.05

        # Punish for losing
        if self.game.game_over:
            reward -= 1.0

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
        self._agent_location = np.array([self._normalize(self.game.player_sprite.centerx, 'x'), self._normalize(self.game.player_sprite.centery, 'y')], dtype=np.float32)
        self._agent_bullets = np.array([[self._normalize(b.rect.centerx, 'x'), self._normalize(b.rect.centery, 'y')] for b in self.game.player_bullets], dtype=np.float32)
        self._enemy_locations = np.array([[self._normalize(e.rect.centerx, 'x'),self._normalize(e.rect.centery, 'y')] for e in self.game.enemy_sprites], dtype=np.float32)
        self._enemy_bullets = np.array([[self._normalize(b.rect.centerx, 'x'), self._normalize(b.rect.centery, 'y')] for b in self.game.enemy_bullets], dtype=np.float32)
        self._asteroid_locations = np.array([[self._normalize(a.rect.centerx, 'x'), self._normalize(a.rect.centery, 'y')] for a in self.game.asteroid_sprites], dtype=np.float32)

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
