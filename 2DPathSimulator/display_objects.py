import pygame as pg
import time

# test subclass that inherits the Sprite superclass
class Rect(pg.sprite.Sprite):
    def __init__(self, x, y, width = 50, height = 50, color = (0,0,0)):
        super().__init__()
        self.image = pg.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.type_DO = "rect"

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
    def __init__(self, string, x, y, size_font, color):
        super().__init__()
        self.x = x
        self.y = y
        self.size = size_font
        self.color = color
        self.type_DO = "text"

        # create font object
        self.font = pg.font.Font('freesansbold.ttf', self.size)

        # create display object and get its rect
        self.text = self.font.render(string, True, color)   # text, antialiasing, color, bg color
        self.rect = self.text.get_rect()
        self.rect.center = (self.x, self.y)
        self.image = self.text

class TextBox():
    def __init__(self,screen, x, y, width, height, size_font, color_text, color_bg):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.size = size_font
        self.color_text = color_text
        self.color_bg = color_bg
        self.type_DO = "text box"
        self.rect = pg.Rect(self.x,self.y, self.width, self.height)

        # variable to manage filling of the box
        self.default_text = '*insert text here*'
        self.text_box = self.default_text
        self.box_active = True

        # create font object
        self.font = pg.font.Font('freesansbold.ttf', self.size)
        self.text = self.font.render(self.text_box, True, self.color_text)
        self.min_width = self.text.get_width() + 10
        # self.image = self.text

    def render(self):
        pg.draw.rect(self.screen, self.color_bg, self.rect)
        self.text = self.font.render(self.text_box, True, self.color_text)
        self.screen.blit(self.text, (self.rect.x + 5, self.rect.y + 5))
        new_width = max(200, self.text.get_width() + 10)
        if new_width -10  > self.min_width:
            self.rect.w = new_width

    # def update(self):
        # self.image = self.text

    def restore_defult(self):
        self.text_box = self.default_text











