import pygame as pg
import random

def random_position(screen, margin=20):
    x_r = random.randint(0 + margin, screen.get_width() - margin)
    y_r = random.randint(0 + margin, screen.get_height() - margin)
    return x_r, y_r

class InputInterpreter(object):
    def __init__(self):
        super().__init__()
        self.reset = False

    def execute(self, message):
        if "daje roma" in message.strip().lower():
            daje_roma = pg.mixer.Sound('static/sounds/daje_roma_daje.mp3')
            pg.mixer.Sound.play(daje_roma)
        if "reset" in message.strip().lower():
            self.reset = True


class PepperSocket():
    def __init__(self):
        super().__init__()