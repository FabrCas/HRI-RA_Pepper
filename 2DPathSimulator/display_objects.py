import pygame as pg
import math
import time
import copy
import threading
from random import randint
from services import PepperMotion

# ---------------------------------------------- static and global variables

progDos_rects           = 1
progDos_static_images   = 1
progDos_buttons         = 1
progDos_texts           = 1
progDos_TextBoxes       = 1
progDos_room            = 1
progDos_door            = 1
progDos_window          = 1
progDos_furniture       = 1

font_path = "static/nasa_font.ttf"

tiles = {
    'parquet': 'static/texture/floor_parquet.jpg',
    'grey': 'static/texture/floor_grey_tiles.jpg',
    'white': 'static/texture/floor_white.jpg',
    'marble': 'static/texture/floor_marble.jpg',
    'black_marble': 'static/texture/floor_black_marble.jpg',
    'ceramic': 'static/texture/floor_ceramic.jpg',
    'parquet_strips': 'static/texture/floor_parquet_strips.jpg',
    'rhombus': 'static/texture/floor_rhombus.jpg',
    'test': 'static/texture/floor_test.png'
}

assets_furniture = {
    "apple"             : {"path": "static/assets/apple.png",            "is_movable": True,    "w": 500,   "h": 500},
    "armchair"          : {"path": "static/assets/armchair.png",         "is_movable": False,   "w": 250,   "h": 250},
    "bed"               : {"path": "static/assets/bed.png",              "is_movable": False,   "w": 500,   "h": 500},
    "big_table"         : {"path": "static/assets/big_table.png",        "is_movable": False,   "w": 500,   "h": 300},
    "big_table_chairs"  : {"path": "static/assets/big_table_chairs.png", "is_movable":  False,  "w": 500,   "h": 400},
    "cabinet"           : {"path": "static/assets/cabinet.png",          "is_movable": False,   "w": 500,   "h": 300},
    "cards"             : {"path": "static/assets/cards.png",            "is_movable": True,    "w": 500,   "h": 500},
    "chair"             : {"path": "static/assets/chair.png",            "is_movable": False,   "w": 300,   "h": 500},
    "coffee"            : {"path": "static/assets/coffee.png",           "is_movable": True,    "w": 500,   "h": 500},
    "glasses"           : {"path": "static/assets/glasses.png",          "is_movable": True,    "w": 500,   "h": 150},
    "green_marker"      : {"path": "static/assets/green_marker.png",     "is_movable": True,    "w": 50,    "h": 500},
    "kitchen"           : {"path": "static/assets/kitchen.png",          "is_movable": False,   "w": 1000,  "h": 300},
    "orange"            : {"path": "static/assets/orange.png",           "is_movable": True,    "w": 500,   "h": 500},
    "notebook_pink"     : {"path": "static/assets/notebook_pink.png",    "is_movable": True,    "w": 400,   "h": 500},
    "notebook_green"    : {"path": "static/assets/notebook_green.png",   "is_movable": True,    "w": 400,   "h": 500},
    "notebook_red"      : {"path": "static/assets/notebook_red.png",     "is_movable": True,    "w": 400,   "h": 500},
    "notebook_yellow"   : {"path": "static/assets/notebook_yellow.png",  "is_movable": True,    "w": 400,   "h": 500},
    "pen"               : {"path": "static/assets/pen.png",              "is_movable": True,    "w": 50,    "h": 500},
    "pencil"            : {"path": "static/assets/pencil.png",           "is_movable": True,    "w": 50,    "h": 500},
    "plant_1"           : {"path": "static/assets/plant_1.png",          "is_movable": False,   "w": 500,   "h": 500},
    "plant_2"           : {"path": "static/assets/plant_2.png",          "is_movable": False,   "w": 500,   "h": 500},
    "plate"             : {"path": "static/assets/plate.png",            "is_movable": True,    "w": 500,   "h": 500},
    "pool"              : {"path": "static/assets/pool.png",             "is_movable": False,   "w": 300,   "h": 500},
    "sink"              : {"path": "static/assets/sink.png",             "is_movable": False,   "w": 500,   "h": 300},
    "small_table"       : {"path": "static/assets/small_table.png",      "is_movable": False,   "w": 500,   "h": 250},
    "smartphone"        : {"path": "static/assets/smartphone.png",       "is_movable": True,    "w": 300,   "h": 500},
    "sofa"              : {"path": "static/assets/sofa.png",             "is_movable": False,   "w": 500,   "h": 250},
    "stove"             : {"path": "static/assets/stove.png",            "is_movable": False,   "w": 500,   "h": 500},
    "studio_chair"      : {"path": "static/assets/studio_chair.png",     "is_movable": False,   "w": 500,   "h": 500},
    "studio_table"      : {"path": "static/assets/studio_table.png",     "is_movable": False,   "w": 1000,  "h": 600},
    "toilet_water"      : {"path": "static/assets/toilet_water.png",     "is_movable": False,   "w": 250,   "h": 500},
    "toilet_sink"       : {"path": "static/assets/toilet_sink.png",      "is_movable": False,   "w": 500,   "h": 300},
    "tub"               : {"path": "static/assets/tub.png",              "is_movable": False,   "w": 250,   "h": 500},
    "tv_off"            : {"path": "static/assets/tv_off.png",           "is_movable": False,   "w": 500,   "h": 250},
    "tv_on"             : {"path": "static/assets/tv_on.png",            "is_movable": False,   "w": 500,   "h": 250}
}

# dictionary that describes positions (Vec2) where pepper should be placed when want to reach them
reach_positions = {
    "desk_studio":          pg.math.Vector2(104, 276),   # x=134
    "pool_studio":          pg.math.Vector2(215,185),
    "kitchenette":          pg.math.Vector2(179, 837),
    "table_kitchen":        pg.math.Vector2(275, 816),
    "bed":                  pg.math.Vector2(305, 485),
    "cabinet_bedroom_l":    pg.math.Vector2(360, 636),
    "cabinet_bedroom_r":    pg.math.Vector2(90, 636),
    "tv_bedroom":           pg.math.Vector2(225, 650),
    "water":                pg.math.Vector2(490, 80),
    "tub":                  pg.math.Vector2(490, 190),
    "sink":                 pg.math.Vector2(650, 229),
    "cabinet_toilet":       pg.math.Vector2(696, 90),
    "tv_living":            pg.math.Vector2(590, 325),
    "sofa":                 pg.math.Vector2(680, 487),
    "table_living":         pg.math.Vector2(590, 363),
    "armchair_l":           pg.math.Vector2(500, 453),  #to otheside add to y -100
    "armchair_r":           pg.math.Vector2(680, 452),  #to otheside add to y -100
    "table_dining":         pg.math.Vector2(635, 745)
}

# dictionary that describes positions (Vec2)  where pepper use to place grasped object
place_positions = {
    "desk_studio":          [pg.math.Vector2(134,306), pg.math.Vector2(154,306), pg.math.Vector2(174,306), pg.math.Vector2(194,306)],
    "pool_studio":          [pg.math.Vector2(160, 185)],
    "kitchenette":          [pg.math.Vector2(129,867), pg.math.Vector2(129,892), pg.math.Vector2(119, 788)],
    "table_kitchen":        [pg.math.Vector2(275, 776), pg.math.Vector2(275, 756)],
    "bed":                  [pg.math.Vector2(265, 515), pg.math.Vector2(265, 535),  pg.math.Vector2(235, 485)],
    "cabinet_bedroom_l":    [pg.math.Vector2(360, 696),pg.math.Vector2(345, 696),pg.math.Vector2(375, 696)],
    "cabinet_bedroom_r":    [pg.math.Vector2(90, 696),pg.math.Vector2(75, 696),pg.math.Vector2(105, 696)],
    "water":                [pg.math.Vector2(440, 85)],
    "tub":                  [pg.math.Vector2(465,190)],
    "sink":                 [pg.math.Vector2(615, 244)],
    "cabinet_toilet":       [pg.math.Vector2(751, 90),pg.math.Vector2(751, 70),pg.math.Vector2(751, 110)],
    "sofa":                 [pg.math.Vector2(630, 472)],
    "table_living":         [pg.math.Vector2(590, 403), pg.math.Vector2(570, 403), pg.math.Vector2(610, 403)],
    "armchair_l":           [pg.math.Vector2(500, 403)],
    "armchair_r":           [pg.math.Vector2(680, 407)],
    "table_dining":         [pg.math.Vector2(635, 780), pg.math.Vector2(635, 805), pg.math.Vector2(615, 780)]
}

# dictionary to define free_space position in the room
free_space_positions = {
    "foyer" :       pg.math.Vector2(875,122),
    "living_room":  pg.math.Vector2(745, 562),
    "dining":       pg.math.Vector2(740, 930),
    "toilet":       pg.math.Vector2(690, 80),
    "studio":       pg.math.Vector2(375, 135),
    "bedroom":      pg.math.Vector2(75, 440),
    "kitchen":      pg.math.Vector2(195, 932),
    "outdoor":      pg.math.Vector2(935, 635) 
}



# function used to retrieve all the display object for planning
rooms = []
windows = []
doors = []
furniture = []

def get_rooms():
    """
    :return: list containing all the rooms created
    """
    return rooms

def get_windows():
    """
    :return: list containing all the rooms created
    """
    return windows

def get_doors():
    """
    :return: list containing all the rooms created
    """
    return doors

def get_furniture():
    """
    :return: list containing all the rooms created
    """
    return furniture

"""
    Position attributes specification:
    1) x,y refers to the top left corner of the rect: Rect, StaticImage, Text, InputTextBox, OutputTextBox
        in general is used from pygame for all rect that contains DOs
    2) x,y refers to the center of the rect: Button, HouseElement
        in general us used from pygame to handle each kind of surface, if i take the rect from the surface i pass to (1)
"""

# ---------------------------------------------- [UI]

class Rect(pg.sprite.Sprite):
    """
        simple rect subclass that inherits the Sprite superclass, used for the creation of rectangular figures
    """

    def __init__(self, screen, x, y, width = 50, height = 50, color = (0,0,0), alpha = 255):
        super().__init__()

        self.screen = screen
        self.image = pg.Surface((width, height)).convert_alpha()
        self.width = width
        self.height = height
        self.image.fill((*color, alpha))
        self.rect = self.image.get_rect()
        # self.rect.center = (x, y)
        self.x = x
        self.y = y
        self.rect.x = x             # fix top left corner position
        self.rect.y = y             # fix top left corner position
        self.type_DO = "rect"

        global progDos_rects
        self.prog = progDos_rects
        progDos_rects += 1

    def draw(self):
        self.screen.blit(self.image,self.rect)

    def center_to(self, x=None, y=None):
        if x == None and y == None:
            return
        elif x == None:
            self.rect.center = (self.rect.center[0], y)
        elif y == None:
            self.rect.center = (x, self.rect.center[1])
        else:
            self.rect.center = (x, y)

class StaticImage(pg.sprite.Sprite):

    def __init__(self, file_path, screen, x, y, width=50, height=50):
        super().__init__()
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pg.image.load(file_path).convert_alpha()
        self.image = pg.transform.smoothscale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = self.x    #    (self.x, self.y)
        self.rect.y = self.y
        self.type_DO = 'static_image'

        global progDos_static_images
        self.prog = progDos_static_images
        progDos_static_images += 1

        print(f"Created {self.type_DO} n° {self.prog}: {file_path}")

    def draw(self):
        self.screen.blit(self.image,self.rect)

class Button(pg.sprite.Sprite):

    def __init__(self, name, screen,  x, y, width, height, type_button='on'):

        super().__init__()
        self.screen = screen
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.name = name
        self.status = type_button
        if type_button == 'on':
            self.image = pg.image.load("static/assets/green_bt.png").convert_alpha() # sprite for both on and off button
        elif type_button == 'off':
            self.image = pg.image.load("static/assets/red_bt.png").convert_alpha()
        else:
            raise ValueError("Wrong button type has been assigned")

        self.image = pg.transform.smoothscale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.last_click = None
        self.type_DO = 'button'
        self.sound = pg.mixer.Sound("static/sounds/button_click.mp3")

        global progDos_buttons
        self.prog = progDos_buttons
        progDos_buttons += 1

        print(f"Created {self.type_DO} ({self.name}) n° {self.prog}: status {self.status}")

    def change_status(self):
        # if needed can be used a cooling time variable to reduce the number of switch changes

        # if self.last_click == None:
        #     cooling_time = 1
        # else:
        #     cooling_time = abs(time.time() - self.last_click)
        # if cooling_time >0.2:
            # print(f"Button has been pressed at coordinates {mouse_pos}")
        # self.last_click = time.time()

        if self.status == 'on':
            print(f'button {self.name} goes to off')
            pg.mixer.Sound.play(self.sound)
            self.image = pg.image.load("static/assets/red_bt.png").convert_alpha()
            self.image = pg.transform.smoothscale(self.image, (self.width, self.height))
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)
            self.status = 'off'
            self.update()

        elif self.status == 'off':
            print(f'button {self.name} goes to on')
            pg.mixer.Sound.play(self.sound)
            self.image = pg.image.load("static/assets/green_bt.png").convert_alpha()
            self.image = pg.transform.smoothscale(self.image, (self.width, self.height))
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)
            self.status = 'on'
            self.update()

    def draw(self):
        self.screen.blit(self.image,self.rect)

class Text(pg.sprite.Sprite):

    def __init__(self, string, screen,  x, y,  color, size_font=30):
        super().__init__()
        self.string = string
        self.screen = screen
        self.x = x
        self.y = y
        self.size = size_font
        self.color = color
        self.type_DO = "text"
        global progDos_texts
        self.prog = progDos_texts
        progDos_texts += 1

        # create font object
        # self.font = pg.font.Font('freesansbold.ttf', self.size)
        self.font = pg.font.Font(font_path, self.size)

        # create display object and get its rect
        self.text = self.font.render(string, True, color)   # text, antialiasing, color, bg color
        self.rect = self.text.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.image = self.text

        print(f'Created {self.type_DO} n° {self.prog}: "{self.string.strip()}"')

    def center_to(self, x = None ,y = None):
        if x == None and y == None:
            return
        elif x == None:
            self.rect.center = (self.rect.center[0], y)
        elif y == None:
            self.rect.center = (x, self.rect.center[1])
        else:
            self.rect.center = (x, y)

    def draw(self):
        self.screen.blit(self.image,self.rect)

class InputTextBox():

    def __init__(self, screen, x, y, height, color_text, color_bg, size_font=30):
        self.screen = screen
        self.x = x
        self.y = y
        # self.width = width
        self.height = height
        self.size = size_font
        self.color_text = color_text
        self.color_bg = color_bg
        self.type_DO = "input text box"

        global progDos_TextBoxes
        self.prog = progDos_TextBoxes
        progDos_TextBoxes += 1

        # variable to manage filling of the box
        self.default_text = '*insert text here*'
        self.text_box = self.default_text
        self.box_active = False

        # create font object
        self.font = pg.font.Font(font_path, self.size)
        self.text = self.font.render(self.text_box, True, self.color_text)
        self.min_width = self.text.get_width() + 10   # minimum length when it's used the default text
        self.rect = pg.Rect(self.x, self.y, self.min_width, self.height)

        print(f"Created text box (input) n° {self.prog}")

    # specific render function, first render the text box and the text, with dynamic changes
    def draw(self, max_width=200):   #$render
        pg.draw.rect(self.screen, self.color_bg, self.rect)
        self.text = self.font.render(self.text_box, True, self.color_text)

        new_width = min(max_width, self.text.get_width() + 10)

        # stretch the box until the limit is reached
        if new_width > self.min_width:
            self.rect.w = new_width + 10

        # show partially the text if the new limit is reached
        if self.text.get_width() > self.rect.w:
            partial_text = self.text_box
            while(self.text.get_width() > self.rect.w - 10):
                partial_text = partial_text[1:]
                self.text = self.font.render(partial_text, True, self.color_text)

        self.screen.blit(self.text, (self.rect.x + 5, self.rect.y + 5))

    def restore_default(self):
        self.rect.w = self.min_width
        self.text_box = self.default_text

    def restore_empty(self):
        self.rect.w = self.min_width
        self.text_box = ""

class OutputTextBox():

    def __init__(self,screen, x, y, width, height, color_text, color_bg, size_font=30):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.size = size_font
        self.color_text = color_text
        self.color_bg = color_bg
        self.type_DO = "output text box"

        global progDos_TextBoxes
        self.prog = progDos_TextBoxes
        progDos_TextBoxes += 1

        self.messages = []
        self.default_text = ''
        self.text_box = ''

        # create font object
        self.font = pg.font.Font(font_path, self.size)
        self.text = self.font.render(self.text_box, True, self.color_text)
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)

        print(f"Created text box (output) n° {self.prog}")

    # specific render function, first render the text box (static) and adjust the text to fit in the box
    def draw(self):

        # draw the rect containing the text
        pg.draw.rect(self.screen, self.color_bg, self.rect)

        # define the max height, not all the messages can be visible, show the most recent until there is space
        max_height = self.rect.height - 15
        messages_height = 0
        visible_messages = []
        n_messages = 0
        while messages_height < max_height and n_messages +1 <= len(self.messages):
            message = self.messages[- (n_messages +1)]
            # print(message)
            if type(message) == str:
                message_height = self.font.render(message, True, self.color_text).get_height()
                messages_height += message_height
            elif type(message) == list:
                sub_messages_height = 0
                for sub_message in message:
                    sub_message_height = self.font.render(sub_message, True, self.color_text).get_height()
                    sub_messages_height += sub_message_height
                messages_height += sub_messages_height

            if messages_height < max_height:
                n_messages += 1
                visible_messages.insert(0, message)


        # print messages as lines after the split
        vertical_offset = 0
        for idx, message in enumerate(visible_messages):
            if type(message) == str:
                self.text = self.font.render(message, True, self.color_text)
                self.screen.blit(self.text, (self.rect.x + 5, self.rect.y + 5 + 25 *vertical_offset))
                vertical_offset += 1
            elif type(message) == list:
                for sub_message in message:
                    self.text = self.font.render(sub_message, True, self.color_text)
                    self.screen.blit(self.text, (self.rect.x + 5, self.rect.y + 5 + 25 * vertical_offset))
                    vertical_offset += 1



            # break

    def add_message(self, message):
        # define max width for the box
        max_width = self.rect.w - 15

        message = '- '+ message[0].upper() + message[1:]

        # create sub-messages if text is too long
        message_text = self.font.render(message, True, self.color_text)
        if message_text.get_width() + 10 > max_width: # sub-messages are needed
            sub_messages = []

            while (message != ''):
                sub_message = message
                words = sub_message.split(' ')
                sub_message_text = self.font.render(sub_message, True, self.color_text)

                while (sub_message_text.get_width() > max_width):
                    sub_messages_list = sub_message.split(' ')
                    sub_message = ' '.join(sub_messages_list[:-1])

                    # sub_message = sub_message.replace(words[-1], '')
                    sub_message_text = self.font.render(sub_message, True, self.color_text)

                message = message.replace(sub_message, '').strip()
                if sub_messages != []:
                    sub_message = '   ' + sub_message
                sub_messages.append(sub_message)

            self.messages.append(sub_messages)
        else:
            self.messages.append( message)

    def restore_default(self):
        self.text_box = self.default_text

# ---------------------------------------------- [Simulation]

class HouseElement(pg.sprite.Sprite):
    def __init__(self, name, screen, group, x, y, width, height):   # x and y center of the DO box rectangle
        super().__init__()
        self.name = name
        self.screen = screen
        self.group = group
        self.x = x   # refers to center
        self.y = y   # refers to center
        self.width = width
        self.height = height
        self.rel_angle = 0
        self.rect_gfx = None


        if (type(self).__name__ == "Room"):
            global progDos_room
            self.prog = progDos_room
            progDos_room += 1
            self.type_DO = "Room"

        elif (type(self).__name__ == "Door"):
            global progDos_door
            self.prog = progDos_door
            progDos_door += 1
            self.type_DO = "Door"

        elif (type(self).__name__ == "Window"):
            global progDos_window
            self.prog = progDos_window
            progDos_window += 1
            self.type_DO = "Window"

        elif (type(self).__name__ == "Furniture"):
            global progDos_furniture
            self.prog = progDos_furniture
            progDos_furniture += 1
            self.type_DO = "furniture"

        elif (type(self).__name__ == "Pepper"):
            self.type_DO = "Pepper"
            self.prog = None

        if self.prog != None:
            print(f"Created {self.type_DO} ({self.name}) n° {self.prog}")
        else:
            print(f"Created Pepper!")


    def get_display_name(self, side = 'top', color = (255, 255, 255), size_font = 30):  # edge: 'top','bottom'

        vertices = self.get_vertices()
        if side == 'top':
            pos_text_x = vertices['left-top'][0] + self.width/2
            pos_text_y = vertices['left-top'][1] + 20
        elif side == 'bottom':
            pos_text_x = vertices['left-down'][0] + self.width/2
            pos_text_y = vertices['left-down'][1] - 20
        else:
            raise ValueError("Invalid edge location as parameter!")

        text_dos = Text(self.name, screen=self.screen, x=pos_text_x, y= pos_text_y, color=color, size_font=size_font)
        text_dos.center_to(x = pos_text_x, y = pos_text_y)

        return text_dos

    # function to rotate a single point around a pivot using the relative angle property
    def _rotate_point(self, pivot, point, angle = None):

        if angle == None: angle = self.rel_angle

        # needed transformation from degrees to radians
        angle = - math.radians(angle)

        # rotate clockwise so i do the complement of the angle (+ -> ccw, - -> cw)
        x = round((math.cos(angle) * (point[0] - pivot[0])) -
                       (math.sin(angle) * (point[1] - pivot[1])) +
                       pivot[0])
        y = round((math.sin(angle) * (point[0] - pivot[0])) +
                       (math.cos(angle) * (point[1] - pivot[1])) +
                       pivot[1])

        return (x, y)



    def _rotate_central_anim(self, image, angle):
        """
            Function to call for central rotation during animation, this avoid the distortion from each approximation
        """
        self.image = pg.transform.rotate(image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def _rotate_pivot_anim(self, image, pivot, offset, angle):
        """

        :param image: the new image to be rotated
        :param pivot: point (2D vector) that represent the pivot point on the screen surface, (global coordinates)
        :param offset: distance (2D vector) that represent how much the surface should be displaced from the central rotation (relative coordinates)
        :param angle: the angle for the rotation
        :return: None
        """
        self.image = pg.transform.rotate(image, angle)
        rotated_offset = offset.rotate(-angle)
        self.rect = self.image.get_rect(center = pivot + rotated_offset)

    def print_shape(self):
        print("Rect center -> ",       self.rect.center)
        print("Rect topleft -> ",      self.rect.topleft)
        print("Rect topright -> ",     self.rect.topright)
        print("Rect bottomleft -> ",   self.rect.bottomleft)
        print("Rect bottomright -> ",  self.rect.bottomright, "\n")

    def get_vertices(self):

        center_x = self.rect.center[0]
        center_y = self.rect.center[1]
        pivot = (center_x, center_y)

        # left_top corner
        lt = (center_x - self.width/2, center_y - self.height/2)
        ltr = self._rotate_point(pivot, lt)
        # right_top corner
        rt = (center_x + self.width/2, center_y - self.height/2)
        rtr = self._rotate_point(pivot, rt)
        # left_down  corner
        ld = (center_x - self.width/2, center_y + self.height/2)
        ldr = self._rotate_point(pivot, ld)
        # # right_down corner
        rd = (center_x + self.width/2, center_y + self.height/2)
        rdr = self._rotate_point(pivot, rd)

        vertices = {
            'left-top':     ltr,
            'right-top':    rtr,
            'left-down':    ldr,
            'right-down':   rdr
        }
        return vertices


    def draw(self):
        self.screen.blit(self.image, self.rect)

    # create or remove the graphic representation of the rect containing  the surface

    def display_gfxRect(self, x=None, y=None, width=None, height=None):
        if (x == None) and (y == None) and (width == None) and (height == None):
            self.rect_gfx = Rect(self.screen, self.rect.topleft[0], self.rect.topleft[1], self.rect.width, self.rect.height, (255,0,0), alpha= 100)
        else:
            if type(self).__name__ == "Furniture" and self.is_movable:
                self.rect_gfx = Rect(self.screen, x, y, width, height, (0, 0, 255), alpha=100)
            else:
                self.rect_gfx = Rect(self.screen, x, y, width, height, (255, 0, 0), alpha=100)

    def remove_gfxRect(self):
        if self.rect_gfx: self.group.remove(self.rect_gfx)
        del self.rect_gfx
        self.rect_gfx = None

    # functions for the debug mode in rendering

    def render_debug_vertices(self):
        vertices = self.get_vertices()
        pg.draw.circle(self.screen, (0,0, 255), (self.x, self.y), radius= 10)
        for v in list(vertices.values()):
            pg.draw.circle(self.screen, (255,0,0), v, radius = 5)

    def render_debug_rect(self):
        if not(self.rect_gfx is None):
            self.rect_gfx.draw()

class Room(HouseElement):

    def __init__(self, name, screen, x, y, width, height, env_group, tile_type='test'):
        super().__init__(name, screen, env_group, x, y, width, height)
        self.max_w_tile = 100
        self.max_h_tile = 100
        self.image = pg.Surface((width, height), pg.SRCALPHA)

        # full the surface with the image
        for i in range(math.ceil(self.width/self.max_w_tile)):
            for j in range(math.ceil(self.height/self.max_h_tile)):
                tmp_image = pg.image.load(tiles[tile_type]).convert_alpha()
                tmp_image = pg.transform.smoothscale(tmp_image, (self.max_w_tile, self.max_h_tile)).convert_alpha()
                self.image.blit(tmp_image, (i*self.max_w_tile, j*self.max_h_tile))

        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        # list of elements
        self.bounds     = {}    # k: (str) side             v: list of tuple with x and y vector values for each segment
        self.windows    = {}    # k: (str) name             v: TUPLE for left window and right window
        self.doors      = {}    # k: (str) name             v: door display object
        self.furniture  = {}    # k: (str) name             v: furniture display object

        # add in the list of element for rendering
        self.group.add(self)

        # include the room in the global list
        global rooms
        rooms.append(self)

        self._create_boundaries()
        self.visible_boundaries = False

    def _create_boundaries(self):  # depth wall 10 pixels
        vertices = self.get_vertices()

        # initially the bounds are defined as a whole continuous interval
        top_wall    = [(pg.math.Vector2(vertices['left-top'])   , pg.math.Vector2(vertices['right-top'])    )]
        bottom_wall = [(pg.math.Vector2(vertices['left-down'])  , pg.math.Vector2(vertices['right-down'])   )]
        left_wall   = [(pg.math.Vector2(vertices['left-top'])   , pg.math.Vector2(vertices['left-down'])    )]
        right_wall  = [(pg.math.Vector2(vertices['right-top'])  , pg.math.Vector2(vertices['right-down'])   )]

        self.bounds['north'] = top_wall
        self.bounds['south'] = bottom_wall
        self.bounds['west'] = left_wall
        self.bounds['east'] = right_wall

    def _edit_boundaries(self, side, start, end):
        """
        Function used to change the shape of the room's boundaries when a door is inserted.
        this function decompose each segment side in sub-segments separated by the door

        :param side: (str) cardinal direction: north, south, east, west
        :param start: (int) start position (x or y based on the side) of the door
        :param end: (int) end position (x or y based on the side) of the door
        :return: None
        """
        bounds = self.bounds[side]
        start_position = start; end_position = end

        # invert if wrongly assigned start and end
        if start > end:
            tmp = end
            end_position = start_position
            start_position = tmp

        # initialize variables algorithm
        to_insert = []
        idx_delete = -1

        if   side == 'south' or side == 'north':   # check x
            for idx, bound in enumerate(bounds):
                if start_position > bound[0][0] and end_position < bound[1][0]:
                    first_new_bound  = (pg.math.Vector2(bound[0][0], bound[0][1]),pg.math.Vector2(start_position,bound[0][1]))
                    second_new_bound = (pg.math.Vector2(end_position,bound[1][1]),pg.math.Vector2(bound[1][0],bound[1][1]))
                    to_insert = [first_new_bound,second_new_bound]
                    idx_delete = idx
                    break
             # [(pg.math.Vector2(vertices['left-top']), pg.math.Vector2(vertices['right-top']))]
        elif side == 'west' or side == 'east':     # check y
            for idx, bound in enumerate(bounds):
                if start_position > bound[0][1] and end_position < bound[1][1]:
                    first_new_bound  = (pg.math.Vector2(bound[0][0], bound[0][1]),pg.math.Vector2(bound[0][0], start_position))
                    second_new_bound = (pg.math.Vector2(bound[1][0], end_position),pg.math.Vector2(bound[1][0],bound[1][1]))
                    to_insert = [first_new_bound,second_new_bound]
                    idx_delete = idx
                    break

        # insert the new interval removing the old one
        if idx_delete != -1:
            bounds.pop(idx_delete)
            bounds.insert(idx_delete, to_insert[0])
            bounds.insert(idx_delete+1, to_insert[1])

    def show_boundaries(self):
        self.visible_boundaries = True

    def hide_boundaries(self):
        self.visible_boundaries = False

    # def add_door(self, room: HouseElement):   #
    def add_door(self, name:str, other_room: HouseElement, status='close', displ = 0, is_main = False):
        """
        function that insert doors in the room. The door connects two rooms (edge graph like)
        :name -> string used for the name of the door, of the type d_$name
        :param other_room -> the adjacent room which is connected through the door
        :param status -> open or close
        :param is_main -> boolean variable to change asset for the frontal door

        reference points:
        N------------------------E
        |                        |
        |                        |
        |                        |
        |                        |
        |                        |
        W________________________S
        """

        vertices = self.get_vertices()

        x_interval_other = range(other_room.get_vertices()['left-down'][0]+1, other_room.get_vertices()['right-down'][0])
        x_midpoint_other = math.ceil(other_room.get_vertices()['right-down'][0] - (other_room.width/2))

        y_interval_other = range(other_room.get_vertices()['left-top'][1]+1, other_room.get_vertices()['left-down'][1])
        y_midpoint_other = math.ceil(other_room.get_vertices()['left-top'][1] + (other_room.height/2))

        x_interval = range(vertices['left-down'][0]+1, vertices['right-down'][0])
        x_midpoint = math.ceil(vertices['right-down'][0] - (self.width/2))
        y_interval = range(vertices['left-top'][1]+1, vertices['left-down'][1])
        y_midpoint = math.ceil(vertices['left-top'][1] + (self.height/2))

        door_width = 80
        wall_margin = 10

        # check adjacency rooms and if there is possibility to place the door, infer the side
        if (other_room.y + other_room.height/2 + wall_margin == self.y - self.height/2) \
            and (((x_midpoint + displ - door_width/2 in x_interval_other) and (x_midpoint + displ + door_width/2 in x_interval_other))\
            or  ( (x_midpoint_other + displ - door_width/2 in x_interval) and (x_midpoint_other + displ + door_width/2 in x_interval)) ):

            side = 'north'
            x_door = vertices['left-top'][0]
            y_door = vertices['left-top'][1]
            angle_door = 0
            if self.width > other_room.width:
                displacement = other_room.width/2 + displ
            else:
                displacement = self.width/2 + displ

        elif (other_room.x + other_room.width/2 + wall_margin == self.x - self.width/2)\
            and (((y_midpoint + displ - door_width/2 in y_interval_other) and (y_midpoint + displ + door_width/2 in y_interval_other))\
            or  ( (y_midpoint_other + displ - door_width/2 in y_interval) and (y_midpoint_other + displ + door_width/2 in y_interval)) ):

            side = 'west'
            x_door = vertices['left-down'][0]
            y_door = vertices['left-down'][1]
            angle_door = 90
            if self.height > other_room.height:
                displacement = other_room.height/2 + displ
            else:
                displacement = self.height/2 + displ

        elif (other_room.y - other_room.height/2 - wall_margin == self.y + self.height/2) \
            and (((x_midpoint + displ - door_width/2 in x_interval_other) and (x_midpoint + displ + door_width/2 in x_interval_other))\
            or  ( (x_midpoint_other + displ - door_width/2 in x_interval) and (x_midpoint_other + displ + door_width/2 in x_interval)) ):

            side = 'south'
            x_door = vertices['right-down'][0]
            y_door = vertices['right-down'][1]
            angle_door = 180
            if self.width > other_room.width:
                displacement = other_room.width/2 + displ
            else:
                displacement = self.width/2 + displ

        elif (other_room.x - other_room.width/2 - wall_margin == self.x + self.width/2)\
            and (((y_midpoint + displ - door_width/2 in y_interval_other) and (y_midpoint + displ + door_width/2 in y_interval_other)) \
            or  ( (y_midpoint_other + displ - door_width/2 in y_interval) and (y_midpoint_other + displ + door_width/2 in y_interval)) ):

            side = 'east'
            x_door = vertices['right-top'][0]
            y_door = vertices['right-top'][1]
            angle_door = 270
            if self.height > other_room.height:
                displacement = other_room.height/2 + displ
            else:
                displacement = self.height/2 + displ
        else:
            raise ValueError(f"No valid position for the adjacent room")


        # door = Door(self.name + "_" + side + "_" + str(displacement) + "_door", self.screen,
        #             x_door, y_door, angle_door, displacement, door_width, side, status, self,
        #             other_room, self.group, is_main)
        
        door = Door(name, self.screen,x_door, y_door, angle_door, displacement, door_width, side, status, self,
                    other_room, self.group, is_main)

        # add door object to the environment group
        self.group.add(door)

        # add door in the list of doors for the rooms
        self.doors[name] = door

        # i do the same for the adjacent room, using the opposite cardinal direction
        if side == 'north':
            self._edit_boundaries(side, x_door + displacement - door_width / 2, x_door + displacement + door_width / 2)
            other_room.doors['south'] = door
            other_room._edit_boundaries("south", x_door + displacement - door_width/2,
                                        x_door + displacement + door_width/2)
        elif side == 'west':
            self._edit_boundaries(side, y_door - displacement - door_width / 2, y_door - displacement + door_width / 2)
            other_room.doors['east'] = door
            other_room._edit_boundaries("east", y_door - displacement - door_width / 2,
                                  y_door - displacement + door_width / 2)
        elif side == 'south':
            self._edit_boundaries(side, x_door - displacement - door_width / 2, x_door - displacement + door_width / 2)
            other_room.doors['north'] = door
            other_room._edit_boundaries("north", x_door - displacement - door_width / 2,
                                        x_door - displacement + door_width / 2)
        elif side == 'east':
            self._edit_boundaries(side, y_door + displacement - door_width / 2, y_door + displacement + door_width / 2)
            other_room.doors['west'] = door
            other_room._edit_boundaries("west", y_door + displacement  - door_width / 2,
                                  y_door + displacement  + door_width / 2)

        return door

    def add_window(self, name:str, side: str, displacement: int, status='close'):
        """
        :name -> string used for the name of left and right window, left: wl_ + name, right: wr_ + name
        :param side -> north, west, south, east
        :param status -> open or close
        :param displacement -> pixel distance from the reference corner, used to place the window
        """
        vertices = self.get_vertices()

        if side == 'north':
            x_win = vertices['left-top'][0]
            y_win = vertices['left-top'][1]
            angle_win = 0
        elif side == 'west':
            x_win = vertices['left-down'][0]
            y_win = vertices['left-down'][1]
            angle_win = 90
        elif side == 'south':
            x_win = vertices['right-down'][0]
            y_win = vertices['right-down'][1]
            angle_win = 180
        elif side == 'east':
            x_win = vertices['right-top'][0]
            y_win = vertices['right-top'][1]
            angle_win = 270

        # left window with convention of being oriented downward (grip on the down side)

        window_l = Window("wl_" + name,
                        self.screen, x_win, y_win, angle_win, displacement, side, True, status, self, self.group)

        window_r = Window("wr_" + name,
                        self.screen, x_win, y_win, angle_win, displacement, side, False, status, self, self.group)

        # add window left and right in the group
        self.group.add(window_l)
        self.group.add(window_r)

        # add both windows as a tuple in the list of windows for the Room
        self.windows[name] = (window_l,window_r)

        return window_l, window_r

    def add_furniture(self, name:str, type_forniture, x, y, width, height, rotation, flip_x=False, flip_y=False):

        house_component = Furniture(name, self.screen, self.group, type_forniture, x, y,\
                                    width, height, rotation, self, flip_x, flip_y)

        self.furniture[name] = house_component
        self.group.add(house_component)

    def draw(self, width_line = 5):
        super().draw()
        if self.visible_boundaries:
            for segment in self.bounds['north']:
                pg.draw.line(self.screen, (255, 0, 0), start_pos= segment[0], end_pos=segment[1], width=width_line)
            for segment in self.bounds['south']:
                pg.draw.line(self.screen, (255, 0, 0), start_pos= segment[0], end_pos=segment[1], width=width_line)
            for segment in self.bounds['east']:
                pg.draw.line(self.screen, (255, 0, 0), start_pos= segment[0], end_pos=segment[1], width=width_line)
            for segment in self.bounds['west']:
                pg.draw.line(self.screen, (255, 0, 0), start_pos= segment[0], end_pos=segment[1], width=width_line)

class Door(HouseElement):  # used to connect two rooms or a room and the outdoor
    def __init__(self, name, screen, x, y, angle_side, displacement, door_width, side, status, room_a, room_b, group, is_main = False):
        super().__init__(name, screen, group, x, y, width= door_width, height= 100) # door_width = 80 ;height= 100

        self.status = status            # status(str) -> open || close
        self.side = side                # side(str) -> north || west || south || east
        self.angle_side = angle_side    # global angle (int) respect the world (screen) when windows are closed
        self.rel_angle = 0              # relative angle (int) from the creation reference frame
        self.angle_open = - 90          # relative angle (int) that represent the open state
        self.angle_close = 0            # relative angle (int) that represent the close state
        self.rooms = (room_a, room_b)   # the two rooms that are connected from the door, the door rotates in direction of the first
        self.displacement = displacement
        self.is_main = is_main
        self.shape = (self.width, 10)

        # variable to handle animation
        self.is_opening = False
        self.is_closing = False

        # load images
        self._load_images()

        # correct positions and get rect
        new_rect = self._correctionPos()
        self.rect = new_rect

        # compute reduced rect for white surface of opened door
        self.rect_open = self._get_reduced_rect()

        # correct angle based on status
        self._correctionStatus()

        # create debug rect
        x_, y_, w_, h_ = self._get_gfx_shape()
        self.display_gfxRect(x_, y_, w_, h_)

        # load sound effects
        self.sound_open = pg.mixer.Sound("static/sounds/open_door.mp3")
        self.sound_close = pg.mixer.Sound("static/sounds/close_door.mp3")
        
        
        global doors
        doors.append(self)


    def _transformation_image(self, image):
        # upscale/downscale, rotate
        image = pg.transform.smoothscale(image, (self.width, self.height))
        image = pg.transform.rotate(image, self.angle_side)
        return image

    def _get_reduced_rect(self):
        """
        :return: reduced rect from the transparent asset of the door, used to show when it's open
        """
        init_rect = self.rect.copy()


        if self.side == 'north':
            init_rect.height = 10
            init_rect.y = self.rect.center[1] - 5    # rect needs the top left corner, so remove the half width offset
            init_rect.width -= 3                     # next 3 lines are to enhance aspect
            init_rect.center = self.rect.center
            init_rect.x += 4
        elif self.side == 'south':
            init_rect.height = 10
            init_rect.y = self.rect.center[1] - 5
            init_rect.width -= 3
            init_rect.center = self.rect.center
            init_rect.x -= 4
        elif self.side == 'west':
            init_rect.width = 10
            init_rect.x = self.rect.center[1] - 5
            init_rect.height -= 3
            init_rect.center = self.rect.center
            init_rect.y -= 4
        elif self.side == 'east':
            init_rect.width = 10
            init_rect.x = self.rect.center[1] - 5
            init_rect.height -= 3
            init_rect.center = self.rect.center
            init_rect.y += 4

        return init_rect

    def _get_gfx_shape(self):
        if self.side in ["north", "south"]:
            width = self.rect.width
            height = 1/5 * self.rect.height
            if self.status == "open":
                width = math.ceil(width * 4/5)

        elif self.side in ["east", "west"]:
            width = 1/5 * self.rect.width
            height = self.rect.height
            if self.status == "open":
                height= math.ceil(height * 4/5)

        if self.status == "open":
            tmp = width
            width = height
            height = tmp

        x = self.rect.topleft[0] + math.ceil((self.rect.width - width) / 2)
        y = self.rect.topleft[1] + math.ceil((self.rect.height - height) / 2)

        return x, y, width, height

    def _load_images(self):
        if not(self.is_main):
            self.image_door = pg.image.load("static/assets/door.png").convert_alpha()
        else:
            self.image_door = pg.image.load("static/assets/main_door.png").convert_alpha()
        self.image = self.image_door.copy()
        self.image = self._transformation_image(self.image)

    def _correctionPos(self, vertical_offset=5):

        # get the rect containing the surface (image)
        new_rect = self.image.get_rect()

        # correct displacement on the axis
        if self.side == 'north':
            new_rect.center = (self.x + self.displacement, self.y - vertical_offset)
        elif self.side == 'west':
            new_rect.center = (self.x - vertical_offset, self.y - self.displacement)
        elif self.side == 'south':
            new_rect.center = (self.x - self.displacement, self.y + vertical_offset)
        elif self.side == 'east':
            new_rect.center = (self.x + vertical_offset, self.y + self.displacement)

        return new_rect

    def _correctionStatus(self):
        # correct angle if door has open status

        if self.status == 'open':
            image = self._transformation_image(self.image_door)
            if self.side == "north":
                center_image = pg.math.Vector2(self.rect.center[0] -self.width / 2, self.rect.center[1])
                offset = pg.math.Vector2(self.width/2, 0)
            if self.side == 'west':
                center_image = pg.math.Vector2(self.rect.center[0], self.rect.center[1] + self.width/2)
                offset = pg.math.Vector2(0, -self.width/2)
            if self.side == 'east':
                center_image = pg.math.Vector2(self.rect.center[0], self.rect.center[1] - self.width/2)
                offset = pg.math.Vector2(0, self.width/2)
            if self.side == 'south':
                center_image = pg.math.Vector2(self.rect.center[0] + self.width/2, self.rect.center[1])
                offset = pg.math.Vector2(-self.width/2, 0)

            self._rotate_pivot_anim(image, center_image, offset, self.angle_open)
            self.rel_angle = self.angle_open


    def open(self):  # try animations
        if self.status == 'open':
            return
        else:               # from close to open
            pg.mixer.Sound.play(self.sound_open)
            self.status = 'open'
            self.rel_angle = 0
            self.is_opening = True

    def close(self):
        if self.status == 'close':
            return
        else:               # from open to close
            pg.mixer.Sound.play(self.sound_close)
            self.status = 'close'
            self.rel_angle = self.angle_open  # initial angle when open
            self.is_closing = True

    def update(self):

        # set angle increment and use module of the angle
        increment = 5
        if self.rel_angle > 0:
            self.rel_angle = self.rel_angle % 360
        else:
            self.rel_angle = self.rel_angle % - 360

        # incremental step
        if (self.status == 'open' and self.is_opening):
            self.rel_angle -= increment
        elif (self.status == 'close' and self.is_closing):
            self.rel_angle += increment

        # animation update [Opening & Closing]
        if self.is_opening or self.is_closing:

            # compute the temp image and get rect with positions

            image_tmp = self.image_door.copy()

            image_tmp = self._transformation_image(image_tmp)
            self.rect = self._correctionPos()

            # perform anchor rotation
            if self.side == "north":
                center_image = pg.math.Vector2(self.rect.center[0] - self.width / 2, self.rect.center[1])
                offset = pg.math.Vector2(self.width / 2, 0)
            if self.side == 'west':
                center_image = pg.math.Vector2(self.rect.center[0], self.rect.center[1] + self.width / 2)
                offset = pg.math.Vector2(0, -self.width / 2)
            if self.side == 'east':
                center_image = pg.math.Vector2(self.rect.center[0], self.rect.center[1] - self.width / 2)
                offset = pg.math.Vector2(0, self.width / 2)
            if self.side == 'south':
                center_image = pg.math.Vector2(self.rect.center[0] + self.width / 2, self.rect.center[1])
                offset = pg.math.Vector2(-self.width / 2, 0)
            self._rotate_pivot_anim(image_tmp, center_image, offset, self.rel_angle)

            # check whether turn off opening
            if abs(self.rel_angle) == abs(self.angle_open):
                self.is_opening = False

            # check whether turn off closing
            if abs(self.rel_angle) == abs(self.angle_close):
                self.is_closing = False

        # display rect for debug
        if not(self.is_closing or self.is_opening):
            x_, y_, w_, h_ = self._get_gfx_shape()
            self.display_gfxRect(x_, y_, w_, h_)
        else:
            self.remove_gfxRect()

    def draw(self):
        if abs(self.rel_angle) == abs(self.angle_open):
            pg.draw.rect(surface= self.screen, color=(15, 255, 80), rect=self.rect_open)
        super().draw()

class Window(HouseElement):
    def __init__(self, name, screen, x, y, angle_side, displacement, side, is_left: bool, status, room, group):
        super().__init__(name, screen, group, x, y, width= 50, height= 80) # width = 60;height= 100

        self.status = status            # status(str) -> open || close
        self.side = side                # side(str) -> north || west || south || east
        self.angle_side = angle_side    # global angle (int) respect the world (screen) when windows are closed
        self.rel_angle = 0              # relative angle (int) from the creation reference frame
        self.angle_open = - 90     #135    # relative angle (int) that represent the open state
        self.angle_close = 0            # relative angle (int) that represent the close state

        self.shape = (self.width, 10)
        self.is_left = is_left          # boolean variable to indicate which window door is of the pair
        self.room = room

        # variable to handle animation
        self.is_opening = False
        self.is_closing = False

        if self.is_left:
            self.displacement = displacement - self.width / 2
        else:
            self.displacement = displacement + self.width / 2

        # load images
        self._load_images()

        # correct positions and get rect
        new_rect = self._correctionPos()
        self.rect = new_rect

        # compute reduced rect for white surface of opened window
        self.rect_open = self._get_reduced_rect()

        # correct angle based on status
        self._correctionStatus()

        # create debug rect
        x_, y_, w_, h_ = self._get_gfx_shape()
        self.display_gfxRect(x_, y_, w_, h_)

        # load sound effects
        self.sound_open = pg.mixer.Sound("static/sounds/window_open.mp3")
        self.sound_close = pg.mixer.Sound("static/sounds/window_close.mp3")
        
        global windows
        windows.append(self)

    def _transformation_image(self, image):
        # flip if right window, upscale/downscale, rotate

        if not(self.is_left):
            image = pg.transform.flip(image, True, False)
        image = pg.transform.smoothscale(image, (self.width, self.height))
        image = pg.transform.rotate(image, self.angle_side)
        return image

    def _get_reduced_rect(self):
        """
        :return: reduced rect from the transparent asset of the door, used to show when it's open
        """
        init_rect = self.rect.copy()
        if self.side == 'north' or self.side == 'south':
            init_rect.y = self.rect.center[1] - 5
            init_rect.height = 10
            init_rect.width += 6
        elif self.side == 'west' or self.side == 'east':
            init_rect.width = 10
            init_rect.x = self.rect.center[1] - 5
            init_rect.height += 6

        init_rect.center = self.rect.center
        return init_rect

    def _get_gfx_shape(self):
        if self.side in ["north", "south"]:
            width = self.rect.width
            height = 1/5 * self.rect.height
            if self.status == "open":
                width = math.ceil(width * 3/5)

        elif self.side in ["east", "west"]:
            width = 1/5 * self.rect.width
            height = self.rect.height
            if self.status == "open":
                height = math.ceil(height * 3/5)

        if self.status == "open":
            tmp = width
            width = height
            height = tmp

        x = self.rect.topleft[0] + math.ceil((self.rect.width - width) / 2)
        y = self.rect.topleft[1] + math.ceil((self.rect.height - height) / 2)

        return x, y, width, height

    def _load_images(self):
        # load both images (no transformations)
        self.image_open = pg.image.load("static/assets/window_open.png").convert_alpha()
        self.image_close = pg.image.load("static/assets/window-closed.png").convert_alpha()

        # load actual image based on status
        if self.status == 'open':
            self.image = pg.image.load("static/assets/window_open.png").convert_alpha()
        elif self.status == 'close':
            self.image = pg.image.load("static/assets/window-closed.png").convert_alpha()
        else:
            raise ValueError("Wrong window status has been assigned")

        self.image = self._transformation_image(self.image)

        self.starting_image = self.image.copy()  # check if needed


    def _correctionPos(self, vertical_offset=5):

        # get the rect containing the surface (image)
        new_rect = self.image.get_rect()

        # correct displacement on the axis
        if self.side == 'north':
            new_rect.center = (self.x + self.displacement, self.y - vertical_offset)
        elif self.side == 'west':
            new_rect.center = (self.x - vertical_offset, self.y - self.displacement)
        elif self.side == 'south':
            new_rect.center = (self.x - self.displacement, self.y + vertical_offset)
        elif self.side == 'east':
            new_rect.center = (self.x + vertical_offset, self.y + self.displacement)

        return new_rect


    def _correctionStatus(self):

        # correct angle if window has open status
        if self.status == 'open':
            image = self._transformation_image(self.image_open)

            if self.is_left:   # left window
                if self.side == "north":
                    center_image = pg.math.Vector2(self.rect.center[0] - self.width / 2, self.rect.center[1])
                    offset = pg.math.Vector2(self.width/2, 0)
                if self.side == 'west':
                    center_image = pg.math.Vector2(self.rect.center[0], self.rect.center[1] + self.width/2)
                    offset = pg.math.Vector2(0, -self.width/2)
                if self.side == 'east':
                    center_image = pg.math.Vector2(self.rect.center[0], self.rect.center[1] - self.width/2)
                    offset = pg.math.Vector2(0, self.width/2)
                if self.side == 'south':
                    center_image = pg.math.Vector2(self.rect.center[0] + self.width/2, self.rect.center[1])
                    offset = pg.math.Vector2(-self.width/2, 0)

                self._rotate_pivot_anim(image, center_image, offset, self.angle_open)
                self.rel_angle = self.angle_open

            else:              # right window
                if self.side == "north":
                    center_image = pg.math.Vector2(self.rect.center[0] + self.width / 2, self.rect.center[1])
                    offset = pg.math.Vector2(-self.width/2, 0)
                if self.side == 'west':
                    center_image = pg.math.Vector2(self.rect.center[0], self.rect.center[1] - self.width/2)
                    offset = pg.math.Vector2(0, self.width/2)
                if self.side == 'east':
                    center_image = pg.math.Vector2(self.rect.center[0], self.rect.center[1] + self.width/2)
                    offset = pg.math.Vector2(0, -self.width/2)
                if self.side == 'south':
                    center_image = pg.math.Vector2(self.rect.center[0] - self.width/2, self.rect.center[1])
                    offset = pg.math.Vector2(self.width/2, 0)

                self._rotate_pivot_anim(image, center_image, offset, - self.angle_open)
                self.rel_angle = - self.angle_open


    def open(self):
        if self.status == 'open':   # nothing to do
            return
        else:                       # from close to open
            pg.mixer.Sound.play(self.sound_open)
            self.status = 'open'
            self.rel_angle = 0
            self.is_opening = True

    def close(self):
        if self.status == 'close':   # nothing to do
            return
        else:                       # from open to close
            pg.mixer.Sound.play(self.sound_close)
            self.status = 'close'
            if self.is_left:    # ccw
                self.rel_angle = self.angle_open   # initial angle when open
            else:               # cw
                self.rel_angle = - self.angle_open
            self.is_closing = True

    def update(self):

        # set angle increment and use module of the angle
        increment = 5
        if self.rel_angle > 0: self.rel_angle = self.rel_angle % 360
        else: self.rel_angle = self.rel_angle % - 360

        # incremental step
        if (self.status == 'open' and self.is_opening):
            if self.is_left:
                self.rel_angle -= increment
            else:
                self.rel_angle += increment
        if (self.status == 'close' and self.is_closing):
            if self.is_left:
                self.rel_angle += increment
            else:
                self.rel_angle -= increment

        # animation update [Opening & Closing]
        if self.is_opening or self.is_closing:

            # compute the temp image and get rect with positions
            if self.is_opening: image_tmp = self.image_open.copy()
            elif self.is_closing: image_tmp = self.image_close.copy()
            image_tmp = self._transformation_image(image_tmp)
            self.rect = self._correctionPos()

            # perform anchor rotation
            if self.is_left:

                # north, west, south, east
                if self.side == "north":
                    center_image = pg.math.Vector2(self.rect.center[0] - self.width / 2, self.rect.center[1])
                    offset = pg.math.Vector2(self.width/2, 0)
                if self.side == 'west':
                    center_image = pg.math.Vector2(self.rect.center[0], self.rect.center[1] + self.width/2)
                    offset = pg.math.Vector2(0, -self.width/2)
                if self.side == 'east':
                    center_image = pg.math.Vector2(self.rect.center[0], self.rect.center[1] - self.width/2)
                    offset = pg.math.Vector2(0, self.width/2)
                if self.side == 'south':
                    center_image = pg.math.Vector2(self.rect.center[0] + self.width/2, self.rect.center[1])
                    offset = pg.math.Vector2(-self.width/2, 0)
            else:
                if self.side == "north":
                    center_image = pg.math.Vector2(self.rect.center[0] + self.width / 2, self.rect.center[1])
                    offset = pg.math.Vector2(-self.width/2, 0)
                if self.side == 'west':
                    center_image = pg.math.Vector2(self.rect.center[0], self.rect.center[1] - self.width/2)
                    offset = pg.math.Vector2(0, self.width/2)
                if self.side == 'east':
                    center_image = pg.math.Vector2(self.rect.center[0], self.rect.center[1] + self.width/2)
                    offset = pg.math.Vector2(0, -self.width/2)
                if self.side == 'south':
                    center_image = pg.math.Vector2(self.rect.center[0] - self.width/2, self.rect.center[1])
                    offset = pg.math.Vector2(self.width/2, 0)

            self._rotate_pivot_anim(image_tmp, center_image, offset, self.rel_angle)

            # check whether turn off opening
            if abs(self.rel_angle) == abs(self.angle_open):
                self.is_opening = False

            # check whether turn off closing
            if abs(self.rel_angle) == abs(self.angle_close):
                self.is_closing = False

        # display rect for debug (hit box like)
        if not (self.is_closing or self.is_opening):
            x_, y_, w_, h_ = self._get_gfx_shape()
            self.display_gfxRect(x_, y_, w_, h_)
        else:
            self.remove_gfxRect()

    def draw(self):
        if abs(self.rel_angle) == abs(self.angle_open):
            pg.draw.rect(surface= self.screen, color=(255, 255, 51), rect=self.rect_open)
        super().draw()

class Furniture(HouseElement):
    def __init__(self, name, screen, group, type_furniture, x, y, width, height, rotation, room, flip_x = False, flip_y = False):
        super().__init__(name, screen, group, x, y, width, height)
        self.type_furniture = type_furniture
        self.rotation = rotation
        self.room = room
        self.flip_x = flip_x
        self.flip_y = flip_y
        self.is_movable = assets_furniture[self.type_furniture]["is_movable"]  # if is movable can be considered an object not mobilia
        self.asset_width = assets_furniture[self.type_furniture]["w"]
        self.asset_height = assets_furniture[self.type_furniture]["h"]
        self.name_asset = assets_furniture[self.type_furniture]["path"].split("/")[-1].replace(".png", "")
        self._load_image()
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        x_, y_, w_, h_ = self._get_gfx_shape()
        self.display_gfxRect(x_, y_, w_, h_)
        self.is_on = []
        self.has_on = []
        self._compute_bottom_furniture()
        
        global furniture
        furniture.append(self)


    def _transformation_image(self, image):
        # upscale/downscale, rotate
        image = pg.transform.smoothscale(image, (self.width, self.height))
        image = pg.transform.rotate(image, self.rotation)
        if self.flip_x or self.flip_y:
            image = pg.transform.flip(image, self.flip_x, self.flip_y)
        self.image = image

    def _compute_bottom_furniture(self):
        for k,v in  self.room.furniture.items():
            rect = v.rect_gfx.rect
            if (self.x >= rect.left and self.x <= rect.right) and\
                (self.y>= rect.top and self.y<= rect.bottom):
                    self.is_on.append(v)  # add to object
                    v.has_on.append(self)
                    # print(f"{self.name} self.is_on" , self.is_on)
                    # print(f"{v.name}    v.has_on"   , v.has_on)
                    # print(f"{self.name} self.has_on", self.has_on)

    def _get_gfx_shape(self):
        if not(self.name_asset in ["kitchen","studio_table"]):

            if abs(self.rotation) == 0 or abs(self.rotation) == 180:
                width = (self.asset_width/500) * self.rect.width
                height = (self.asset_height/500) * self.rect.height
            elif abs(self.rotation) == 90 or abs(self.rotation) == 270:
                width = (self.asset_height/500) * self.rect.width
                height = (self.asset_width/500) * self.rect.height

            x = self.rect.topleft[0] + math.ceil((self.rect.width - width)/2)
            y = self.rect.topleft[1] + math.ceil((self.rect.height - height)/2)

            return x, y, width, height
        else:
            return None, None, None, None


    def _load_image(self):
        self.image_asset = pg.image.load(assets_furniture[self.type_furniture]["path"]).convert_alpha()
        self.image = self.image_asset.copy()
        self._transformation_image(self.image)

class Pepper(HouseElement):
    def __init__(self, screen, group, room, displ_x, displ_y, output_box):
        super().__init__('Pepper', screen, group, room.x + displ_x, room.y + displ_y, width = 20, height= 20)
        self.rel_angle = 0
        self.actual_room = room
        self.grabbed_object = None
        self.color = (255, 255, 255)
        self.p_letter = Text("P", self.screen, self.x, self.y, color=(0, 0, 0), size_font= 21)
        self.p_original_letter = Text("P", self.screen, self.x, self.y, color=(0, 0, 0), size_font= 19)  #size_font
        self.output_box = output_box

        # homing data
        self.homing_room_name = 'Studio'
        self.homing_room_position = (room.x, room.y)

        # adding to the environment group
        self.group.add(self)
        self.group.add(self.p_letter)

        # pepper socket for communication with simulator
        self.socket: PepperMotion = PepperMotion(self)

        print(f"Pepper is in the {self.actual_room.name}")


        # flags vfx
        self.show_clearance = False
        self.show_target    = False
        self.show_direction = False
        self.show_forces    = False

        # flags motion
        self.changed_position       = False             # to update clearance and logo
        self.changed_orientation    = False
        self.in_motion              = False             # to handle start and end of a motion, is used in the rendering to call pepper.move()
        self.use_apf                = True

        # motion variables
        self.m2pixels = lambda x: x * 100       # Each 100 pixels represent 1 meter
        self.orientation = 90
        self.orientation_increment = 0
        self.toRoom = None
        self.clearance = None
        self.target = None
        self.target_orientation = None
        self.target_name  = None
        self.range = None
        self.bearing = None
        self.direction = None
        self.direction_norm = None
        self.motion_time_interval = None
        self.profile  = 'conical'                 # choose btw: "conical", "paraboloidal", "mixed"
        #  from m/s to pixel/s (compute pixel speed)

        # motion constants
        self.SPEED = 0.2 / 10             # [m/(s/10] 1/10 of seconds in time interval for the update time]
        self.MAX_SPEED = 0.5            # [m/s] approximated max speed from PEPPER-Technical Specifications
        self.POS_TOLERANCE = 1
        self.P_SPEED = self.m2pixels(self.SPEED)  # 2 [pixel/second]

        # plan execution thread
        self.listener_thread = None
        self.plan = None
        
        # instantiation messages
        self.output_box.add_message(f"Pepper is in the {self.actual_room.name}")
        self.output_box.add_message(f"Pepper APF profile: {self.profile}")

    # change position methods
    def set_Xpos(self, x = None):
        if x is not None:
            self.x = x
            old_logo_center = self.logo.rect.center
            self.logo.rect.center = (x, old_logo_center[1])
            
    def set_Ypos(self, y = None):
        if y is not None:
            self.y = y
            old_logo_center = self.logo.rect.center
            self.logo.rect.center = (old_logo_center[0], y)
        
    def set_random_position(self):
        margin_from_wall = 20
        rand_increment = self.socket.random_position(self.actual_room.width, self.actual_room.height, margin_from_wall)
        rand_pos_x = self.actual_room.rect.topleft[0] +  rand_increment[0]
        rand_pos_y = self.actual_room.rect.topleft[1] + rand_increment[1]
        print(f"Random position: {(rand_pos_x,rand_pos_y)}")
        self.x = rand_pos_x
        self.y = rand_pos_y
        self.changed_position = True

        # check if the position lies on obstacles, in that case, recompute
        for k, window in self.actual_room.windows.items():
            if not(window[0].rect_gfx is None):     # left window
                if self.socket.in_rect(window[0].rect_gfx.rect, pg.math.Vector2(self.x, self.y)):
                    self.set_random_position()
                    return
            if not(window[1].rect_gfx is None):     # right window
                if self.socket.in_rect(window[1].rect_gfx.rect, pg.math.Vector2(self.x, self.y)):
                    self.set_random_position()
                    return

        for k, door in self.actual_room.doors.items():
            if not(door.rect_gfx is None):
                if self.socket.in_rect(door.rect_gfx.rect, pg.math.Vector2(self.x, self.y)):
                    self.set_random_position()
                    return

        for k, furniture in self.actual_room.furniture.items():
            if not(furniture.rect_gfx is None):
                if self.socket.in_rect(furniture.rect_gfx.rect, pg.math.Vector2(self.x, self.y)):
                    self.set_random_position()
                    return
        return

    def set_random_room(self):
        rooms = get_rooms()
        random_room = rooms[randint(0, len(rooms)-1)]
        self.actual_room = random_room
        self.x = random_room.rect.center[0]
        self.y = random_room.rect.center[1]
        self.changed_position = True

    def set_random_room_position(self):
        self.set_random_room()
        self.set_random_position()

    def get_position(self):
        return pg.math.Vector2(self.x, self.y)

    # motion methods
    def compute_clearance(self):
        self.clearance, _ = self.socket.compute_clearance()

    def rotate2target(self):
        from_pos = pg.math.Vector2(self.x, self.y)
        # print("rotate 2 target", self.target,(self.x, self.y))
        
        self.changed_orientation =  True
        # Calculate the vector between the two points
        vector =  self.target - from_pos 
        
        # Calculate the angle of rotation in radians
        angle_rad = math.atan2(vector.y, vector.x)

        # Convert the angle to degrees
        angle_deg = int(math.degrees(angle_rad))
        
        self.target_orientation = angle_deg
        
        if self.target_orientation<0:
            self.target_orientation = self.target_orientation + 360
            
        # print(self.target_orientation)
        # print(self.orientation)

    def move2pos(self, target: pg.math.Vector2, motion_time_interval = 100):
        self.target = target
        self.target_name = f"Position: x = {int(target.x)}, y = {int(target.y)}"

        self.rotate2target()

        if not self.use_apf : # linear motion
            # compute direction and the normalized direction vector
            direction: pg.math.Vector2 = target - pg.math.Vector2(self.x, self.y)
            self.direction = direction
            try:
                self.direction_norm = pg.math.Vector2.normalize(self.direction)
            except:
                self.direction_norm = pg.math.Vector2(0,0)
        else:
            # compute the total force using APF methods
            f_t = self.socket.apf(self.target,self.P_SPEED, profile=self.profile)

            print(f_t)
            # we use this force as a generalized velocity
            self.direction = f_t
            try:
                self.direction_norm = pg.math.Vector2.normalize(self.direction)
            except:
                self.direction_norm = pg.math.Vector2(0,0)

        # set flags on
        if not(self.in_motion): self.in_motion = True

        print(f'started the motion: {time.strftime("%H:%M:%S")}')
        print(f'target: {self.target}')

    # it's important to update the current room for pepper, otherwise the APF doesn't work properly
    def move2Room(self, room_name: str, direction: str, motion_time_interval = 100):
        
        #displacement = 60
        displacement = 40
        # compute the target based on the direction
        if "west" in direction.strip().lower():
            target = pg.math.Vector2(self.x - displacement, self.y)
        elif "east" in direction.strip().lower():
            target = pg.math.Vector2(self.x + displacement, self.y)
        elif "south" in direction.strip().lower():
            target = pg.math.Vector2(self.x, self.y + displacement)
        elif "north" in direction.strip().lower():
            target = pg.math.Vector2(self.x, self.y - displacement)
            

        self.target = target
        self.target_name = f"room {room_name}"

        self.rotate2target()

        if not self.use_apf : # linear motion
            # compute direction and the normalized direction vector
            direction: pg.math.Vector2 = target - pg.math.Vector2(self.x, self.y)
            self.direction = direction
            try:
                self.direction_norm = pg.math.Vector2.normalize(self.direction)
            except:
                self.direction_norm = pg.math.Vector2(0,0)
        else:
            # compute the total force using APF methods
            f_t = self.socket.apf(self.target,self.P_SPEED, profile=self.profile)

            print(f_t)
            # we use this force as a generalized velocity
            self.direction = f_t
            try:
                self.direction_norm = pg.math.Vector2.normalize(self.direction)
            except:
                self.direction_norm = pg.math.Vector2(0,0)

        # set flags on
        if not(self.in_motion): self.in_motion = True


        r = get_rooms()
        elem = None
        for e in r:
            if e.name == room_name:
                elem = e
        self.toRoom = elem
        
        print(f'started the motion: {time.strftime("%H:%M:%S")}')
        print(f'target: {self.target}')
    
    def move2Furniture(self, target_name: str, motion_time_interval = 100):
        
        target = reach_positions[target_name]
        self.target = target
        self.target_name = f" furniture {target_name}"

        self.rotate2target()

        if not self.use_apf : # linear motion
            # compute direction and the normalized direction vector
            direction: pg.math.Vector2 = target - pg.math.Vector2(self.x, self.y)
            self.direction = direction
            try:
                self.direction_norm = pg.math.Vector2.normalize(self.direction)
            except:
                self.direction_norm = pg.math.Vector2(0,0)
        else:
            # compute the total force using APF methods
            f_t = self.socket.apf(self.target,self.P_SPEED, profile=self.profile)

            print(f_t)
            # we use this force as a generalized velocity
            self.direction = f_t
            try:
                self.direction_norm = pg.math.Vector2.normalize(self.direction)
            except:
                self.direction_norm = pg.math.Vector2(0,0)

        # set flags on
        if not(self.in_motion): self.in_motion = True

        print(f'started the motion: {time.strftime("%H:%M:%S")}')
        print(f'target: {self.target}')

    def move2FreeSpace(self, room_name = None, motion_time_interval = 100):
        
        if room_name is None: room_name = self.actual_room.name
        
        target = free_space_positions[room_name]
        self.target = target
        self.target_name = f" free space {room_name}"

        self.rotate2target()

        if not self.use_apf : # linear motion
            # compute direction and the normalized direction vector
            direction: pg.math.Vector2 = target - pg.math.Vector2(self.x, self.y)
            self.direction = direction
            try:
                self.direction_norm = pg.math.Vector2.normalize(self.direction)
            except:
                self.direction_norm = pg.math.Vector2(0,0)
        else:
            # compute the total force using APF methods
            f_t = self.socket.apf(self.target,self.P_SPEED, profile=self.profile)

            print(f_t)
            # we use this force as a generalized velocity
            self.direction = f_t
            try:
                self.direction_norm = pg.math.Vector2.normalize(self.direction)
            except:
                self.direction_norm = pg.math.Vector2(0,0)

        # set flags on
        if not(self.in_motion): self.in_motion = True

        print(f'started the motion: {time.strftime("%H:%M:%S")}')
        print(f'target: {self.target}')

    def move2Door(self, name, distance_wall = 30, motion_time_interval= 100):

        # set the time interval
        self.motion_time_interval = motion_time_interval
        self.target_name = f" door {name}"

        
        door = None
        doors = get_doors()
        for elem in doors:
            if elem.name == name:
                door = elem
                
        if door is None:
            print(f"No door of the name {name} has been found")
            return

        side = door.side.lower()
        
        # compute the sign multiplier for the distance
        # sign_x = 1
        # sign_y = 1
        # if self.actual_room.x < door.x:
        #     sign_x *= -1
        # if self.actual_room.y > door.y:
        #     sign_y *= -1
        
        # if door.status == 'open':
        # self.target = pg.math.Vector2(door.rect_open.center)
        # else:
        #     self.target = pg.math.Vector2(door.rect.center)

        # if side == "north":
        if self.actual_room.x < door.x and (side == "east" or side == "west"):
            self.target = pg.math.Vector2(door.rect_open.center[0] - distance_wall, door.rect_open.center[1])
        # elif side == "south":
        elif self.actual_room.x > door.x and (side == "east" or side == "west"):
            self.target = pg.math.Vector2(door.rect_open.center[0] + distance_wall, door.rect_open.center[1])
        # elif side == "east":
        elif self.actual_room.y < door.y and (side == "north" or side == "south"):
            self.target = pg.math.Vector2(door.rect_open.center[0], door.rect_open.center[1] - distance_wall)
        # elif side == "west":
        elif self.actual_room.y > door.y and (side == "north" or side == "south"):
            self.target = pg.math.Vector2(door.rect_open.center[0], door.rect_open.center[1] + distance_wall)

        # apf method
        # compute the total force using APF methods
        f_t = self.socket.apf(self.target, self.P_SPEED, profile=self.profile)
        print(f_t)
        self.direction = f_t
        try:
            self.direction_norm = pg.math.Vector2.normalize(self.direction)
        except:
            self.direction_norm = pg.math.Vector2(0, 0)

        # set flags on
        if not(self.in_motion): self.in_motion = True
        self.rotate2target()
        
        print(f'started the motion: {time.strftime("%H:%M:%S")}')
        print(f'target: {self.target}')

    def move2Win(self, name, distance_wall = 30, motion_time_interval=100):
        """
        :param side: cardinal coordinates for the window target
        :param window_part: "whole","left" or "right" to select the correct target
        :param motion_time_interval: motion time interval: default 100 [ms]
        :return: None
        """

        # set the time interval
        self.motion_time_interval = motion_time_interval
        self.target_name = f" window {name}"

        window = None
        windows = get_windows()
        for elem in windows:
            if elem.name == name:
                window = elem
                
        if window is None:
            print(f"No door of the name {name} has been found")
            return

        side = window.side
        
        rect_c = window.rect_open.center
        
        if side == "north" or side == "south":
            self.target = pg.math.Vector2(rect_c[0], rect_c[1] +distance_wall)
        elif side == "south":
            self.target = pg.math.Vector2(rect_c[0], rect_c[1] - distance_wall)
        elif side == "east":
            self.target = pg.math.Vector2(rect_c[0] - distance_wall, rect_c[1])
        elif side == "west":
            self.target = pg.math.Vector2(rect_c[0] + distance_wall, rect_c[1])


        # --------- old version that include positioning to left win, right win or in the middle of them

        # if window_part == 'left':
        #     rect_c = window[0].rect_open.center

        #     if side == "north" or side == "south":
        #         self.target = pg.math.Vector2(rect_c[0], rect_c[1] +distance_wall)
        #     elif side == "south":
        #         self.target = pg.math.Vector2(rect_c[0], rect_c[1] - distance_wall)
        #     elif side == "east":
        #         self.target = pg.math.Vector2(rect_c[0] - distance_wall, rect_c[1])
        #     elif side == "west":
        #         self.target = pg.math.Vector2(rect_c[0] + distance_wall, rect_c[1])


        # elif window_part == 'right':
        #     rect_c = window[1].rect_open.center

        #     if side == "north" or side == "south":
        #         self.target = pg.math.Vector2(rect_c[0], rect_c[1] +distance_wall)
        #     elif side == "south":
        #         self.target = pg.math.Vector2(rect_c[0], rect_c[1] - distance_wall)
        #     elif side == "east":
        #         self.target = pg.math.Vector2(rect_c[0] - distance_wall, rect_c[1])
        #     elif side == "west":
        #         self.target = pg.math.Vector2(rect_c[0] + distance_wall, rect_c[1])

        # elif window_part == "whole":
        #     if side == "north" or side == "south":
        #         self.target = pg.math.Vector2((window[0].rect_open.center[0] + window[1].rect_open.center[0])/2, (window[0].rect_open.center[1]) - distance_wall)
        #     elif side == "east" or side == "west":
        #         self.target = pg.math.Vector2((window[0].rect_open.center[0]) - distance_wall,(window[0].rect_open.center[1] + window[1].rect_open.center[1])/2)

        # apf method

        # compute the total force using APF methods
        f_t = self.socket.apf(self.target, self.P_SPEED, profile=self.profile)
        self.direction = f_t
        try:
            self.direction_norm = pg.math.Vector2.normalize(self.direction)
        except:
            self.direction_norm = pg.math.Vector2(0, 0)

        # set flags on
        if not(self.in_motion): self.in_motion = True
        self.rotate2target()
        
        print(f'started the motion: {time.strftime("%H:%M:%S")}')
        print(f'target: {self.target}')

    def reset_motion_variables(self):
        self.in_motion = False
        self.target = None
        self.target_orientation = None
        self.orientation_increment = 0
        self.target_name = None
        self.clearance = None
        self.direction = None
        self.direction_norm = None

    def toggle_inMotion(self):
        if self.in_motion: self.in_motion = False
        else: self.in_motion = True

    def move(self, verbose = False):
        
        if self.direction is None:
            return
        
        # do motion
        if self.use_apf:
            self.x += self.direction.x  # in this case direction contains the generalized velocity
            self.y += self.direction.y
        else:
            self.x += self.P_SPEED * self.direction_norm.x  # x0 + vx [p/s] * 1 [s]
            self.y += self.P_SPEED * self.direction_norm.y  # y0 + vy [p/s] * 1 [s]

        self.socket.last_positions.append(pg.math.Vector2(self.x, self.y))
        if len(self.socket.last_positions) > 10:
            self.socket.last_positions.pop(0)

        if verbose: print(f"New position {(self.get_position())}")
        distance = (self.get_position() - self.target).length()
        if verbose: print(f"Distance {distance}")

        # print(distance)
        if distance < self.POS_TOLERANCE:   # motion complete
            self.output_box.add_message(f"Pepper has reached {self.target_name}")
            print(f'completed the motion: {time.strftime("%H:%M:%S")}')
            self.reset_motion_variables()
            self.socket.reset_motion_variables()

        else:
            # if apf compute the new direction for the next step
            if self.use_apf:
                # compute the total force using APF methods
                f_t = self.socket.apf(self.target, self.P_SPEED, profile=self.profile)
                # we use this force as a generalized velocity
                self.direction = f_t
                try:
                    self.direction_norm = pg.math.Vector2.normalize(self.direction)
                except:
                    self.direction_norm = pg.math.Vector2(0, 0)

        self.changed_position = True

    def update(self, width_logo=60, height_logo=60):
        # update logo
        if self.changed_position:
            # update the logo
            self.logo.rect.x = self.x - width_logo/2
            self.logo.rect.y = self.y - height_logo/2

        if self.changed_orientation:
            try:
                orientation = self.orientation % 360
                target = self.target_orientation % 360

                    # Calculate the absolute difference between the angles
                diff = target-orientation
                
                if diff >= 0: sign = 1
                else: sign = -1

                # Choose the smaller orientation gap
                if abs(diff) > 360 - abs(diff):
                    sign = sign*-1

                orientation_gap = min(abs(diff), 360 - abs(diff))
                orientation_gap = orientation_gap * sign
                
                # diff = self.orientation - self.target_orientation
            except:
                self.changed_orientation = False
                return
            
            if orientation_gap == 0:
                # print("orientation reached")
                self.changed_orientation = False
                
            if orientation_gap > 0:
                # print(f"rotating ccw {self.orientation}")
                self.orientation_increment =  1
                self.orientation += 1
            else:
                # print(f"rotating cw {self.orientation}")
                self.orientation_increment = 1
                self.orientation -= 1
                
            self.orientation = self.orientation % 360
             
            
        # compute new clarance if pepper is moving
        if self.show_clearance:
            if (self.clearance is None) or self.changed_position:
                self.compute_clearance()

        # set to false the changed position (if in motion will be set to True again from move function)
        if self.changed_position: self.changed_position = False # restore default False value

        if not(self.toRoom is None) and not(self.in_motion):
            self.actual_room = self.toRoom
            self.toRoom = None
            
    # grab/place method                                                             
    def grab(self, name_object: str):
        
        furniture = get_furniture()
        item = None
        for elem in furniture:
            if elem.name.lower().strip() == name_object:
                item = elem
        
        
        if not(item.is_movable):
            print("Pepper cannot hold this object!")
        else:
            self.grabbed_object = item
            self.group.remove(item)
            print("Pepper has grabbed {}".format(item.name))
            self.output_box.add_message(f"Pepper has grabbed {self.grabbed_object.name}")
            
        self.in_motion = True
        timer = threading.Timer(1, lambda: self.toggle_inMotion())
        timer.start()
           
    def place(self, name_place:str):
        if self.grabbed_object is None:
            print("Pepper has not grabbed an object")
        else:
            # take and switch position in the list
            target = place_positions[name_place].pop(0)
            print(target)
            if place_positions[name_place] == []:
                place_positions[name_place] = [target]
                
            place_positions[name_place][-1] = target
            
            self.grabbed_object.rect.center = (target.x, target.y)
            print("Pepper is placing {}".format(self.grabbed_object.name))
            self.output_box.add_message(f"Pepper has placed {self.grabbed_object.name}")
            self.group.add(self.grabbed_object)
            self.group.remove(self)
            self.group.remove(self.p_letter)

            self.group.add(self)
            self.group.add(self.p_letter)

        self.in_motion = True
        timer = threading.Timer(1, lambda: self.toggle_inMotion())
        timer.start()

                                                                # open/close method
                                                                
    def openDoor(self, door_name):   # door name of the type "d_$room1_$room2"
        found = False
        doors = get_doors()
        for door in doors:
            if door.name == door_name:
                door.open()
                found = True
        if not found:
            print(f"{door_name} is not present in the room where pepper is placed ({self.actual_room.name})")    
        
        self.in_motion = True
        timer = threading.Timer(1, lambda: self.toggle_inMotion())
        timer.start()
        
    def closeDoor(self, door_name):
        found = False
        doors = get_doors()
        for door in doors:
            if door.name == door_name:
                door.close()
                found = True
        if not found:
            print(f"{door_name} is not present in the room where pepper is placed ({self.actual_room.name})")      
        
        self.in_motion = True
        timer = threading.Timer(1, lambda: self.toggle_inMotion())
        timer.start()
        
    def openWin(self, win_name):    # window name of the type "wl_$room" or "wr_$room", respectively for left and right windows
        found = False
        windows = get_windows()
        for window in windows:
                if window.name == win_name:
                    window.open()
                    found = True
        if not found:
            print(f"{win_name} is not present in the room where pepper is placed ({self.actual_room.name})")    
        
        self.in_motion = True
        timer = threading.Timer(1, lambda: self.toggle_inMotion())
        timer.start()
         
    def closeWin(self, win_name):
        found = False
        windows = get_windows()
        for window in windows:
            if window.name == win_name:
                window.close()
                found = True
        if not found:
            print(f"{win_name} is not present in the room where pepper is placed ({self.actual_room.name})") 

        self.in_motion = True
        timer = threading.Timer(1, lambda: self.toggle_inMotion())
        timer.start()
    
    
    # plan execution
    
    def provide_plan(self, plan):
        if self.plan is None:
            self.plan = plan
            self.listener_thread = threading.Thread(target = self.exe_plan)
            self.listener_thread.daemon = True
            self.listener_thread.start()
        else:
            self.output_box.add_message(f"Pepper is busy cannot execute the task")
        
    def  _getType_elem(self, item):
        """
            simple function that returns the type of house element object to understand which kind of motion to accomplish
        """
        d = get_doors()
        for elem in d:
            if item in elem.name.strip().lower():
                return "door"
        
        w = get_windows()
        for elem in w:
            if item in elem.name.strip().lower():
                return "window"
                
        f = get_furniture()
        for elem in f:
            if item in elem.name.strip().lower():
                return "furniture"
            
        return None

        
    def exe_plan(self):
        
        while not (self.plan == []):
            if not(self.in_motion):
                step = self.plan.pop(0)
                if step['action'].strip().lower() == "move2":
                    room_name   =  step['arguments'][0].strip().lower()
                    # from_elem   =  step['arguments'][1].strip().lower()
                    to_elem     =  step['arguments'][2].strip().lower()
                    if "free_space" in to_elem:
                        self.move2FreeSpace()
                    else:
                        type_elem = self._getType_elem(to_elem)
                        
                        if type_elem == "door":
                            self.move2Door(name = to_elem)
                        elif type_elem == "window":
                            self.move2Win(name = to_elem)
                        elif type_elem == "furniture":
                            self.move2Furniture(target_name= to_elem)
                    
                    
                elif step['action'].strip().lower() == "move2room":
                    direction  = step['arguments'][3].strip().lower()
                    room_name = step['arguments'][1].strip().lower()
                    self.move2Room(room_name=room_name, direction=direction)
                    
                elif step['action'].strip().lower() == "open_door":
                    self.openDoor(step['arguments'][0].strip().lower())
                    
                elif step['action'].strip().lower() == "close_door":
                    self.closeDoor(step['arguments'][0].strip().lower())
                    
                elif step['action'].strip().lower() == "open_win":
                    self.openWin(step['arguments'][0].strip().lower())
                    
                elif step['action'].strip().lower() == "close_win":
                    self.closeWin(step['arguments'][0].strip().lower())
                    
                elif step['action'].strip().lower() == "grab_object":
                    self.grab(step['arguments'][0].strip().lower())
                    
                elif step['action'].strip().lower() == "place_object":
                    self.place(step['arguments'][2].strip().lower())
                
                else:
                    raise ValueError("action requested is not described by the PDDL domain file")
        
        
        self.output_box.add_message(f"Pepper has completed the task assigned")            
        self.plan = None
                     
    # graphic methods
    def set_color(self, color):
        self.color = color

    def get_logo(self, width=60, height=60):
        logo = StaticImage("static/assets/pepper.png", self.screen, self.x - width / 2, self.y - height / 2, width,
                           height)
        logo.rect.center = (self.x ,self.y)
        self.logo = logo
        return self.logo
    
    def draw(self, direction_normalized = True):

        # draw a circle to track the position of pepper
        pg.draw.circle(self.screen, color=(0, 0, 0), center=(self.x, self.y), radius=13)  # thick circle
        pg.draw.circle(self.screen, color=self.color, center=(self.x, self.y), radius=10)
        self.p_letter.center_to(self.x, self.y)
        
        
        # tmp code to find positions for reach_positions place_positions
        # f = get_furniture()
        # elem = None
        # for e in f:
        #     if e.name == "table_dining":
        #         elem = e
    
        # x = elem.x + 25
        # y = elem.y - 25
        
        # pg.draw.circle(self.screen, color=(0, 255, 0), center=(x,y), radius=5)
        # print(x,y)
        # r = get_rooms()
        # elem = None
        # for e in r:
        #     if e.name == "outdoor":
        #         elem = e
    
        # x = elem.x + 50
        # y = elem.y - 170
        
        # pg.draw.circle(self.screen, color=(0, 255, 0), center=(x,y), radius=5)
        # print(x,y)
        
        

        
        if (self.show_clearance and not(self.clearance is None)):
            pg.draw.circle(self.screen, color=(255, 0, 0), center=(self.clearance.x, self.clearance.y), radius=5)

        if (self.show_target and not(self.target is None)):
            pg.draw.circle(self.screen, (0, 130, 0), (self.target.x, self.target.y), radius=5)

        if (self.show_forces and not(self.socket.last_apf == {})):
            arc_angle_points = 12  # angle to compute points for the arrow

            if ((self.socket.last_apf['f_a'] != None) and \
                    ((self.socket.last_apf['f_a'].x != 0) or (self.socket.last_apf['f_a'].y != 0))):

                # attractive force
                pg.draw.line(self.screen, (0, 0, 255), (self.x, self.y),
                             (self.x + (self.socket.last_apf['f_a'].x * 25), self.y + (self.socket.last_apf['f_a'].y * 25)), width=3)

                direction_offset_1 = self.socket.last_apf['f_a'].rotate(-int(arc_angle_points / 2))
                direction_offset_2 = self.socket.last_apf['f_a'].rotate(int(arc_angle_points / 2))

                point_offset_1 = pg.math.Vector2((self.x + (direction_offset_1.x * 20)),
                                                 (self.y + (direction_offset_1.y * 20)))
                point_offset_2 = pg.math.Vector2((self.x + (direction_offset_2.x * 20)),
                                                 (self.y + (direction_offset_2.y * 20)))
                point_target = pg.math.Vector2((self.x + (self.socket.last_apf['f_a'].x * 25)),
                                               (self.y + (self.socket.last_apf['f_a'].y * 25)))

                points = [point_offset_1, point_offset_2, point_target]
                pg.draw.polygon(self.screen, (0, 0, 255), points, width=0)

            # repulsive force
            if ((self.socket.last_apf['f_r'] != None) and \
                    ((self.socket.last_apf['f_r'].x != 0) or (self.socket.last_apf['f_r'].y != 0))):
                pg.draw.line(self.screen, (255, 0, 0), (self.x, self.y),
                             (self.x + (self.socket.last_apf['f_r'].x * 25), self.y + (self.socket.last_apf['f_r'].y * 25)), width=3)

                direction_offset_1 = self.socket.last_apf['f_r'].rotate(-int(arc_angle_points / 2))
                direction_offset_2 = self.socket.last_apf['f_r'].rotate(int(arc_angle_points / 2))

                point_offset_1 = pg.math.Vector2((self.x + (direction_offset_1.x * 20)),
                                                 (self.y + (direction_offset_1.y * 20)))
                point_offset_2 = pg.math.Vector2((self.x + (direction_offset_2.x * 20)),
                                                 (self.y + (direction_offset_2.y * 20)))
                point_target = pg.math.Vector2((self.x + (self.socket.last_apf['f_r'].x * 25)),
                                               (self.y + (self.socket.last_apf['f_r'].y * 25)))

                points = [point_offset_1, point_offset_2, point_target]
                pg.draw.polygon(self.screen, (255, 0, 0), points, width=0)

            # vortex field force
            if ((self.socket.last_apf['f_v'] != None) and \
                    ((self.socket.last_apf['f_v'].x != 0) or (self.socket.last_apf['f_v'].y != 0))):
                pg.draw.line(self.screen, (0, 255, 255), (self.x, self.y),
                             (self.x + (self.socket.last_apf['f_v'].x * 25), self.y + (self.socket.last_apf['f_v'].y * 25)), width=3)

                direction_offset_1 = self.socket.last_apf['f_v'].rotate(-int(arc_angle_points / 2))
                direction_offset_2 = self.socket.last_apf['f_v'].rotate(int(arc_angle_points / 2))

                point_offset_1 = pg.math.Vector2((self.x + (direction_offset_1.x * 20)),
                                                 (self.y + (direction_offset_1.y * 20)))
                point_offset_2 = pg.math.Vector2((self.x + (direction_offset_2.x * 20)),
                                                 (self.y + (direction_offset_2.y * 20)))
                point_target = pg.math.Vector2((self.x + (self.socket.last_apf['f_v'].x * 25)),
                                               (self.y + (self.socket.last_apf['f_v'].y * 25)))

                points = [point_offset_1, point_offset_2, point_target]
                pg.draw.polygon(self.screen, (0, 255, 255), points, width=0)


        # show total force
        if (self.show_direction and not(self.direction is None) and not(self.show_forces)): # priority to show forces
            if direction_normalized:
                # draw the arrow: the line
                pg.draw.line(self.screen, (0, 255, 0), (self.x, self.y), (self.x + (self.direction_norm.x * 50), self.y + (self.direction_norm.y * 50)), width = 3)

                # draw the arrow: the triangle
                arc_angle_points = 12  # degrees
                direction_offset_1 = self.direction_norm.rotate(-int(arc_angle_points/2))
                direction_offset_2 = self.direction_norm.rotate( int(arc_angle_points/2))

                point_offset_1 = pg.math.Vector2((self.x + (direction_offset_1.x * 40)), (self.y + (direction_offset_1.y * 40)))
                point_offset_2 = pg.math.Vector2((self.x + (direction_offset_2.x * 40)), (self.y + (direction_offset_2.y * 40)))
                point_target = pg.math.Vector2((self.x + (self.direction_norm.x * 50)), (self.y + (self.direction_norm.y * 50)))

                points =  [point_offset_1, point_offset_2, point_target]
                pg.draw.polygon(self.screen, (0, 255, 0), points, width=0)
            else:
                pg.draw.line(self.screen, (0, 255, 0), (self.x, self.y), (self.x + (self.direction.x * 50), self.y + (self.direction.y * 50)), width = 3)

                # draw the arrow: the triangle
                arc_angle_points = 12  # degrees
                direction_offset_1 = self.direction.rotate(-int(arc_angle_points/2))
                direction_offset_2 = self.direction.rotate( int(arc_angle_points/2))

                point_offset_1 = pg.math.Vector2((self.x + (direction_offset_1.x * 40)), (self.y + (direction_offset_1.y * 40)))
                point_offset_2 = pg.math.Vector2((self.x + (direction_offset_2.x * 40)), (self.y + (direction_offset_2.y * 40)))
                point_target = pg.math.Vector2((self.x + (self.direction.x * 50)), (self.y + (self.direction.y * 50)))

                points =  [point_offset_1, point_offset_2, point_target]
                pg.draw.polygon(self.screen, (0, 255, 0), points, width=0)
