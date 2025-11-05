import pygame

def get_reward_info(v):
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

def play_sound():
    pygame.mixer.init()
    sound = pygame.mixer.Sound("audio/grimm_troupe.mp3")

    sound.play(loops=-1)

    input("Press Enter to quit: ")
    sound.stop()