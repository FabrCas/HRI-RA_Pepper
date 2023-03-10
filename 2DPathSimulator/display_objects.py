import pygame as pg


# ---------------------------------------------- [UI]

progDos_rects           = 1
progDos_static_images   = 1
progDos_buttons         = 1
progDos_texts           = 1
progDos_TextBoxes       = 1

font_path = "static/nasa_font.ttf"
font_size = 30

# simple rect subclass that inherits the Sprite superclass
class Rect(pg.sprite.Sprite):

    def __init__(self, x, y, width = 50, height = 50, color = (0,0,0)):
        super().__init__()
        self.image = pg.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.type_DO = "rect"
        global progDos_rects
        self.prog = progDos_rects
        progDos_rects += 1

        print(f"Created {self.type_DO} n° {self.prog}")

class StaticImage(pg.sprite.Sprite):

    def __init__(self, file_path, x, y, width=50, height=50):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pg.image.load(file_path).convert_alpha()
        self.image = pg.transform.smoothscale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = self.x#    (self.x, self.y)
        self.rect.y = self.y
        self.type_DO = 'static_image'
        global progDos_static_images
        self.prog = progDos_static_images
        progDos_static_images += 1

        print(f"Created {self.type_DO} n° {self.prog}")


class Button(pg.sprite.Sprite):

    def __init__(self, name ,  x, y, width, height, type_button='on'):

        super().__init__()
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.name = name
        self.status = type_button
        # image = pg.image.load("static/buttons_.png").convert_alpha() # sprite for both on and off button
        # # crop image to get green
        # rect = image.get_rect()
        # crop_rect = pg.Rect(rect.x, rect.y, rect.width/2, rect.height)
        # self.image = image.subsurface(crop_rect)
        if type_button == 'on':
            self.image = pg.image.load("static/green_bt.png").convert_alpha() # sprite for both on and off button
        else:
            self.image = pg.image.load("static/red_bt.png").convert_alpha()
        self.image = pg.transform.smoothscale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.last_click = None
        self.type_DO = 'button'

        global progDos_buttons
        self.prog = progDos_buttons
        progDos_buttons += 1

        print(f"Created {self.type_DO} ({self.name}) n° {self.prog}")

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
            self.image = pg.image.load("static/red_bt.png").convert_alpha()
            self.image = pg.transform.smoothscale(self.image, (self.width, self.height))
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)
            self.status = 'off'
            self.update()

        elif self.status == 'off':
            print(f'button {self.name} goes to on')
            self.image = pg.image.load("static/green_bt.png").convert_alpha()
            self.image = pg.transform.smoothscale(self.image, (self.width, self.height))
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)
            self.status = 'on'
            self.update()


class Text(pg.sprite.Sprite):

    def __init__(self, string, x, y,  color, size_font=font_size):
        super().__init__()
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
        # self.rect.center = (self.x, self.y)
        self.rect.x = self.x
        self.rect.y = self.y
        self.image = self.text

        print(f"Created {self.type_DO} n° {self.prog}")

    def center_to(self, x = None ,y = None):
        if x == None and y == None:
            return
        elif x == None:
            self.rect.center = (self.rect.center[0], y)
        elif y == None:
            self.rect.center = (x, self.rect.center[1])
        else:
            self.rect.center = (x, y)


class InputTextBox():

    def __init__(self,screen, x, y, height, color_text, color_bg, size_font=font_size):
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


    def render(self, max_width=200):
        pg.draw.rect(self.screen, self.color_bg, self.rect)
        self.text = self.font.render(self.text_box, True, self.color_text)

        new_width = min(max_width, self.text.get_width() + 10)

        # stretch the box until the limit is reached
        if new_width > self.min_width:
            self.rect.w = new_width + 10

        # show partially the text if the new limit is reached
        if self.text.get_width() > self.rect.w:
            # print("ao stai a sforà")
            partial_text = self.text_box
            while(self.text.get_width() > self.rect.w - 10):
                partial_text = partial_text[1:]
                self.text = self.font.render(partial_text, True, self.color_text)

        self.screen.blit(self.text, (self.rect.x + 5, self.rect.y + 5))

    def restore_defult(self):
        self.rect.w = self.min_width
        self.text_box = self.default_text

class OutputTextBox():

    def __init__(self,screen, x, y, width, height, color_text, color_bg, size_font=font_size):
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




    def render(self):

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

        # todo


        # print messages as lines after the split
        vertical_offset = 0
        for idx, message in enumerate(visible_messages):
            if type(message) == str:
                self.text = self.font.render(message, True, self.color_text)
                self.screen.blit(self.text, (self.rect.x + 5, self.rect.y + 5 + 25 *vertical_offset))
                vertical_offset += 1
            elif type(message) == list:
                for sub_messsage in message:
                    self.text = self.font.render(sub_messsage, True, self.color_text)
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

    def restore_defult(self):
        self.text_box = self.default_text
# ---------------------------------------------- [Simulation]

class Room():
    def __init__(self):
        pass

class Pepper():
    def __init__(self):
        pass

class HouseObject():
    def __init__(self):
        pass

class Furniture():
    def __init__(self):
        pass











