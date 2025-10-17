from PPO.environment import Environment
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from gymnasium.utils.env_checker import check_env
import pygame
import sys

MAX_STEPS = 25000

def train():
    env = Monitor(Environment())

    model = PPO("MultiInputPolicy", env, verbose=1)

    model.learn(total_timesteps=MAX_STEPS)
    model.save("models/saved_model")

    model = model.load("models/saved_model")

    obs, _ = env.reset()
    while True:
        action, _ = model.predict(obs)
        obs, rewards, terminated, truncated, info = env.step(action)
        if terminated or truncated:
            obs, _ = env.reset()
        env.render()
    

def _check_env(env):
    """Check if environment is compliant with gym requirements"""
    try:
        check_env(env)
        print("Environment passes all checks!")
    except Exception as e:
        print(f"Environment has issues: {e}")

if __name__ == "__main__":
    train()

