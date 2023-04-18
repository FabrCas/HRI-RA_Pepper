import pygame
import pygame as pg
import math

# ---------------------------------------------- static and global variables

progDos_rects           = 1
progDos_static_images   = 1
progDos_buttons         = 1
progDos_texts           = 1
progDos_TextBoxes       = 1
progDos_room            = 1
progDos_door            = 1
progDos_window          = 1
progDos_furniture         = 1

font_path = "static/nasa_font.ttf"

tiles = {
    'parquet': 'static/floor_parquet.jpg',
    'grey': 'static/floor_grey_tiles.jpg',
    'white': 'floot_white.jpg',
    'marble': 'static/floor_marble.jpg',
}

furniture = {

}


"""
    attributes understanding
    1) x,y refers to the top left corner of the rect: Rect, StaticImage, Text, InputTextBox, OutputTextBox
        in general is used from pygame for all rect that contains DOs
    2) x,y referes to the center of the rect: Button, HouseElement
        in general us used from pygame to handle each kind of surface, if i take the rect from the surface i pass to (1)
"""

# ---------------------------------------------- [UI]

# simple rect subclass that inherits the Sprite superclass used for testing
class Rect(pg.sprite.Sprite):

    def __init__(self, screen, x, y, width = 50, height = 50, color = (0,0,0), alpha = 255):
        super().__init__()

        self.screen = screen
        self.image = pg.Surface((width, height)).convert_alpha()

        self.image.fill((*color, alpha))

        self.rect = self.image.get_rect()

        # self.rect.center = (x, y)
        self.rect.x = x
        self.rect.y = y
        self.type_DO = "rect"

        global progDos_rects
        self.prog = progDos_rects
        progDos_rects += 1

        print(f"Created {self.type_DO} n° {self.prog}")

    def draw(self):
        self.screen.blit(self.image,self.rect)



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
        # if needed can be used a cooling time variable to reduce the number of switch

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
    def __init__(self, name, screen, x, y, width, height):   # x and y center of the DO box rectangle
        super().__init__()
        self.name = name
        self.screen = screen
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

        print(f"Created {self.type_DO} ({self.name}) n° {self.prog}")


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

    # rotation functions support all the angles, by the way only multiples of pi/2 are used in this case
    def rotate(self, angle):
        self.image = pg.transform.rotate(self.image, angle)  # se the rotation is of the surface, not the rect!

        # update the rect and move to the starting position
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.rel_angle += angle

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

    def _rotate_pivot(self,origin, pivot, angle):
        """
        :param pivot:  position of the pivot on the target Surface screen (relative to the top left of screen)
        # :param pivot: position of the pivot on the image Surface (relative to the top left of image)
        :param offset: 2d vector that represent the offset between the pivot and the center of the image
        :param angle:  angle for the rotation (degrees)
        :return: None

        How to perform rotation of an image around a pivot:
        - step 1: rotate the image
        - step 2: take a vector from pivot position to the center of the image (offset) and rotate
        - step 3: get the new rect from (1), and pass the pivot point plus offset vector as the center argument
                to shift the new rect
        """

        image_rect = self.image.get_rect(topleft = (origin[0] - pivot[0], origin[1] - pivot[1]))
        offset_center_to_pivot = pg.math.Vector2(origin) - image_rect.center
        rotated_offset = offset_center_to_pivot.rotate(-angle)
        rotated_image_center = (origin[0] - rotated_offset.x, origin[1] - rotated_offset.y)
        self.image =  pg.transform.rotozoom(self.image, angle, 1)
        self.rect = self.image.get_rect(center = rotated_image_center)



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
    def __init__(self, name, screen, x, y, width, height, env_group, tile_type):
        super().__init__(name, screen, x, y, width, height)
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
        self.group = env_group

        # list of elements
        self.walls = []
        self.windows    = []
        self.doors      = []
        self.furnitures = []

        self.group.add(self)

    def create_walls(self):
        pass

    def add_door(self, room: HouseElement):   # the door connects two rooms
        pass

    def add_window(self, side, displacement, status = 'close'): # side: top,left,bottom,right
        vertices = self.get_vertices()

        if side == 'top':
            x_win = vertices['left-top'][0]
            y_win = vertices['left-top'][1]
            angle_win = 0
        elif side == 'left':
            x_win = vertices['left-down'][0]
            y_win = vertices['left-down'][1]
            angle_win = 90
        elif side == 'bottom':
            x_win = vertices['right-down'][0]
            y_win = vertices['right-down'][1]
            angle_win = 180
        elif side == 'right':
            x_win = vertices['right-top'][0]
            y_win = vertices['right-top'][1]
            angle_win = 270

        # left window with convention of beeing oriented downward
        window_l = Window(self.name + "_" + "left" + "_" + side + "_" + str(displacement) + "_window",
                        self.screen, x_win, y_win, angle_win, displacement, side, True, status, self.group)

        window_r = Window(self.name + "_" + "right" + "_" + side + "_" + str(displacement) + "_window",
                        self.screen, x_win, y_win, angle_win, displacement, side, False, status, self.group)

        # add window left and right in the group
        self.group.add(window_l)
        self.group.add(window_r)

        # add both windows as a tuple in the list of windows for the Room
        # self.windows.append((window_l,window_r))
        return window_l

class Door(HouseElement):  #used to connect two rooms or a room and the outdoor
    def __init__(self, name, screen, x, y, status):
        super().__init__(name, screen, x, y, width= 20, height= 10)
        self.status = status


    def open(self):  # try animations
        if self.status == 'open':
            return
        else:
            self.status == 'close'
            return

    def close(self):
        if self.status == 'close':
            return
        else:
            self.status == 'open'
            return


class Window(HouseElement):
    def __init__(self, name, screen, x, y, angle, displacement, side, is_left, status, group):
        super().__init__(name, screen, x, y, width= 100, height= 80)

        self.status = status
        self.side = side                # side(str) -> top || left || bottom || right
        self.angle_start = angle        # global angle (int) respect the world (screen)
        self.rel_angle = 0              # relative angle (int) from the creation reference frame
        self.angle_open = - 135         # relative angle (int) that represent the open state
        self.angle_close = 0            # relative angle (int) that represent the close state
        self.is_left: bool
        self.is_left = is_left          # boolean variable to indicate which window door is of the pair
        self.group = group


        # load image
        if self.status == 'open':
            self.image = pg.image.load("static/window_open.png").convert_alpha()
        elif self.status == 'close':
            self.image = pg.image.load("static/window-closed.png").convert_alpha()
        else:
            raise ValueError("Wrong button type has been assigned")

        # compute correct displacement and transform image: flip if right window, upscale/downscale, rotate
        if is_left:
            self.displacement = displacement - self.width/2
        else:
            self.displacement = displacement + self.width/2
            self.image = pg.transform.flip(self.image, True, False)

        self.image = pg.transform.smoothscale(self.image, (self.width, self.height))
        self.image = pg.transform.rotate(self.image, self.angle_start)

        # get the rect containing the surface (image)
        self.rect = self.image.get_rect()

        # correct positions
        self.correctionPos_()

        # create debug rect
        self.display_gfxRect()

        # load sound effects
        self.sound_open = pg.mixer.Sound("static/window_open.mp3")
        self.sound_close = pg.mixer.Sound("static/window_close.mp3")


    def correctionPos_(self):

        # correct displacement on the axis
        if self.side == 'top':
            self.rect.center = (self.x + self.displacement, self.y)
        elif self.side == 'left':
            self.rect.center = (self.x, self.y - self.displacement)
        elif self.side == 'bottom':
            self.rect.center = (self.x - self.displacement, self.y)
        elif self.side == 'right':
            self.rect.center = (self.x, self.y + self.displacement)

        print("self.rect.center", self.rect.center)
        print("self.rect.topleft", self.rect.topleft)
        print("self.rect.topright", self.rect.topright)
        print("self.rect.bottomleft", self.rect.bottomleft)
        print("self.rect.bottomright", self.rect.bottomright, "\n")


        # correct angle if window has open status
        if self.status == 'open':
            if self.is_left:   # left window (seen frontally)
                pass
                # self._rotate_pivot(self.rect.center, (-self.width/2 + 10, 0), self.angle_open)

                # self.image = pg.transform.rotate(self.image, self.angle_open)
                # self.rect = self.image.get_rect(center = self.rect.center)

            else:               # right window (seen frontally)
                self.image = pg.transform.rotate(self.image, - self.angle_open)
                self.rect = self.image.get_rect(center=self.rect.center)


    def open(self): # try animations
        if self.status == 'open':   # nothing to do
            return
        else:                       # from close to open
            pg.mixer.Sound.play(self.sound_open)
            # todo update the image

            self.status = 'open'
            self.rel_angle = 0

    def close(self):
        if self.status == 'close':
            return
        else:                       # from open to close
            pg.mixer.Sound.play(self.sound_close)

            # todo update the image
            self.status = 'close'
            if self.is_left:
                self.rel_angle = -135
            else:
                self.rel_angle = 135

    def update(self):
        if self.status == 'open' and abs(self.rel_angle) < abs(self.angle_open):
            if self.is_left:
                self.rel_angle -= 1
                self.display_gfxRect()
                print(self.rel_angle)
                self._rotate_pivot(self.rect.center, (-self.width/2,self.height/2), -0.00001)



        elif self.status == 'close' and abs(self.rel_angle) > abs(self.angle_close):
            pass





class Furniture(HouseElement):
    def __init__(self, name, screen, x, y, width, height):
        super().__init__(name, screen, x, y, width, height)

class Pepper():
    def __init__(self):
        pass









