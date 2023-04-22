import pygame
import pygame as pg
import math
from services import PepperSocket

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
    'parquet': 'static/floor_parquet.jpg',
    'grey': 'static/floor_grey_tiles.jpg',
    'white': 'static/floor_white.jpg',
    'marble': 'static/floor_marble.jpg',
    'black_marble': 'static/floor_black_marble.jpg',
    'ceramic': 'static/floor_ceramic.jpg',
    'parquet_strips': 'static/floor_parquet_strips.jpg',
    'rhombus': 'static/floor_rhombus.jpg',
    'test': 'static/floor_test.png'
}

furniture = {


}

rooms = []
def get_rooms():
    """
    :return: list containing all the rooms created
    """
    return rooms

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
            self.image = pg.image.load("static/green_bt.png").convert_alpha() # sprite for both on and off button
        elif type_button == 'off':
            self.image = pg.image.load("static/red_bt.png").convert_alpha()
        else:
            raise ValueError("Wrong button type has been assigned")

        self.image = pg.transform.smoothscale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.last_click = None
        self.type_DO = 'button'
        self.sound = pg.mixer.Sound("static/button_click.mp3")

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
            self.image = pg.image.load("static/red_bt.png").convert_alpha()
            self.image = pg.transform.smoothscale(self.image, (self.width, self.height))
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)
            self.status = 'off'
            self.update()

        elif self.status == 'off':
            print(f'button {self.name} goes to on')
            pg.mixer.Sound.play(self.sound)
            self.image = pg.image.load("static/green_bt.png").convert_alpha()
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
        self.rect = self.image.get_rect(center = self.rect.center)

    def _rotate_pivot_anim(self, image, pivot, offset,angle):
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

    def display_gfxRect(self):
        self.rect_gfx = Rect(self.screen, self.rect.topleft[0], self.rect.topleft[1], self.rect.width, self.rect.height, (255,0,0), alpha= 100)

    def remove_gfxRect(self):
        if self.rect_gfx: self.group.remove(self.rect_gfx)
        del self.rect_gfx
        self.rect_gfx = None

    def render_debug_vertices(self):
        vertices = self.get_vertices()
        pg.draw.circle(self.screen, (0,0, 255), (self.x, self.y), radius=15)
        for v in list(vertices.values()):
            pg.draw.circle(self.screen, (255,0,0), v, radius = 10)

    def render_debug_rect(self):
        try:
            self.rect_gfx.draw()
        except:
            raise ValueError("First instantiate the graphic rect of the display object!")

class Room(HouseElement):

    def __init__(self, name, screen, x, y, width, height, env_group, tile_type='test'):
        super().__init__(name, screen, env_group, x, y, width, height)
        self.max_w_tile = 100
        self.max_h_tile = 100
        self.image = pygame.Surface((width, height), pg.SRCALPHA)

        # full the surface with the image
        for i in range(math.ceil(self.width/self.max_w_tile)):
            for j in range(math.ceil(self.height/self.max_h_tile)):
                tmp_image = pg.image.load(tiles[tile_type]).convert_alpha()
                tmp_image = pg.transform.smoothscale(tmp_image, (self.max_w_tile, self.max_h_tile)).convert_alpha()
                self.image.blit(tmp_image, (i*self.max_w_tile, j*self.max_h_tile))

        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        # list of elements
        self.bounds      = {}
        self.windows    = {}
        self.doors      = {}
        self.furniture  = {}

        # add in the list of element for rendering
        self.group.add(self)

        # include the room in the global list
        global rooms
        rooms.append(self)

        self._create_boundaries()
        self.visible_boundaries = True

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
        Function used to change the shape of the room's boundaries when a door is inserted

        :param side: (str) cardinal direction: north, south, east, west
        :param start: (int) start position (x or y based on the side) of the door
        :param end: (int) end position (x or y based on the side) of the door
        :return: None
        """
        bounds = self.bounds[side]
        start_position = start; end_position = end

        # print("side", side)
        # print("start", start)
        # print("end", end)
        # print("bounds", bounds)

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
                    print("passed -------")
                    first_new_bound  = (pg.math.Vector2(bound[0][0], bound[0][1]),pg.math.Vector2(start_position,bound[0][1]))
                    second_new_bound = (pg.math.Vector2(end_position,bound[1][1]),pg.math.Vector2(bound[1][0],bound[1][1]))
                    to_insert = [first_new_bound,second_new_bound]
                    idx_delete = idx
                    break
             # [(pg.math.Vector2(vertices['left-top']), pg.math.Vector2(vertices['right-top']))]
        elif side == 'west' or side == 'east':     # check y
            for idx, bound in enumerate(bounds):
                if start_position > bound[0][1] and end_position < bound[1][1]:
                    print("passed -------")
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
    def add_door(self, other_room: HouseElement, status='close', is_main = False):
        """
        function that insert doors in the room. The door connects two rooms (edge graph like)
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


        # print("\n------------------------")
        # print("vertices",vertices)
        # print("vertices other", other_room.get_vertices())
        # print(self.name)
        # print("x_interval_other",x_interval_other)
        # print("x_midpoint_other",x_midpoint_other)
        # print("x_interval",x_interval)
        # print("x_midpoint",x_midpoint)
        # print("y_interval_other", y_interval_other)
        # print("y_midpoint_other", y_midpoint_other)
        # print("y_interval", y_interval)
        # print("y_midpoint", y_midpoint)
        # print("\n------------------------")

        door_width = 100
        wall_margin = 10

        # check adjacency rooms and if there is possibility to place the door, infer the side
        if (other_room.y + other_room.height/2 + wall_margin == self.y - self.height/2) \
            and (((x_midpoint - door_width/2 in x_interval_other) and (x_midpoint + door_width/2 in x_interval_other))\
            or  ( (x_midpoint_other - door_width/2 in x_interval) and (x_midpoint_other + door_width/2 in x_interval)) ):

            side = 'north'
            x_door = vertices['left-top'][0]
            y_door = vertices['left-top'][1]
            angle_door = 0
            if self.width > other_room.width:
                displacement = other_room.width/2
            else:
                displacement = self.width/2

        elif (other_room.x + other_room.width/2 + wall_margin == self.x - self.width/2)\
            and (((y_midpoint - door_width/2 in y_interval_other) and (y_midpoint + door_width/2 in y_interval_other))\
            or  ( (y_midpoint_other - door_width/2 in y_interval) and (y_midpoint_other + door_width/2 in y_interval)) ):

            side = 'west'
            x_door = vertices['left-down'][0]
            y_door = vertices['left-down'][1]
            angle_door = 90
            if self.height > other_room.height:
                displacement = other_room.height/2
            else:
                displacement = self.height/2

        elif (other_room.y - other_room.height/2 - wall_margin == self.y + self.height/2) \
            and (((x_midpoint - door_width/2 in x_interval_other) and (x_midpoint + door_width/2 in x_interval_other))\
            or  ( (x_midpoint_other - door_width/2 in x_interval) and (x_midpoint_other + door_width/2 in x_interval)) ):

            side = 'south'
            x_door = vertices['right-down'][0]
            y_door = vertices['right-down'][1]
            angle_door = 180
            if self.width > other_room.width:
                displacement = other_room.width/2
            else:
                displacement = self.width/2

        elif (other_room.x - other_room.width/2 - wall_margin == self.x + self.width/2)\
            and (((y_midpoint - door_width/2 in y_interval_other) and (y_midpoint + door_width/2 in y_interval_other)) \
            or  ( (y_midpoint_other - door_width/2 in y_interval) and (y_midpoint_other + door_width/2 in y_interval)) ):

            side = 'east'
            x_door = vertices['right-top'][0]
            y_door = vertices['right-top'][1]
            angle_door = 270
            if self.height > other_room.height:
                displacement = other_room.height/2
            else:
                displacement = self.height/2
        else:
            raise ValueError(f"No valid position for the adjacent room")


        door = Door(self.name + "_" + side + "_" + str(displacement) + "_door", self.screen,
                    x_door, y_door, angle_door, displacement, door_width, side, status, self,
                    other_room, self.group, is_main)

        # add door object to the environment group
        self.group.add(door)

        # add door in the list of doors for the rooms
        self.doors[side] = door

        # i do the same for the adjacent room, using the opposite cardinal direction
        if side == 'north':
            other_room.doors['south'] = door
        elif side == 'west':
            other_room.doors['east'] = door
        elif side == 'south':
            other_room.doors['north'] = door
        elif side == 'east':
            other_room.doors['west'] = door

        if side == 'north' or side == 'south':
            self._edit_boundaries(side, door.rect.center[0] - door_width/2, door.rect.center[0] + door_width/2)
        elif side == 'west' or side == 'east':
            self._edit_boundaries(side, door.rect.center[1] - door_width/2, door.rect.center[1] + door_width/2)

        return door

    def add_window(self, side: str, displacement: int, status='close'):
        """
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

        window_l = Window(self.name + "_" + "left" + "_" + side + "_" + str(displacement) + "_window",
                        self.screen, x_win, y_win, angle_win, displacement, side, True, status, self, self.group)

        window_r = Window(self.name + "_" + "right" + "_" + side + "_" + str(displacement) + "_window",
                        self.screen, x_win, y_win, angle_win, displacement, side, False, status, self, self.group)

        # add window left and right in the group
        self.group.add(window_l)
        self.group.add(window_r)

        # add both windows as a tuple in the list of windows for the Room
        self.windows[side] = (window_l,window_r)

        return window_l, window_r

    def add_furniture(self): #todo
        pass

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

class Door(HouseElement):  #used to connect two rooms or a room and the outdoor
    def __init__(self, name, screen, x, y, angle_side, displacement, door_width, side, status, room_a, room_b, group, is_main = False):
        super().__init__(name, screen, group, x, y, width= door_width, height= 100)

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

        # correct angle based on status
        self._correctionStatus()

        # create debug rect
        self.display_gfxRect()

        # load sound effects
        self.sound_open = pg.mixer.Sound("static/open_door.mp3")
        self.sound_close = pg.mixer.Sound("static/close_door.mp3")

        # compute reduced rect for white surface of opened door
        self.rect_open = self._get_reduced_rect()

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

    def _load_images(self):
        if not(self.is_main):
            self.image_door = pg.image.load("static/door.png").convert_alpha()
        else:
            self.image_door = pg.image.load("static/main_door.png").convert_alpha()
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
            print(self.rel_angle)

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
        self.display_gfxRect()

    def draw(self):
        if abs(self.rel_angle) == abs(self.angle_open):
            pg.draw.rect(surface= self.screen, color=(15, 255, 80), rect=self.rect_open)
        super().draw()

class Window(HouseElement):
    def __init__(self, name, screen, x, y, angle_side, displacement, side, is_left: bool, status, room, group):
        super().__init__(name, screen, group, x, y, width= 60, height= 100)

        self.status = status            # status(str) -> open || close
        self.side = side                # side(str) -> north || west || south || east
        self.angle_side = angle_side    # global angle (int) respect the world (screen) when windows are closed
        self.rel_angle = 0              # relative angle (int) from the creation reference frame
        self.angle_open = - 135         # relative angle (int) that represent the open state
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

        # correct angle based on status
        self._correctionStatus()

        # create debug rect
        self.display_gfxRect()

        # load sound effects
        self.sound_open = pg.mixer.Sound("static/window_open.mp3")
        self.sound_close = pg.mixer.Sound("static/window_close.mp3")

        # compute reduced rect for white surface of opened window
        self.rect_open = self._get_reduced_rect()

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

    def _load_images(self):
        # load both images (no transformations)
        self.image_open = pg.image.load("static/window_open.png").convert_alpha()
        self.image_close = pg.image.load("static/window-closed.png").convert_alpha()

        # load actual image based on status
        if self.status == 'open':
            self.image = pg.image.load("static/window_open.png").convert_alpha()
        elif self.status == 'close':
            self.image = pg.image.load("static/window-closed.png").convert_alpha()
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

            print(self.rel_angle)

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

        # display rect for debug
        self.display_gfxRect()

    def draw(self):
        if abs(self.rel_angle) == abs(self.angle_open):
            pg.draw.rect(surface= self.screen, color=(15, 255, 80), rect=self.rect_open)
        super().draw()

class Furniture(HouseElement):
    def __init__(self, name, screen, group, x, y, width, height):
        super().__init__(name, screen, group, x, y, width, height)

class Pepper(HouseElement):
    def __init__(self, screen, group, room):
        super().__init__('Pepper', screen, group, room.x, room.y, width = 20, height= 20)
        self.rel_angle = 0
        self.actual_room = room
        self.color = (255, 255, 255)
        self.p_letter = Text("P", self.screen, self.x, self.y, color=(0, 0, 0), size_font= 21)

        # homing data
        self.homing_room_name = 'Studio'
        self.homing_room_position = (room.x, room.y)

        # adding to the environment group
        self.group.add(self)
        self.group.add(self.p_letter)

        # pepper socket for communication with simulator
        self.socket = PepperSocket()

    def move_to(self, position):
        pass

    def set_color(self, color):
        self.color = color

    def draw(self):
        # draw a circle to track the position
        pg.draw.circle(self.screen, color=(0, 0, 0), center=(self.x, self.y), radius=13)  # thick circle
        pg.draw.circle(self.screen, color=self.color, center=(self.x, self.y), radius=10)
        self.p_letter.center_to(self.x, self.y)

    def get_logo(self, width = 80, height = 80):
        logo = StaticImage("static/pepper.png", self.screen, self.x - width/2, self.y - height/2, width, height)
        return logo









