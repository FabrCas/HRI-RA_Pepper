import pygame as pg
import random

def random_position(screen, margin=20):
    x_r = random.randint(0 + margin, screen.get_width() - margin)
    y_r = random.randint(0 + margin, screen.get_height() - margin)
    return x_r, y_r

class InputInterpreter(object):
    def __init__(self, simulation_objects):
        super().__init__()
        self.ui = simulation_objects['UI_DOs']
        self.boxes = simulation_objects['text_boxes']
        self.env = simulation_objects['environment']
        self.reset = False
        self.changed_debug = False
        self.changed_show_obstacles = False
        self.boxes[1].add_message("Started the simulation")

    def execute(self, message):
        if "daje roma" in message.strip().lower():
            daje_roma = pg.mixer.Sound('static/sounds/daje_roma_daje.mp3')
            pg.mixer.Sound.play(daje_roma)
        if "reset" in message.strip().lower():
            print("Resetting the environment...")
            self.reset = True
        if "debug" in message.strip().lower():
            print("Changing the debug mode...")
            self.changed_debug = True
        if "obs" in message.strip().lower():
            print("Changing the show obstacles mode...")
            self.changed_show_obstacles = True

    def update_debug(self, debug):
        if self.changed_debug:

            # change value
            if debug: debug = False
            else: debug = True

            # restore default value for input interpreter
            self.changed_debug = False

            # output message
            self.boxes[1].add_message(f"Debug mode: {debug}")

        return debug

    def toggle_show_obstacles(self, show_obstacles):
        if self.changed_show_obstacles:

            # change value
            if show_obstacles: show_obstacles = False
            else: show_obstacles = True

            # restore default value for input interpreter
            self.changed_show_obstacles = False

            # output message
            self.boxes[1].add_message(f"show obstacles mode: {show_obstacles}")

        return show_obstacles




class PepperSocket():
    def __init__(self):
        super().__init__()