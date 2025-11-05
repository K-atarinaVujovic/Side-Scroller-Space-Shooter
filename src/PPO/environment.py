import gymnasium as gym
import numpy as np
from typing import Optional
import pygame
import sys
from side_scroller_space_shooter.game import Game
from PPO.helpers.draw_helper import DrawHelper
from PPO.helpers.obs_space_helper import ObsSpaceHelper
from PPO.helpers.reward_helper import RewardHelper

MAX_ENEMIES = 4
MAX_ASTEROIDS = 4
MAX_AGENT_BULLETS = 7
MAX_ENEMY_BULLETS = 7
MAX_STEPS = 2000

class Environment(gym.Env):
    """Gym environment"""
    def __init__(self, version = "", dont_draw = False):
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

        # For picking a reward system
        self.version = version
        
        # Initialize helpers
        self.draw_helper = DrawHelper(self.game)
        self.reward_helper = RewardHelper(self.game)
        self.obs_space_helper = ObsSpaceHelper(self.game, MAX_AGENT_BULLETS, MAX_ENEMIES, MAX_ENEMY_BULLETS, MAX_ASTEROIDS)


    def render(self, mode="human"):
        """Render the environment"""
        if mode == "human":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.game.draw_game()
            self.draw_helper.draw_info(self.episode, self.episode_reward, self.step_count, self.total_reward, self.total_steps)
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
        self.obs_space_helper.update_obs()

        # Terminate episode if agent died
        terminated = self.game.game_over

        # Check if it's time to end the episode
        truncated = self.step_count >= MAX_STEPS

        # Calculate reward
        reward = self.reward_helper.calculate_reward()
        # For render
        self.episode_reward += reward
        self.total_reward += reward

        observation = self._get_obs()
        info = self._get_info()

        if not self.dont_draw:
            self.render()

        return observation, reward, terminated, truncated, info

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

    def _get_info(self):
        """Get info, NOT IMPLEMENTED"""
        return {} 

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
