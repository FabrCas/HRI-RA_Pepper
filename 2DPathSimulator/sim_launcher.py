import pygame
import pygame as pg
import time
import os
import sys
import math
import random
from display_objects import Rect, Button, Text, InputTextBox, StaticImage

# definition of constants as default values
WIDTH_WIN = 640
HEIGHT_WIN = 480
X_WIN = 0
Y_WIN = 0
FPS = 60
XC_WIN = lambda : math.ceil(WIDTH_WIN/2)
YC_WIN = lambda : math.ceil(HEIGHT_WIN/2)

texts = []

def random_position(screen):
    margin = 20
    x_r = random.randint(0 + margin, screen.get_width()  - margin)
    y_r = random.randint(0 + margin, screen.get_height() - margin)
    return x_r, y_r

def update_win_size():
    global WIDTH_WIN
    global HEIGHT_WIN
    global X_WIN
    global Y_WIN
    info_display = pg.display.Info()
    WIDTH_WIN = math.floor(info_display.current_w/2) +100
    HEIGHT_WIN = info_display.current_h - 75
    X_WIN = WIDTH_WIN -200
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
    text_boxes = []  # text boxes are handled differently since are custom objects that don't inherit pygame classes

    # lateral panel

    # print(screen.get_width(), screen.get_height())


    lateral_panel =  StaticImage(file_path = "static/lateral_panel.jpg", x= math.ceil(screen.get_width()*2/3), y =0, \
                                 width= math.ceil(screen.get_width()/3), height= screen.get_height())
                                 # width=1000, height=1000)
    button_on   = Button(300,300, 50,50, 'on')
    button_off  = Button(300, 600, 50, 50, 'off')
    text_sleep  = Text("Sleep: ", x=220, y=300,  color=(0, 255, 0), size_font=20)
    text_box    = InputTextBox(screen, x=220, y=500,height= 30,
                               color_text=(0, 0, 0), color_bg=(160,160,160),size_font=20)
    x_r, y_r = random_position(screen)
    text_box2    = InputTextBox(screen, x_r, y_r, height= 30,
                                color_text=(0, 0, 0), color_bg=(160,160,160), size_font=20)

    text_boxes.append(text_box)
    text_boxes.append(text_box2)

    ui_group.add(lateral_panel)
    ui_group.add(text_sleep)
    ui_group.add(button_on)
    ui_group.add(button_off)

    """
    - prompt command 
    - reset button 
    - sleep button 
    - simulator messages
    """

    return ui_group, text_boxes

def rendering():
    # initialize the pygame engine, get main display object and clock for the rendering
    screen, clock = initialization()
    # create display objects for the UI
    ui_group, text_boxes = create_UI(screen)
    # create display objects for the simulation
    elements_group = create_DOs()

    # variable used for the continuous elimination of characters when pressing backspace
    deleting = None; time_delete = time.time();

    # ---------------------------------------- Main rendering Loop
    while True:

        if deleting is not None:
            cooldown_delete = time.time() - time_delete
            if  cooldown_delete > 0.15:
                deleting.text_box = deleting.text_box[:-1]
                time_delete = time.time()

        # ---------------------------------------- Process user's inputs
        for event in pg.event.get():

            # Quit simulation
            if event.type == pg.QUIT: # pg.QUIT generated when the window is closed
                print("Closed the window using the button")
                pg.quit()
                # sys.exit()
                return

                # raise SystemExit

            if event.type == pg.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("Closed the window using the ESC key")
                    pg.quit()
                    # exit(0)
                    return

            # Mouse click events
            if event.type == pg.MOUSEBUTTONDOWN:
                print("Mouse clicked")
                mouse_pos = pg.mouse.get_pos()

                # interact with the buttons
                for ui_elem in ui_group:
                    if ui_elem.type_DO == 'button' and (ui_elem.rect.collidepoint(mouse_pos)):
                        ui_elem.change_status()

                # interact with the input boxes
                for box in text_boxes:
                    if (box.rect.collidepoint(mouse_pos)):
                        box.box_active = True
                        if box.text_box == box.default_text:
                            box.text_box = ''
                        print(box.type_DO + ' is activated')
                    else:
                        box.box_active = False
                        if box.text_box.strip() == '':
                            box.restore_defult()

            if event.type == pg.MOUSEBUTTONUP:
                print("Mouse released")
                mouse_pos = pg.mouse.get_pos()
                # if player.rect.collidepoint(pygame.mouse.get_pos()):

            # text input events
            if event.type == pg.KEYDOWN:
                for box in text_boxes:
                    if box.type_DO == 'text box' and box.box_active:
                        if event.key == pg.K_BACKSPACE:
                            time_delete = time.time()
                            deleting = box
                            box.text_box = box.text_box[:-1]

                        elif event.key == pg.K_RETURN: # reset the text in the box
                            deleting = None
                            print(box.text_box)
                            # text_box.text_box = ''
                            box.box_active = False
                            box.restore_defult()

                        elif event.unicode.isprintable():
                            deleting = None
                            box.text_box += event.unicode


            if event.type == pg.KEYUP:
                if event.key == pg.K_BACKSPACE: deleting = None


        # ---------------------------------------- Logical updates
        ui_group.update()
        elements_group.update()

        # ---------------------------------------- Render graphics
        # fill the background
        screen.fill((255, 255, 255))

        # render UI
        ui_group.draw(screen)
        for text_box in text_boxes:
            text_box.render()

        # render simulation graphical elements
        elements_group.draw(screen)

        # ---------------------------------------- display update

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
sys.exit(0)