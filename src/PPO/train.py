from PPO.environment import Environment
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from gymnasium.utils.env_checker import check_env
from PPO.arguments import get_train_args

MODELS_PATH = "PPO/models/"
TENSORBOARD_PATH = "PPO/tensorboard/"

def train(args):
    timesteps, model_path, model_name, runs, dont_draw = _parse_args(args)

    log_path = TENSORBOARD_PATH + model_name + "/"
    env = Monitor(Environment(dont_draw))

    model = PPO("MultiInputPolicy", env, verbose=1, tensorboard_log=log_path)

    try:
        model = model.load(model_path, env)
    except:
        print("Couldn't load, making new...")       

    model.learn(total_timesteps=timesteps, tb_log_name=f"run", reset_num_timesteps=False)
    model.save(model_path)

    # Log additional info
    info = _get_reward_info()
    with open(log_path + "additional_info.txt", "w") as f:
        f.write(info)
 

def _get_reward_info():
    """Returns text explaining the rewards. Used for logging."""
    shoot = 500
    shoot_close = "0.05 / (1 + normalized_distance)**2"
    lose = -700

    text = f"Reward for shooting: {shoot}\n"
    text += f"Reward for shooting close to enemy: {shoot_close}\n"
    text += f"Punishment for losing: {lose}"

    return text

def _parse_args(args):
    timesteps = args.timesteps
    runs = args.runs
    dont_draw = args.dont_draw

    if args.model == "":
        model_path = MODELS_PATH + "PPO_model"
    else:
        model_path = MODELS_PATH + args.model

    model_name = args.model

    return timesteps, model_path, model_name, runs, dont_draw

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

