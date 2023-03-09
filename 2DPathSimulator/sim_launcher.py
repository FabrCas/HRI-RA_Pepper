import pygame
import pygame as pg
import time
import os
import sys
import math
from display_objects import Rect, Button

# definition of constants as default values
WIDTH_WIN = 640
HEIGHT_WIN = 480
X_WIN = 0
Y_WIN = 0
FPS = 60;
XC_WIN = lambda : math.ceil(WIDTH_WIN/2)
YC_WIN = lambda : math.ceil(HEIGHT_WIN/2)

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
    rect = Rect(XC_WIN(), YC_WIN())
    elements_group.add(rect)

    return elements_group

def create_UI():
    ui_group = pg.sprite.Group()
    button_on = Button(300,300, 50,50, 'on')
    button_off = Button(300, 600, 50, 50, 'off')

    ui_group.add(button_on)
    ui_group.add(button_off)
    return ui_group



def rendering():
    screen, clock = initialization()
    ui_group = create_UI()
    elements_group = create_DOs()

    while True:
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
                for ui_elem in ui_group:
                    if ui_elem.type_DO == 'button' and (ui_elem.rect.collidepoint(mouse_pos)):
                        ui_elem.change_status()




            if event.type == pg.MOUSEBUTTONUP:
                print("Mouse released")
                mouse_pos = pg.mouse.get_pos()
                # if player.rect.collidepoint(pygame.mouse.get_pos()):



        # Logical updates
        ui_group.update()
        # elements_group.update()



        # Render graphics
        screen.fill((255, 255, 255))
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