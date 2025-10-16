from side_scroller_space_shooter.game import Game
import gymnasium as gym
import numpy as np
from typing import Optional
import pygame

MAX_ENEMIES = 4
MAX_ASTEROIDS = 4
MAX_AGENT_BULLETS = 7
MAX_ENEMY_BULLETS = 7


class Environment(gym.Env):
    """Gym environment"""
    def __init__(self):
        self.game = Game()
        
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

    def reset(self, seed: Optional[int] = None, options: Optional[dict] = None):
        """Start a new episode"""
        super().reset(seed=seed)

        self.game.reset()

        observation = self._get_obs()
        info = self._get_info()

        return observation, info

    def step(self, action):
        """Execute one timestep within the environment"""
        keys = self._action_to_keys(action)

        self.game.update_game_state(keys)

        terminated = False
        truncated = False
        reward = 0 # TODO: implement reward mechanism

        observation = self._get_obs()
        info = self._get_info()

        return observation, reward, terminated, truncated, info


    def _get_info():
        """Get info, unused"""
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
