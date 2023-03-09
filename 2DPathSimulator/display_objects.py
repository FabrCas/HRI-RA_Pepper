import pygame as pg

progDos_rects = 0
progDos_static_images = 0
progDos_buttons = 0
progDos_texts = 0
progDos_inputTextBoxes = 0

font_path = "static/nasa_font.ttf"
font_size = 30

# test subclass that inherits the Sprite superclass
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

    def __init__(self, x, y, width, height, type_button='on'):

        super().__init__()
        self.width = width
        self.height = height
        self.x = x
        self.y = y
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

        print(f"Created {self.type_DO} n° {self.prog}")

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
            print('button goes to off')
            self.image = pg.image.load("static/red_bt.png").convert_alpha()
            self.image = pg.transform.smoothscale(self.image, (self.width, self.height))
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)
            self.status = 'off'
            self.update()

        elif self.status == 'off':
            print('button goes to on')
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
        self.rect.center = (self.x, self.y)
        self.image = self.text

        print(f"Created {self.type_DO} n° {self.prog}")


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
        self.type_DO = "text box"
        global progDos_inputTextBoxes
        self.prog = progDos_inputTextBoxes
        progDos_inputTextBoxes += 1

        # variable to manage filling of the box
        self.default_text = '*insert text here*'
        self.text_box = self.default_text
        self.box_active = True

        # create font object
        self.font = pg.font.Font(font_path, self.size)
        self.text = self.font.render(self.text_box, True, self.color_text)
        self.min_width = self.text.get_width() + 10   # minimum length when it's used the default text
        self.rect = pg.Rect(self.x, self.y, self.min_width, self.height)

        print(f"Created {self.type_DO} n° {self.prog}")


    def render(self, max_width=200):
        pg.draw.rect(self.screen, self.color_bg, self.rect)
        self.text = self.font.render(self.text_box, True, self.color_text)

        new_width = min(max_width, self.text.get_width())

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











