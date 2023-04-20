import pygame as pg
from pygame import Surface
import math
import time
import threading
from display_objects import StaticImage, Text,  InputTextBox, Button, OutputTextBox, Room

def create_UI(screen: Surface, verbose = True):

    if verbose: print("\n         [sketching the UI panel]          ")

    # create collections
    ui_group = pg.sprite.Group()
    text_boxes = []  # text boxes are handled differently since are custom objects that don't inherit pygame classes

    # print(screen.get_width(), screen.get_height())

    # 1) create lateral panel and title, ltc -> left top corner
    lateral_panel_ltc_x = math.ceil(screen.get_width()*3/4)
    lateral_panel_ltc_y = 0
    lateral_panel_width = math.ceil(screen.get_width()/4)
    lateral_panel_height = screen.get_height()

    lateral_panel = StaticImage(file_path = "static/lateral_panel.jpg", screen= screen, x= lateral_panel_ltc_x,\
                                 y=lateral_panel_ltc_y, width=lateral_panel_width, height=lateral_panel_height)

    text_control_panel = Text("Control Panel", screen= screen, x= lateral_panel_ltc_x \
                              , y=10,  color=(255, 255, 255), size_font=30)
    text_control_panel.center_to(x = lateral_panel_ltc_x + lateral_panel_width/2)

    ui_group.add(lateral_panel)
    ui_group.add(text_control_panel)

    # 2) create prompt
    text_prompt = Text("Prompt ", screen = screen, x=lateral_panel_ltc_x + 10, y=90, color=(255, 255, 255), size_font=20)
    prompt = InputTextBox(screen, x=lateral_panel_ltc_x + 110, y=85, height= 30,
                               color_text=(0, 0, 0), color_bg=(200,200,200),size_font=20)

    ui_group.add(text_prompt)
    text_boxes.append(prompt)

    # 3) create buttons
    text_sleep  = Text("Sleep mode ", screen = screen, x=lateral_panel_ltc_x + 10, y=170,  color=(255, 255, 255), size_font=20)
    button_sleep = Button("sleep", screen, lateral_panel_ltc_x + lateral_panel_width*3/5, 170 + 15, 60, 60, 'off')

    text_mic  = Text("Microphone ", screen=screen, x=lateral_panel_ltc_x + 10, y=250,  color=(255, 255, 255), size_font=20)
    button_mic = Button("microphone", screen, lateral_panel_ltc_x + lateral_panel_width*3/5, 250 + 15, 60, 60, 'on')

    text_extraHUD = Text("Extra HUD ", screen = screen, x=lateral_panel_ltc_x + 10, y=330,  color=(255, 255, 255), size_font=20)
    button_extraHUD = Button('HUD', screen, lateral_panel_ltc_x + lateral_panel_width*3/5, 330 + 15, 60, 60, 'off')

    ui_group.add(text_sleep)
    ui_group.add(button_sleep)
    ui_group.add(text_mic)
    ui_group.add(button_mic)
    ui_group.add(text_extraHUD)
    ui_group.add(button_extraHUD)

    # 4) create system Output box
    system_box = OutputTextBox(screen, x= lateral_panel_ltc_x + 10, y= lateral_panel_height - 410, width=lateral_panel_width -20, height= 400,
                               color_text=(0, 0, 0), color_bg=(200,200,200),size_font=20)

    text_system_box = Text("System output", screen=screen, x=lateral_panel_ltc_x + 10, y= system_box.y-30,  color=(255, 255, 255), size_font=20)
    text_system_box.center_to(x = lateral_panel_ltc_x + lateral_panel_width/2)

    text_boxes.append(system_box)
    ui_group.add(text_system_box)

    test_messages(system_box, screen)
    return ui_group, text_boxes


def create_environment(screen: Surface, verbose = True):

    if verbose: print("\n         [sketching the House environment]          ")

    # create environment group
    env_group = pg.sprite.Group()

    # create extra hud group
    extra_hud_group = pg.sprite.Group()

    # 1) create background garden + outdoor exit sidewalk
    env_ltc_x = 0
    env_ltc_y = 0
    env_width = math.ceil(screen.get_width()*3/4)
    env_height = screen.get_height()

    bg_garden_t = StaticImage('static/garden.jpg', screen, env_ltc_x,env_ltc_y, env_width,
                               math.ceil(env_height / 2))

    bg_garden_d = StaticImage('static/garden.jpg', screen, env_ltc_x, math.ceil(env_height / 2), env_width,
                               math.ceil(env_height / 2))
    bg_garden_d.image = pg.transform.flip(bg_garden_d.image, False, True)

    #todo - exit outdoor sidewalk using outdoor class


    env_group.add(bg_garden_t)
    env_group.add(bg_garden_d)

    # create the House Rooms

    # 2) living room

    living_room = Room(name='Living Room', screen= screen, x=300, y=300, width=350,\
                       height=400, env_group= env_group, tile_type='parquet')

    extra_hud_group.add(living_room.get_display_name(side='top'))
    living_room.add_window("top",       displacement= 175, status='close')
    living_room.add_window("left",      displacement= 175, status='close')
    living_room.add_window("right",     displacement= 175, status='close')
    living_room.add_window("bottom",    displacement= 175, status='close')

    test_animate_windows(living_room)
    timer = threading.Timer(4, lambda: test_animate_windows(living_room))
    timer.start()





    return env_group, extra_hud_group


# ----------------------------------- test functions -------------------------------------
def test_messages(system_box, screen):
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

    start_time = threading.Timer(3, lambda : system_box.add_message("window width -> {}, window height -> {}".format(str(screen.get_width()), str(screen.get_height()))))
    start_time.start()

def test_animate_windows(room):

    def call_timers(windows, time):
        print(windows)
        print(windows[0].status)
        if windows[0].status == "close":
            t_r = threading.Timer(time, lambda: windows[0].open())
            t_l = threading.Timer(time, lambda: windows[1].open())

        elif windows[0].status == 'open':
            t_r = threading.Timer(time, lambda: windows[0].close())
            t_l = threading.Timer(time, lambda: windows[1].close())

        t_r.start()
        t_l.start()

    # open windows
    call_timers(room.windows['top'],    time=1)
    call_timers(room.windows['left'],   time=2)
    call_timers(room.windows['right'],  time=3)
    call_timers(room.windows['bottom'], time=4)







