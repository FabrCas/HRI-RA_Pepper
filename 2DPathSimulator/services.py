import pygame as pg
import random

def random_position(screen, margin=20):
    x_r = random.randint(0 + margin, screen.get_width() - margin)
    y_r = random.randint(0 + margin, screen.get_height() - margin)
    return x_r, y_r

class InputInterpreter(object):
    def __init__(self):
        super().__init__()

    def execute(self, message):
        if "daje roma" in message.strip().lower():
            daje_roma = pg.mixer.Sound('static/daje_roma_daje.mp3')
            pg.mixer.Sound.play(daje_roma)
        pass


class PepperSocket():
    def __init__(self):
        super().__init__()