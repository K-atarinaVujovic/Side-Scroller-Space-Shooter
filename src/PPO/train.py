from PPO.environment import Environment
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from gymnasium.utils.env_checker import check_env
from PPO.arguments import get_train_args
import time
import os
from PPO.utils.logging_utils import play_sound

MODELS_PATH = "PPO/models/"
TENSORBOARD_PATH = "PPO/tensorboard/"

def train(args):
    """Train model"""
    timesteps, model_path, model_name, dont_draw = _parse_args(args)

    log_path = TENSORBOARD_PATH + model_name + "/"

    if(dont_draw):
        os.environ["SDL_VIDEODRIVER"] = "dummy"

    env = Monitor(Environment(dont_draw))

    model = PPO("MultiInputPolicy", env, verbose=1, tensorboard_log=log_path)

    try:
        model = model.load(model_path, env)
    except:
        print("Couldn't load, making new...")       

    # Start of training
    start = time.time()
    model.learn(total_timesteps=timesteps, tb_log_name=f"run", reset_num_timesteps=False)
    model.save(model_path)

    # End of training
    elapsed_sec = time.time() - start
    elapsed_min = elapsed_sec / 60
    print(f"{timesteps} steps took: {elapsed_min:.2f} minutes")

    # Training finished, come back!!
    play_sound()

def _parse_args(args):
    """Parse user arguments"""
    timesteps = args.timesteps
    dont_draw = args.dont_draw

    if args.model == "":
        model_path = MODELS_PATH + "PPO_model"
    else:
        model_path = MODELS_PATH + args.model

    model_name = args.model

    return timesteps, model_path, model_name, dont_draw

def _check_env(env):
    """Check if environment is compliant with gym requirements"""
    try:
        check_env(env)
        print("Environment passes all checks!")
    except Exception as e:
        print(f"Environment has issues: {e}")

if __name__ == "__main__":
    args = get_train_args()
    train(args)

