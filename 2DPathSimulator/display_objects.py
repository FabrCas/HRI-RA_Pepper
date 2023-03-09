import pygame as pg
import time

# test subclass that inherits the Sprite superclass
class Rect(pg.sprite.Sprite):
    def __init__(self, x, y, dim = 50):
        super().__init__()
        self.image = pg.Surface((dim, dim))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

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

    # def update(self):
        # # if pg.mouse.get_pressed()[0]: # left mouse key pressed
        # mouse_pos = pg.mouse.get_pos()
        # if self.last_click == None:
        #     cooling_time = 1
        # else:
        #     cooling_time = abs(time.time() - self.last_click)
        # if self.rect.collidepoint(mouse_pos) and (cooling_time >0.2):
        #     print(f"Button has been pressed at coordinates {mouse_pos}")
        #     self.last_click = time.time()
        #     if self.status == 'on':
        #         self.image = pg.image.load("static/green_bt.png").convert_alpha()
        #         self.rect = self.image.get_rect()
        #         self.rect.center = (self.x, self.y)
        #         self.image = pg.transform.smoothscale(self.image, (self.width, self.height))
        #         self.status = 'of
        #
        #     elif self.status == 'off':
        #         self.image = pg.image.load("static/red_bt.png").convert_alpha()
        #         self.rect = self.image.get_rect()
        #         self.rect.center = (self.x, self.y)
        #         self.image = pg.transform.smoothscale(self.image, (self.width, self.height))
        #         self.status = 'on'

    def change_status(self):
        # if needed can be used a cooling time variable to reduce the number of switch

        # if self.last_click == None:
        #     cooling_time = 1
        # else:
        #     cooling_time = abs(time.time() - self.last_click)
        # if cooling_time >0.2:
            # print(f"Button has been pressed at coordinates {mouse_pos}")
        # self.last_click = time.time()

        print('sto qui')
        if self.status == 'on':
            print('go to off')
            self.image = pg.image.load("static/red_bt.png").convert_alpha()
            self.image = pg.transform.smoothscale(self.image, (self.width, self.height))
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)
            self.status = 'off'
            self.update()

        elif self.status == 'off':
            print('go to on')
            self.image = pg.image.load("static/green_bt.png").convert_alpha()
            self.image = pg.transform.smoothscale(self.image, (self.width, self.height))
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)
            self.status = 'on'
            self.update()




