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

    # 1) Create background garden + outdoor exit sidewalk

    # define dimensions of the environment and top left corner coordinates
    env_ltc_x = 0
    env_ltc_y = 0
    env_width = math.ceil(screen.get_width()*3/4)
    env_height = screen.get_height()

    margin = 50     # margin to be kept from the environment boundary
    wall_size = 10   # distance between contiguous rooms since walls

    print(f"Environment shape -> width:{env_width}, height:{env_height}")

    # garden
    bg_garden_t = StaticImage('static/garden.jpg', screen, env_ltc_x,env_ltc_y, env_width,\
                               math.ceil(env_height / 2))   # static images are defined with top left corner coordinates

    bg_garden_b = StaticImage('static/garden.jpg', screen, env_ltc_x, math.ceil(env_height / 2), env_width,\
                               math.ceil(env_height / 2))
    bg_garden_b.image = pg.transform.flip(bg_garden_b.image, False, True)

    env_group.add(bg_garden_t)  # top garden texture
    env_group.add(bg_garden_b)  # bottom garden texture

    # outdoor sidewalk
    outdoor_w = 150; outdoor_h = 400
    outdoor = Room(name='outdoor', screen= screen, x = env_width - (outdoor_w/2 + margin),\
                   y= env_height - (outdoor_h/2), width=outdoor_w,height= outdoor_h,\
                   env_group=env_group, tile_type='grey')  # rooms are defined using the top center coordinates

    extra_hud_group.add(outdoor.get_display_name(side='bottom'))

    # 2) Create the House Rooms

    # studio
    studio_w = 300; studio_h = 400
    studio = Room(name='Studio', screen= screen, x=margin + (studio_w/2), y= margin + (studio_h/2),\
                  width=studio_w, height=studio_h, env_group= env_group, tile_type='parquet')
    extra_hud_group.add(studio.get_display_name(side='top'))
    studio.add_window("north", displacement= studio_w/2, status='close')
    studio.add_door("east", displacement=studio_h / 2, status='open')


    # north toilet
    toiletNorth_w= 300; toiletNorth_h= 200
    toilet_north = Room(name="Toilet (north)", screen= screen, x= margin + studio_w + wall_size+ toiletNorth_w/2,\
                        y= margin + toiletNorth_h/2, width= toiletNorth_w, height=toiletNorth_h,\
                        env_group= env_group, tile_type='rhombus')
    extra_hud_group.add(toilet_north.get_display_name(side='top', color=(0,0,0)))
    toilet_north.add_window("north", displacement= 150, status= 'close')







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







