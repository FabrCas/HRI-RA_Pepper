import pygame as pg
import time
import os
import gc
import sys
import math

# custom components
from environment import create_UI, create_environment
from services import InputInterpreter


# Definition of constants as default values
WIDTH_WIN = 1920; HEIGHT_WIN = 1080
X_WIN = 0; Y_WIN = 0
FPS = 60
XC_WIN = lambda: math.ceil(WIDTH_WIN/2); YC_WIN = lambda: math.ceil(HEIGHT_WIN/2)
os_systems = ['linux', 'windows']; os_selected = os_systems[1]

def update_win_size():
    global WIDTH_WIN
    global HEIGHT_WIN
    global X_WIN
    global Y_WIN
    info_display = pg.display.Info()
    WIDTH_WIN = math.floor(info_display.current_w/2) + 400  # 100
    HEIGHT_WIN = info_display.current_h - 75
    X_WIN = WIDTH_WIN - 800
    Y_WIN = 35

def initialization():
    # initialize pygame
    pg.init()
    update_win_size()

    # move the position where to create the window modifying the SDL properties
    if os_selected == 'windows':
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (X_WIN, Y_WIN)

    screen = pg.display.set_mode((WIDTH_WIN, HEIGHT_WIN))  # it's a surface object to draw in
    pg.display.set_caption("2D simulator HRI-RA")
    pg.display.set_icon(pg.image.load('static/assets/pepper.png'))
    # pg.display.toggle_fullscreen()

    clock = pg.time.Clock()

    return screen, clock

def debug_render(env_group, debug, show_obstacles):

    if debug:
        for el in env_group:
            if type(el).__name__ == "Room":
                el.render_debug_vertices()
                if not(el.visible_boundaries): el.show_boundaries()
            if type(el).__name__ in ["Window", "Door", "Furniture"]:
                el.render_debug_rect()

    elif show_obstacles:
        for el in env_group:
            if type(el).__name__ == "Room":
                if not(el.visible_boundaries): el.show_boundaries()
            if type(el).__name__ in ["Window", "Door", "Furniture"]:
                el.render_debug_rect()
    else:
        for el in env_group:
            if type(el).__name__ == "Room":
                if el.visible_boundaries: el.hide_boundaries()


def rendering():
    # execution flags
    debug               = False
    show_obstacles      = False
    show_clearance      = True
    show_target         = True
    show_direction      = True
    show_forces         = True   # show forces from APF method
    extra_HUD           = False
    test_clearance      = False
    test_motion         = False


    # initialize the pygame engine, get main display object and clock for the rendering
    screen, clock = initialization()
    # create display objects for the UI
    ui_group, text_boxes = create_UI(screen)
    # create display objects for the simulation
    env_group, extra_HUD_group, pepper = create_environment(screen, text_boxes[1])

    pepper.y  += 250

    # custom event raiser every x milliseconds for testing
    test_time_interval   = 2500  # [ms]
    motion_time_interval = 100 # [ms]
    pg.time.set_timer( pg.USEREVENT + 0, test_time_interval)
    pg.time.set_timer(pg.USEREVENT + 1, motion_time_interval) # motion event for each tenth of second


    # variables used for the continuous elimination of characters when pressing backspace
    deleting = None; time_delete = time.time(); deleting_wait = 0.15

    # variable to handle activation of the left mouse button (otherwise i detect generic pg.MOUSEBUTTONDOWN)
    pressed_sx_mouse = False

    # custom object to execute user's inputs
    input_interpreter = InputInterpreter({"UI_DOs": ui_group,"text_boxes": text_boxes, "environment": env_group, "pepper": pepper})

    # frame counter
    counter_frame = 0

    # -------------------------------------------- Main rendering Loop
    while True:

        # for delation animation of the text in the box
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
                # raise SystemExit
                return

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
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
                        if ui_elem.name == 'HUD' and ui_elem.status == 'on':
                            extra_HUD = True
                        elif ui_elem.name == 'HUD' and ui_elem.status == 'off':
                            extra_HUD = False

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
                                    box.restore_default()

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
                            print("Text inserted: {}".format(box.text_box))
                            input_interpreter.execute(box.text_box)
                            # box.box_active = False
                            box.restore_empty()

                        elif event.unicode.isprintable(): # insert unicode chars in the prompt
                            deleting = None
                            box.text_box += event.unicode

                        deleting_wait = 0.15  # reset the velocity when deleting characters from the prompt

            if event.type == pg.KEYUP:
                if event.key == pg.K_BACKSPACE: deleting = None



        # ---------------------------------------- Input Interpreter updates

            # periodic custom event
            if test_clearance and event.type == pg.USEREVENT + 0:
                print("---------------------------------ao")
                pepper.set_random_room_position()
                pepper.compute_clearance()

            # motion custom event
            if  event.type == pg.USEREVENT + 1:
                if pepper.in_motion: pepper.move()


        # update flags based on input
        debug           = input_interpreter.toggle_debug(debug)
        show_obstacles  = input_interpreter.toggle_show_obstacles(show_obstacles)
        test_clearance  = input_interpreter.toggle_test_clearance(test_clearance)
        test_motion     = input_interpreter.toggle_test_motion(test_motion)
        show_clearance  = input_interpreter.toggle_clearance(show_clearance)
        show_target     = input_interpreter.toggle_target(show_target)
        show_direction  = input_interpreter.toggle_direction(show_direction)
        show_forces     = input_interpreter.toggle_forces(show_forces)

        # update flags for pepper
        pepper.show_clearance   = show_clearance
        pepper.show_target      = show_target
        pepper.show_direction   = show_direction
        pepper.show_forces = show_forces

        if test_motion:
            pepper.move2Door("west")
            # pepper.move2Win("east", "right")
            # pepper.move2pos(pg.math.Vector2(pepper.x +40, pepper.y +180))
            test_motion = False


        # handle reset
        if input_interpreter.reset:   # the reset is better to be handled directly in the main loop
            # free memory
            gc.collect()

            # remove old groups
            del env_group; del extra_HUD_group; del ui_group; del text_boxes; del pepper

            # create groups from beginning
            ui_group, text_boxes = create_UI(screen)
            env_group, extra_HUD_group, pepper = create_environment(screen, text_boxes[1])
            pepper.y += 250
            # output message
            text_boxes[1].add_message("The Environment has been reset")

            # restore default value for input interpreter
            input_interpreter = InputInterpreter({"UI_DOs": ui_group,"text_boxes": text_boxes, "environment": env_group, "pepper": pepper})

        # ---------------------------------------- Logical updates
        ui_group.update()
        env_group.update()

        # ---------------------------------------- Render graphics
        # fill the background
        screen.fill((255, 255, 255))

        # rendering UI

        for ui_elem in ui_group:                      #  alternatively: ui_group.draw(screen)
            ui_elem.draw()

        for text_box in text_boxes:
            text_box.draw()

        # rendering House environment
        for env_elem in env_group:                    #  alternatively: env_group.draw(screen)
            env_elem.draw()

        # debug elements rendering
        debug_render(env_group, debug, show_obstacles)

        # extra HUD rendering
        if extra_HUD: extra_HUD_group.draw(screen)

        # ---------------------------------------- display updates

        # update the screen with the current state of the display objects
        pg.display.flip()

        # use current selected FPS property for the rendering
        clock.tick(FPS)

        # update counter frames
        counter_frame += 1

        # time.sleep(6)  #synchronous waiting and exit
        # break


def main():
    start_time = time.time()
    rendering()
    rendering_time = time.time() - start_time
    print("Rendering time {} [s]".format(round(rendering_time, 3)))
    sys.exit(0)

if __name__ == '__main__':
    print(f"Pygame version: {pg.__version__}")
    main()

