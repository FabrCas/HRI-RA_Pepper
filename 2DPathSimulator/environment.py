import pygame as pg
from pygame import Surface
import math
import threading
from display_objects import StaticImage, Text,  InputTextBox, Button, OutputTextBox, Room

def create_UI(screen: Surface):
    # create collections
    ui_group = pg.sprite.Group()
    text_boxes = []  # text boxes are handled differently since are custom objects that don't inherit pygame classes

    # print(screen.get_width(), screen.get_height())

    # 1) create lateral panel and title
    # ltc -> left top corner
    lateral_panel_ltc_x = math.ceil(screen.get_width()*3/4)
    lateral_panel_ltc_y = 0
    lateral_panel_width = math.ceil(screen.get_width()/4)
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
    prompt    = InputTextBox(screen, x=lateral_panel_ltc_x + 110, y=85, height= 30,
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



def create_environment(screen: Surface):
    # create environment group
    env_group = pg.sprite.Group()

    # create extra hud group
    extra_hud_group = pg.sprite.Group()

    # create background garden + outdoor exit sidewalk
    env_ltc_x = 0
    env_ltc_y = 0
    env_width = math.ceil(screen.get_width()*3/4)
    env_height = screen.get_height()

    bg_garden_t = StaticImage('static/garden.jpg', env_ltc_x,env_ltc_y, env_width,
                               math.ceil(env_height / 2))

    bg_garden_d = StaticImage('static/garden.jpg', env_ltc_x, math.ceil(env_height / 2), env_width,
                               math.ceil(env_height / 2))
    bg_garden_d.image = pg.transform.flip(bg_garden_d.image, False, True)

    #todo - exit outdoor sidewalk using outdoor class


    env_group.add(bg_garden_t)
    env_group.add(bg_garden_d)

    # create the House Room

    living_room = Room('Living Room', screen, 300,300,200,400, tile_type='parquet')
    living_room.rotate(270)
    print(living_room.get_vertices())
    env_group.add(living_room)
    # extra_hud_group.add(living_room.get_display_name())


    return env_group, extra_hud_group