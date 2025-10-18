from PPO.environment import Environment
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from gymnasium.utils.env_checker import check_env
from PPO.arguments import get_train_args
import time
import os
import pygame

MODELS_PATH = "PPO/models/"
TENSORBOARD_PATH = "PPO/tensorboard/"

def train(args):
    timesteps, model_path, model_name, runs, dont_draw, v = _parse_args(args)

    log_path = TENSORBOARD_PATH + model_name + "/"

    if(dont_draw):
        os.environ["SDL_VIDEODRIVER"] = "dummy"

    env = Monitor(Environment(v, dont_draw))

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

    # Log additional info
    info = _get_reward_info(v)
    with open(log_path + "additional_info.txt", "w") as f:
        f.write(info)

    # # Training finished, come back!!
    # pygame.mixer.init()
    # sound = pygame.mixer.Sound("audio/grimm_troupe.mp3")

    # sound.play(loops=-1)

    # input("Press Enter to quit: ")
    # sound.stop()
 

def _get_reward_info(v):
    """Returns text explaining the rewards. Used for logging."""
    if v == "v2":
        shoot = 500
        shoot_close = "0.08 / (1 + normalized_distance)**2"
        lose = -400

        text = f"Reward for shooting enemy: {shoot}\n"
        text += f"Reward for shooting close to enemy: {shoot_close}\n"
        text += f"Punishment for losing: {lose}"
    elif v == "v3":
        shoot = 550
        shoot_close = "1.7 / (1 + normalized_distance)"
        lose = -400
        survival = 0.05

        text = f"Reward for shooting enemy: {shoot}\n"
        text += f"Reward for shooting close to enemy: {shoot_close}\n"
        text += f"Punishment for losing: {lose}"
        text += f"Punish for being close to enemy/obstacle/bullet: -1 Asteroid: -1.1\n"
    
    elif v == "v4":
        shoot = 550
        shoot_reward = "2.5 / (1 + normalized_distance)"
        obstacle_close = "1 / (1 + normalized_distance)"
        lose = -400
        # survival = 0.05

        text = f"Reward for shooting enemy: {shoot}\n"
        text += f"Reward for shooting close to enemy: {shoot_reward}\n"
        # text += f"Reward for survival: {survival}\n"
        text += f"Punishment for losing: {lose}\n"
        text += f"Punish for being close to enemy/obstacle/bullet: -1.2* Asteroid: -1.3*\n"

    return text

def _parse_args(args):
    timesteps = args.timesteps
    runs = args.runs
    dont_draw = args.dont_draw
    v = args.version

    if args.model == "":
        model_path = MODELS_PATH + "PPO_model"
    else:
        model_path = MODELS_PATH + args.model

    model_name = args.model

    return timesteps, model_path, model_name, runs, dont_draw, v

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

