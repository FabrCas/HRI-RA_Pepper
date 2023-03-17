import pygame as pg


class InputInterpreter(object):
    def __init__(self):
        super().__init__()

    def execute(self, message):
        if message.strip().lower() == "daje roma daje":
            daje_roma = pg.mixer.Sound('static/daje_roma_daje.mp3')
            pg.mixer.Sound.play(daje_roma)
        pass


class PepperSocket():
    def __init__(self):
        super().__init__()