from PPO.environment import Environment
from stable_baselines3 import PPO
from gymnasium.utils.env_checker import check_env

def train():
    env = Environment()

    try:
        check_env(env)
        print("Environment passes all checks!")
    except Exception as e:
        print(f"Environment has issues: {e}")

if __name__ == "__main__":
    train()