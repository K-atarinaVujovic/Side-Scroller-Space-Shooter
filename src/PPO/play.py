from PPO.environment import Environment
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from gymnasium.utils.env_checker import check_env
from PPO.arguments import get_play_args

MODELS_PATH = "PPO/models/"

def play(args):
    model_path = _parse_args(args)

    env = Monitor(Environment())

    model = PPO("MultiInputPolicy", env, verbose=1)

    try:
        model = model.load(model_path, env)
    except:
        print("Error loading model")
        exit()       

    obs, _ = env.reset()
    while True:
        action, _ = model.predict(obs)
        obs, rewards, terminated, truncated, info = env.step(action)
        if terminated or truncated:
            obs, _ = env.reset()
        # env.render()
    

def _parse_args(args):
    if args.model == "":
        model_path = MODELS_PATH + "PPO_model"
    else:
        model_path = MODELS_PATH + args.model

    return model_path

if __name__ == "__main__":
    args = get_play_args()
    play(args)

