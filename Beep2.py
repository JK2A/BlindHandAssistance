import pygame

class Beep2(object):

    def __init__(self, filepath):
        pygame.mixer.init()
        pygame.mixer.music.load(filepath)
        pygame.mixer.music.set_volume(0)


    def change_volume(self, volume):
        pygame.mixer.music.set_volume(volume)

    def play(self):
        pygame.mixer.music.play(-1)
