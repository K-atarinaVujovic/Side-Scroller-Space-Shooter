import argparse

def get_train_args():
    """Get training arguments"""
    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--timesteps", type=int, default=25000)
    parser.add_argument("-r", "--runs", type=int, default=1)
    parser.add_argument("-m", "--model", type=str, default="")
    parser.add_argument("-dd", "--dont-draw", action="store_true")

    args = parser.parse_args()

    return args

def get_play_args():
    """Get play arguments"""
    parser = argparse.ArgumentParser()

    parser.add_argument("-m", "--model", type=str, default="")

    args = parser.parse_args()

    return args