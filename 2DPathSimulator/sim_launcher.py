import pygame
import pygame as pg
import time
import os
import sys
import math
from display_objects import Rect, Button, Text, TextBox

# definition of constants as default values
WIDTH_WIN = 640
HEIGHT_WIN = 480
X_WIN = 0
Y_WIN = 0
FPS = 60;
XC_WIN = lambda : math.ceil(WIDTH_WIN/2)
YC_WIN = lambda : math.ceil(HEIGHT_WIN/2)

texts = []

def update_win_size():
    global WIDTH_WIN
    global HEIGHT_WIN
    global X_WIN
    global Y_WIN
    info_display = pg.display.Info()
    WIDTH_WIN = math.floor(info_display.current_w/2)
    HEIGHT_WIN = info_display.current_h - 75
    X_WIN = WIDTH_WIN
    Y_WIN = 35

def initialization():
    # initialize pygame
    pg.init()
    update_win_size()

    # move the position where to create the window modifying the SDL properties
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (X_WIN, Y_WIN)

    screen = pg.display.set_mode((WIDTH_WIN, HEIGHT_WIN))  # it's a surface object with all the space
    pg.display.set_caption("2D simulator HRI-RA")
    clock = pg.time.Clock()

    return screen, clock

def create_DOs():
    elements_group = pg.sprite.Group()

    # add Display elements
    # rect = Rect(XC_WIN(), YC_WIN(), 100,200,(0,255,0))
    # elements_group.add(rect)
    return elements_group

def create_UI(screen):
    ui_group = pg.sprite.Group()
    text_boxes = []
    button_on   = Button(300,300, 50,50, 'on')
    button_off  = Button(300, 600, 50, 50, 'off')
    text_sleep  = Text("Sleep: ", x=220, y=300, size_font=20, color=(0, 0, 0))
    text_box    = TextBox(screen, x=220, y=500, width=200, height= 30, size_font=20,\
                          color_text=(0, 0, 255), color_bg=(255,0,255))

    text_boxes.append(text_box)
    ui_group.add(text_sleep)
    ui_group.add(button_on)
    ui_group.add(button_off)
    return ui_group, text_boxes


def rendering():
    # initialize the pygame engine, get main display object and clock for the rendering
    screen, clock = initialization()
    # create display objects for the UI
    ui_group, text_boxes = create_UI(screen)
    # create display objects for the simulation
    elements_group = create_DOs()

    deleting = None; time_delete = time.time()
    while True:

        if deleting is not None:
            cooldown_delete = time.time() - time_delete
            if  cooldown_delete > 0.05:
                deleting.text_box = deleting.text_box[:-1]
                time_delete = time.time()

        # Process player inputs.
        for event in pg.event.get():

            # Quit simulation
            if event.type == pg.QUIT: # pg.QUIT generated when the window is closed
                print("Closed the window using the button")
                pg.quit()
                sys.exit()
                raise SystemExit

            if event.type == pg.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("Closed the window using the ESC key")
                    pg.quit()
                    exit(0)

            # Mouse click events
            if event.type == pg.MOUSEBUTTONDOWN:
                print("Mouse clicked")
                mouse_pos = pg.mouse.get_pos()

                # interact with the buttons
                for ui_elem in ui_group:
                    if ui_elem.type_DO == 'button' and (ui_elem.rect.collidepoint(mouse_pos)):
                        ui_elem.change_status()

                    # if ui_elem.type_DO == 'text box':
                # interact with the input boxes
                for text_box in text_boxes:
                    if (text_box.rect.collidepoint(mouse_pos)):
                        text_box.box_active = True
                        if text_box.text_box == text_box.default_text:
                            text_box.text_box = ''
                        print(text_box.type_DO + ' is activated')
                    else:
                        text_box.box_active = False
                        # text_box.restore_defult()

            if event.type == pg.MOUSEBUTTONUP:
                print("Mouse released")
                mouse_pos = pg.mouse.get_pos()
                # if player.rect.collidepoint(pygame.mouse.get_pos()):

            # text input events
            if event.type == pg.KEYDOWN:
                for text_box in text_boxes:
                    if text_box.type_DO == 'text box' and text_box.box_active:
                        if event.key == pg.K_BACKSPACE:
                            deleting = text_box
                            text_box.text_box = text_box.text_box[:-1]
                        else:
                            deleting = None
                            if event.key == pg.K_RETURN: # reset the text in the box
                                print(text_box.text_box)
                                # text_box.text_box = ''
                                text_box.box_active = False
                                text_box.restore_defult()
                            else:
                             text_box.text_box += event.unicode

            if event.type == pg.KEYUP:
                if event.key == pg.K_BACKSPACE: deleting = None


        # Logical updates
        ui_group.update()
        elements_group.update()

        # Render graphics
        screen.fill((255, 255, 255))
        for text_box in text_boxes:
            text_box.render()

        ui_group.draw(screen)
        elements_group.draw(screen)

        # update the screen with the current state of the display objects
        pg.display.flip()

        # use current selected FPS property for the rendering
        clock.tick(FPS)

        # time.sleep(6)  #synchronous waiting and exit
        # break

if __name__ == '__main__':
    print(f"Pygame version: {pg.__version__}")

start_time = time.time()
rendering()
rendering_time = time.time() - start_time
print("Rendering time {} [s]".format(round(rendering_time, 3)))