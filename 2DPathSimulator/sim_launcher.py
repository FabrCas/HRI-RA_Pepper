import pygame
import pygame as pg
import time
import os
import sys
import math
import threading
import asyncio
from display_objects import Rect, Button, Text, InputTextBox, StaticImage, OutputTextBox

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
    # create collections
    ui_group = pg.sprite.Group()
    text_boxes = []  # text boxes are handled differently since are custom objects that don't inherit pygame classes

    # print(screen.get_width(), screen.get_height())

    # 1) create lateral panel and title
    # ltc -> left top corner
    lateral_panel_ltc_x = math.ceil(screen.get_width()*2/3)
    lateral_panel_ltc_y = 0
    lateral_panel_width = math.ceil(screen.get_width()/3)
    lateral_panel_height = screen.get_height()
    lateral_panel =  StaticImage(file_path = "static/lateral_panel.jpg", x= lateral_panel_ltc_x,
                                 y =lateral_panel_ltc_y, width= lateral_panel_width, height= lateral_panel_height)
    text_control_panel = Text("Control Panel", x= lateral_panel_ltc_x
                              , y=10,  color=(255, 255, 255), size_font=30)
    text_control_panel.center_to(x = lateral_panel_ltc_x + lateral_panel_width/2)

    ui_group.add(lateral_panel)
    ui_group.add(text_control_panel)

    # 2) create prompt
    text_prompt = Text("Prompt ", x=lateral_panel_ltc_x + 10, y=90,  color=(255, 255, 255), size_font=20)
    prompt    = InputTextBox(screen, x=lateral_panel_ltc_x + 135, y=85, height= 30,
                               color_text=(0, 0, 0), color_bg=(200,200,200),size_font=20)

    ui_group.add(text_prompt)
    text_boxes.append(prompt)

    # 3) create buttons
    text_sleep  = Text("Sleep mode ", x=lateral_panel_ltc_x + 10, y=170,  color=(255, 255, 255), size_font=20)
    button_sleep = Button("sleep",lateral_panel_ltc_x + lateral_panel_width*3/5, 170 + 15, 60, 60, 'off')

    text_mic  = Text("Microphone ", x=lateral_panel_ltc_x + 10, y=250,  color=(255, 255, 255), size_font=20)
    button_mic = Button("microphone", lateral_panel_ltc_x + lateral_panel_width*3/5, 250 + 15, 60, 60, 'on')

    text_extraHUD = Text("Extra HUD ", x=lateral_panel_ltc_x + 10, y=330,  color=(255, 255, 255), size_font=20)
    button_extraHUD = Button('HUD', lateral_panel_ltc_x + lateral_panel_width*3/5, 330 + 15, 60, 60, 'off')

    ui_group.add(text_sleep)
    ui_group.add(button_sleep)
    ui_group.add(text_mic)
    ui_group.add(button_mic)
    ui_group.add(text_extraHUD)
    ui_group.add(button_extraHUD)

    # 4) create system Output box
    system_box = OutputTextBox(screen, x= lateral_panel_ltc_x + 10, y= lateral_panel_height - 410, width=lateral_panel_width -20, height= 400,
                               color_text=(0, 0, 0), color_bg=(200,200,200),size_font=20)

    text_system_box = Text("System output", x=lateral_panel_ltc_x + 10, y= system_box.y-30,  color=(255, 255, 255), size_font=20)
    text_system_box.center_to(x = lateral_panel_ltc_x + lateral_panel_width/2)
    text_boxes.append(system_box)
    ui_group.add(text_system_box)

    # test inserendo i messaggi
    system_box.add_message("primo messaggio")
    system_box.add_message("secondo messaggio")
    system_box.add_message("prova prova prova")
    system_box.add_message("sa")
    system_box.add_message("prova prova prova")
    system_box.add_message("sa")
    system_box.add_message(
        "Messaggio molto lungo anzi lunghissimo direi bislungo, ma esiste veramente come parola 'bislungo'? Ma alla fine che ne so io penso di si boh")
    system_box.add_message("prova prova prova")
    system_box.add_message("Bla bla bla bla bla blu blue blue")
    system_box.add_message("Messaggio molto lungo, anzi lunghissimo direi bislungo, ma esiste veramente come parola 'bislungo'? Ma alla fine che ne so io penso di si boh")

    start_time = threading.Timer(3, lambda : system_box.add_message("Nuovo messaggio"))
    start_time.start()

    return ui_group, text_boxes

def rendering():

    # initialize the pygame engine, get main display object and clock for the rendering
    screen, clock = initialization()
    # create display objects for the UI
    ui_group, text_boxes = create_UI(screen)
    # create display objects for the simulation
    elements_group = create_DOs()

    # variable used for the continuous elimination of characters when pressing backspace
    deleting = None; time_delete = time.time(); deleting_wait = 0.15

    pressed_sx_mouse = False

    # ---------------------------------------- Main rendering Loop
    while True:

        if deleting is not None:
            cooldown_delete = time.time() - time_delete
            if  cooldown_delete > deleting_wait:
                deleting_wait *= 0.7
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
            if event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[0]:
                pressed_sx_mouse = True
                print("Mouse clicked")
                mouse_pos = pg.mouse.get_pos()

                # interact with the buttons
                for ui_elem in ui_group:
                    if ui_elem.type_DO == 'button' and (ui_elem.rect.collidepoint(mouse_pos)):
                        ui_elem.change_status()

                # interact with the input boxes
                for box in text_boxes:
                    if box.type_DO == "input text box":
                        if box.rect.collidepoint(mouse_pos):
                            box.box_active = True
                            if box.text_box == box.default_text:
                                box.text_box = ''
                            print(box.type_DO + ' is activated')
                        else:
                            if box.box_active:
                                box.box_active = False
                                print(box.type_DO + ' is deactivated')
                                if box.text_box.strip() == '':
                                    box.restore_defult()

            if event.type == pg.MOUSEBUTTONUP and (pressed_sx_mouse and not(pg.mouse.get_pressed()[0])):
                print("Mouse released")
                pressed_sx_mouse = False

            # text input events
            if event.type == pg.KEYDOWN:
                for box in text_boxes:
                    if 'input text box' in box.type_DO and box.box_active:
                        if event.key == pg.K_BACKSPACE:  # start the deleting, save time and box where remove chars
                            time_delete = time.time()
                            deleting = box
                            box.text_box = box.text_box[:-1]

                        elif event.key == pg.K_RETURN: # reset the text in the box
                            deleting = None
                            print(box.text_box)
                            box.box_active = False
                            box.restore_defult()

                        elif event.unicode.isprintable(): # insert unicode chars in the prompt
                            deleting = None
                            box.text_box += event.unicode

                        deleting_wait = 0.15  # reset the velocity when deleting characters from the prompt

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