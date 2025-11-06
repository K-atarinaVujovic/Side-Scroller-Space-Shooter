import pygame

def play_sound():
    pygame.mixer.init()
    sound = pygame.mixer.Sound("audio/grimm_troupe.mp3")

    sound.play(loops=-1)

    input("Press Enter to quit: ")
    sound.stop()