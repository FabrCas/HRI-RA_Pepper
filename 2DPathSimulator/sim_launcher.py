import pygame as pg
import time
import os
import gc
import sys
import math
import threading

# custom components
from environment import create_UI, create_environment
from services import InputInterpreter, HouseSimulatorSocket
# from display_objects import get_furniture

# Definition of constants as default values
WIDTH_WIN = 1920; HEIGHT_WIN = 1080
X_WIN = 0; Y_WIN = 0
FPS = 60
XC_WIN = lambda: math.ceil(WIDTH_WIN/2); YC_WIN = lambda: math.ceil(HEIGHT_WIN/2)
os_systems = ['linux', 'windows']; os_selected = os_systems[0]

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
    # change default folder position for the path, from .EAI2  to ./EAI2/2DPathSimulator

    if os_selected == 'linux' and not ('2DPathSimulator' in os.getcwd()):
        os.chdir('./2DPathSimulator')
        
    print(os.getcwd())
    
    
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
    
    # execution flags at beginning
    # reset               = False
    debug               = False
    show_obstacles      = False
    show_clearance      = True
    show_target         = True
    show_direction      = True
    show_forces         = True   # show forces from APF method
    extra_HUD           = False
    test_clearance      = False
    test_motion         = False
    test_grab           = False
    test_oc             = False
    test_p              = False
    test_message        = False


    # initialize the pygame engine, get main display object and clock for the rendering
    screen, clock = initialization()
    # create display objects for the UI
    ui_group, text_boxes = create_UI(screen)
    # create display objects for the simulation
    env_group, extra_HUD_group, pepper = create_environment(screen, text_boxes[1])


    # edit starting position for pepper, from the center of the foyer
    # pepper.y  -= 250
    pepper.set_Ypos(pepper.y - 200)

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

    # custom socket for handling client/server communication between simualtors
    sim_socket = HouseSimulatorSocket(input_interpreter, pepper)    # auto exe of listening function

    # use sim socket to request command for the other simulator
    
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
                        if ui_elem.name == "sleep":
                            sim_socket.send_command("sleep "+ ui_elem.status)
                        elif ui_elem.name == "microphone":
                            sim_socket.send_command("microphone "+ ui_elem.status)
                            
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
                pepper.set_random_room_position()
                pepper.compute_clearance()

            # motion custom event
            if  event.type == pg.USEREVENT + 1:
                if pepper.in_motion and not(pepper.direction is None): pepper.move()


        # update flags based on input
        #reset           = input_interpreter.toggle_reset()
        debug           = input_interpreter.toggle_debug(debug)
        show_obstacles  = input_interpreter.toggle_show_obstacles(show_obstacles)
        test_clearance  = input_interpreter.toggle_test_clearance(test_clearance)
        test_motion     = input_interpreter.toggle_test_motion(test_motion)
        test_grab       = input_interpreter.toggle_test_grab(test_grab)
        test_oc         = input_interpreter.toggle_test_open_close(test_oc)
        test_p          = input_interpreter.toggle_test_plan(test_p)
        test_message    = input_interpreter.toggle_test_message(test_message)
        show_clearance  = input_interpreter.toggle_clearance(show_clearance)
        show_target     = input_interpreter.toggle_target(show_target)
        show_direction  = input_interpreter.toggle_direction(show_direction)
        show_forces     = input_interpreter.toggle_forces(show_forces)

        # update flags for pepper
        pepper.show_clearance   = show_clearance
        pepper.show_target      = show_target
        pepper.show_direction   = show_direction
        pepper.show_forces      = show_forces

        if test_grab:
            timer1 = threading.Timer(2, lambda: pepper.grab("smartphone"))
            timer2 = threading.Timer(6, lambda: pepper.place("desk_studio"))
            timer1.start()
            timer2.start()
            test_grab = False
            
        if test_oc:
            # take doors and windows in the room where pepper is located
            doors  = pepper.actual_room.doors
            # windows = pepper.actual_room.windows
            print(doors)

            
            door_name = "d_foyer_outdoor"
            win_namel = "wl_foyer"
            win_namer = "wr_foyer"
            
            # define timers
            timer1 = threading.Timer(1, lambda: pepper.openDoor(door_name))
            timer2 = threading.Timer(4, lambda: pepper.closeDoor(door_name))
            timer3 = threading.Timer(0.5, lambda: pepper.openWin(win_namel))
            timer4 = threading.Timer(1, lambda: pepper.openWin(win_namer))
            timer5 = threading.Timer(1.5, lambda: pepper.closeWin(win_namel))
            timer6 = threading.Timer(2, lambda: pepper.closeWin(win_namer))
            
            # start timers 
            timer1.start()
            timer2.start()
            timer3.start()
            timer4.start()
            timer5.start()
            timer6.start()
            test_oc = False
            
        if test_motion:
            type_test = "mix2"  # types: "free", "door" "win", "furniture", "free_space", "mix", "mix2"
            
            if type_test == "free":
                pos = pg.math.Vector2(pepper.x + 50, pepper.y -100)
                pepper.move2pos(pos)
            
            elif type_test == "door":
                name_door = "d_foyer_living"
                pepper.move2Door(name_door)
            
            elif type_test == "win":
                name_win = "wr_foyer"
                pepper.move2Win(name_win)
            
            elif type_test == "free_space":
                pepper.move2FreeSpace("foyer")
                
            elif type_test == "furniture":
                pepper.move2Furniture("sofa")
                
            if type_test == "mix":
                tasks = ["door", "win", "free"]

                def mix_task():
                    while True:
                        if not(pepper.in_motion):
                            if tasks == []: break
                            
                            if tasks[0] == "free":
                                pepper.move2FreeSpace("foyer")
                                tasks.pop(0)
                            elif tasks[0] == "door":
                                name_door = "d_foyer_living"
                                pepper.move2Door(name_door)
                                tasks.pop(0)
                            elif tasks[0] == "win":
                                name_win = "wl_foyer"
                                pepper.move2Win(name_win)
                                tasks.pop(0)
                                
                listener_thread = threading.Thread(target = mix_task)
                listener_thread.daemon = False
                listener_thread.start()

            if type_test == "mix2":
                tasks = ["door", "room", "furniture", "free_space"]

                def mix_task():
                    while True:
                        if not(pepper.in_motion):
                            if tasks == []: break
                            
                            if tasks[0] == "room":
                                pepper.move2Room(room_name="living_room", direction="west")
                                tasks.pop(0)
                            elif tasks[0] == "door":
                                name_door = "d_foyer_living"
                                pepper.move2Door(name_door)
                                tasks.pop(0)
                            elif tasks[0] == "furniture":
                                pepper.move2Furniture(target_name="sofa")
                                tasks.pop(0)
                            elif tasks[0] == "free_space":
                                pepper.move2FreeSpace()
                                tasks.pop(0)
                                
                listener_thread = threading.Thread(target = mix_task)
                listener_thread.daemon = False
                listener_thread.start()
            
                        

            test_motion = False

        if test_p:
            print("test plan on")
            sim_socket.test_plan()
            test_p = False
        
        if test_message:
            sim_socket.send_command("ao")
            test_message =False 
        # handle reset
        if input_interpreter.changed_reset:   # the reset is better to be handled directly in the main loop

            # remove old groups
            del env_group; del extra_HUD_group; del ui_group; del text_boxes; del pepper
            del input_interpreter
            
            # create groups from beginning
            ui_group, text_boxes = create_UI(screen)
            env_group, extra_HUD_group, pepper = create_environment(screen, text_boxes[1])
            pepper.set_Ypos(pepper.y - 200)
            # output message
            text_boxes[1].add_message("The Environment has been reset")

            
            # restore default value for input interpreter
            input_interpreter = InputInterpreter({"UI_DOs": ui_group,"text_boxes": text_boxes, "environment": env_group, "pepper": pepper})

            # new socket for the new interpreter
            sim_socket.setInterpreter(input_interpreter)
            
            input_interpreter.changed_reset = False
            
            # free memory
            gc.collect()
        
        
        # sim_socket.exe_commmands()
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

