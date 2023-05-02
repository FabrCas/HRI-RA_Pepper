import pygame as pg
from pygame import Surface
import math
from random import randint
import threading
from display_objects import StaticImage, Rect, Text, InputTextBox, Button,\
                            OutputTextBox, Room, Pepper, get_rooms

def create_UI(screen: Surface, verbose = True):

    if verbose: print("\n         [sketching the UI panel]          ")

    # create collections
    ui_group = pg.sprite.Group()
    text_boxes = []  # text boxes are handled differently since are custom objects that don't inherit pygame classes

    # 1) create lateral panel and title, ltc -> left top corner
    lateral_panel_ltc_x = math.ceil(screen.get_width()*3/4)
    lateral_panel_ltc_y = 0
    lateral_panel_width = math.ceil(screen.get_width()/4)
    lateral_panel_height = screen.get_height()

    lateral_panel = StaticImage(file_path = "static/texture/lateral_panel.jpg", screen= screen, x= lateral_panel_ltc_x,\
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

    # test_messages(system_box, screen)
    return ui_group, text_boxes

def create_environment(screen: Surface, verbose = True):

    if verbose: print("\n         [sketching the House environment]          ")

    # create environment group
    env_group = pg.sprite.Group()

    # create extra hud group
    extra_hud_group = pg.sprite.Group()

    # 1) Create garden background garden + outdoor exit sidewalk

    # define dimensions of the environment and top left corner coordinates
    env_ltc_x = 0
    env_ltc_y = 0
    env_width = math.ceil(screen.get_width()*3/4)
    env_height = screen.get_height()

    margin = 50     # margin to be kept from the environment boundary
    wall_size = 10   # distance between contiguous rooms since walls

    print(f"Environment shape -> width:{env_width}, height:{env_height}")

    # -- garden
    bg_garden_t = StaticImage('static/texture/garden2.jpg', screen, env_ltc_x,env_ltc_y, env_width,\
                               math.ceil(env_height / 2))   # static images are defined with top left corner coordinates

    bg_garden_b = StaticImage('static/texture/garden2.jpg', screen, env_ltc_x, math.ceil(env_height / 2), env_width,\
                               math.ceil(env_height / 2))
    bg_garden_b.image = pg.transform.flip(bg_garden_b.image, False, True)

    env_group.add(bg_garden_t)  # top garden texture
    env_group.add(bg_garden_b)  # bottom garden texture

    # -- outdoor sidewalk
    outdoor_w = 150; outdoor_h = 400;
    outdoor_x = env_width - (outdoor_w/2 + margin) - wall_size
    outdoor_y = env_height - (outdoor_h/2)

    outdoor_edge = Rect(screen= screen, x = outdoor_x - outdoor_w/2 - wall_size, y= outdoor_y - outdoor_h/2,\
                   width = outdoor_w + wall_size*2,\
                   height= outdoor_h, color= (150,150,150))
    env_group.add(outdoor_edge)

    outdoor = Room(name='Outdoor', screen= screen, x = outdoor_x,\
                   y=outdoor_y, width=outdoor_w, height= outdoor_h,\
                   env_group=env_group, tile_type='grey')  # rooms are defined using the top center coordinates

    extra_hud_group.add(outdoor.get_display_name(side='bottom'))

    # 2.1) create walls (black background behind rooms)

    wall_up = Rect(screen= screen, x = margin - wall_size, y= margin - wall_size,\
                   width = env_width - 2*(margin - wall_size),\
                   height= env_height - (margin - wall_size) - outdoor.height, color= (0,0,0))

    wall_down = Rect(screen= screen, x = margin - wall_size, y= margin - wall_size + wall_up.height,\
                    width = env_width - (2*(margin - wall_size)) - outdoor.width - margin,\
                    height= env_height - wall_up.height - 2*(margin - wall_size), color= (0,0,0))

    env_group.add(wall_up); env_group.add(wall_down)


    # 2.2) Create the House Rooms, windows, and extra HUD text

    # -- studio
    studio_w = 350; studio_h = 350
    studio = Room(name='Studio', screen= screen, x=margin + (studio_w/2), y= margin + (studio_h/2),\
                  width=studio_w, height=studio_h, env_group= env_group, tile_type='parquet')
    extra_hud_group.add(studio.get_display_name(side='top'))
    win = studio.add_window("north", displacement= studio_w/2, status='close')

    timer1 = threading.Timer(1, lambda: win[0].open())
    timer2 = threading.Timer(1, lambda: win[1].open())
    timer1.start()
    timer2.start()

    # -- toilet
    toilet_w= 360; toilet_h= 200
    toilet = Room(name="Toilet", screen= screen, x= margin + studio_w + wall_size+ toilet_w/2,\
                        y= margin + toilet_h/2, width= toilet_w, height=toilet_h,\
                        env_group= env_group, tile_type='rhombus')
    extra_hud_group.add(toilet.get_display_name(side='top', color=(0,0,0)))
    toilet.add_window("north", displacement= toilet_w/2, status= 'open')

    # -- Foyer
    foyer_w = wall_up.width - wall_size*4 - studio_w - toilet_w; foyer_h= wall_up.height -2* wall_size
    foyer = Room(name="Foyer", screen= screen, x= toilet.x + toilet_w/2 + wall_size + foyer_w/2,\
                        y = wall_up.y + foyer_h/2 + wall_size , width= foyer_w,
                        height= foyer_h, env_group= env_group, tile_type='white')
    extra_hud_group.add(foyer.get_display_name(side='top', color=(0, 0, 0)))
    foyer.add_window("east", displacement=300, status='open')

    # -- Living Room
    living_room_w = toilet_w; living_room_h = wall_up.height + wall_down.height - toilet_h -4* wall_size - 300
    living_room = Room(name="Living Room", screen= screen, x= toilet.x,\
                        y = toilet.y + toilet_h/2 + wall_size + living_room_h/2 , width= living_room_w,
                        height= living_room_h, env_group= env_group, tile_type='parquet_strips')
    extra_hud_group.add(living_room.get_display_name(side='bottom', color=(255, 255, 255)))

    # -- Dining
    dining_w = toilet_w; dining_h = 300
    dining = Room(name="Dining", screen= screen, x= toilet.x,\
                        y = living_room.y + living_room_h/2 + wall_size + dining_h/2 , width= dining_w,
                        height= dining_h, env_group= env_group, tile_type='marble')
    extra_hud_group.add(dining.get_display_name(side='top', color=(0, 0, 0)))
    dining.add_window("east", displacement=dining_h/2, status='open')


    # -- Bedroom
    bedroom_w = studio_w; bedroom_h = 300
    bedroom = Room(name="Bedroom", screen= screen, x= studio.x,\
                        y = studio.y + studio_h/2 + wall_size + bedroom_h/2 , width= bedroom_w,
                        height= bedroom_h, env_group= env_group, tile_type='black_marble')
    extra_hud_group.add(bedroom.get_display_name(side='bottom', color=(255, 255, 255)))
    bedroom.add_window("west", displacement=bedroom_h/2, status='open')

    # -- Kitchen
    kitchen_w = studio_w; kitchen_h = wall_up.height + wall_down.height - studio_h - wall_size*4 - bedroom_h
    kitchen = Room(name="Kitchen", screen= screen, x= studio.x,\
                        y = bedroom.y + bedroom_h/2 + wall_size + kitchen_h/2, width= kitchen_w,
                        height= kitchen_h, env_group= env_group, tile_type='ceramic')
    extra_hud_group.add(kitchen.get_display_name(side='bottom', color=(0, 0, 0)))
    wind = kitchen.add_window("south", displacement= math.ceil(kitchen_w * 1/4), status='open')

    timer1 = threading.Timer(1, lambda: wind[0].close())
    timer1.start()


    # 2.2) creates doors (interconnection between rooms)

    # main door: foyer -> outside
    door_f = foyer.add_door(outdoor, status="open", displ=10, is_main=True)

    # foyer -> living room
    foyer.add_door(living_room, status='open', displ=50)

    # toilet -> living room
    toilet.add_door(living_room,  status='open', displ=-120)

    # studio -> living room
    studio.add_door(living_room, status='open', displ=132)

    # bedroom -> living room
    bedroom.add_door(living_room, status='open', displ=-25)

    # living room -> dining
    living_room.add_door(dining, status='open', displ= 0)

    # dining -> kitchen
    door_d = dining.add_door(kitchen, status='close')

    # timer1 = threading.Timer(1, lambda: door_f.close())
    # timer2 = threading.Timer(1, lambda: door_d.open())
    # timer1.start()
    # timer2.start()

    # 3.1) include furniture (fixed)

    #  -- studio
    desk_studio_w = math.ceil(studio_w /3) + 50 ; desk_studio_h = math.ceil(studio_h /4)
    studio.add_furniture("studio desk", "studio_table",x=math.ceil(studio.x - studio.width/2 + desk_studio_w/2),\
                         y=math.ceil(studio.y + studio.height/2 - desk_studio_h/2 - 20), width=desk_studio_w,\
                         height=desk_studio_h, rotation= 180)

    chair_studio_w = 40; chair_studio_h = 40
    studio.add_furniture("studio chair", "studio_chair",x=math.ceil(studio.x - studio.width/2 + + desk_studio_w/2),\
                         y=math.ceil(studio.y + studio.height/2 - chair_studio_h/2) -5, width=chair_studio_w,\
                         height=chair_studio_h, rotation= 180)

    pool_studio_w = 150; pool_studio_h = 150
    studio.add_furniture("studio pool", "pool",x=math.ceil(studio.x - studio.width/2 + pool_studio_w/2 * 3/5) + 50,\
                         y=studio.y -40, width=pool_studio_w,\
                         height=pool_studio_h, rotation= 0)

    plant_w = 50; plant_h = 50
    studio.add_furniture("studio plant sx", "plant_1", x=math.ceil(studio.x - studio.width/2 + plant_w/2),\
                         y= math.ceil(studio.y - studio.height/2 + plant_h/2) , width=plant_w,\
                         height=plant_h, rotation= 0)

    studio.add_furniture("studio plant dx", "plant_1", x=math.ceil(studio.x + studio.width/2 - plant_w/2),\
                         y= math.ceil(studio.y - studio.height/2 + plant_h/2) , width=plant_w,\
                         height=plant_h, rotation= 0, flip_x= True)


    # -- kitchen
    kitchen_furniture_w = kitchen_h; kitchen_furniture_h = math.ceil(kitchen_w/3)
    kitchen.add_furniture("kitchen furniture", "kitchen",x= kitchen.x - math.ceil(kitchen_w/2) + math.ceil(kitchen_furniture_h/2),\
                         y= kitchen.y, width=kitchen_furniture_w,\
                         height= kitchen_furniture_h, rotation= -90)

    kitchen_big_table_w = 120; kitchen_big_table_h = 120
    kitchen.add_furniture("kitchen big table", "big_table",x= kitchen.x + 50,\
                         y= math.ceil(kitchen.y - kitchen_h/2 + kitchen_big_table_h/2 * 3/5), width=kitchen_big_table_w,\
                         height= kitchen_big_table_h, rotation=0)

    kitchen_chair_w = 60; kitchen_chair_h = 60
    kitchen.add_furniture("kitchen chair dx", "chair",x= kitchen.x + 50 + math.ceil(kitchen_big_table_w/2 + kitchen_chair_w/2 *3/5 + 5),\
                         y= math.ceil(kitchen.y - kitchen_h/2 + kitchen_chair_h/2), width=kitchen_chair_w,\
                         height= kitchen_chair_h, rotation=0)
    kitchen.add_furniture("kitchen chair sx", "chair",x= kitchen.x + 50 - math.ceil(kitchen_big_table_w/2 + kitchen_chair_w/2 *3/5 + 5),\
                         y= math.ceil(kitchen.y - kitchen_h/2 + kitchen_chair_h/2), width=kitchen_chair_w,\
                         height= kitchen_chair_h, rotation=0)

    # -- bedroom
    bed_w = math.ceil(bedroom_w/3); bed_h=math.ceil(bedroom_h/2)
    bedroom.add_furniture("bed", "bed",x= bedroom.x,\
                         y= bedroom.y - math.ceil(bedroom_h/2) + math.ceil(bed_h/2), width=bed_w,\
                         height= bed_h, rotation= 0)

    bedroom_tv_w = 100; bedroom_tv_h = 100;
    bedroom.add_furniture("bedroom tv", "tv_off", x= bedroom.x,\
                         y=math.ceil(bedroom.y + bedroom_h/2 - bedroom_tv_h/2 * 2/5),\
                         width=bedroom_tv_w, height=bedroom_tv_h, rotation=180)

    bedroom_cabinet_w = 80; bedroom_cabinet_h = 80
    bedroom.add_furniture("bedroom cabinet dx", "cabinet", x=math.ceil(bedroom.x + bedroom_w/2 - bedroom_cabinet_w/2),\
                         y= math.ceil(bedroom.y + bedroom_h/2 - (bedroom_cabinet_h/2 * 3/5)),\
                         width=bedroom_cabinet_w, height= bedroom_cabinet_h, rotation=180)

    bedroom.add_furniture("bedroom cabinet sx", "cabinet", x=math.ceil(bedroom.x - bedroom_w/2 + bedroom_cabinet_w/2),\
                         y= math.ceil(bedroom.y + bedroom_h/2 - (bedroom_cabinet_h/2 * 3/5)),\
                         width=bedroom_cabinet_w, height= bedroom_cabinet_h, rotation=180, flip_x =True)


    # -- toilet
    toilet_water_w = 50; toilet_water_h = 50
    toilet.add_furniture("water", "toilet_water", x=toilet.x - math.ceil(toilet_w/2) + math.ceil(toilet_water_w/2) + 5,\
                         y= toilet.y - math.ceil(toilet_h/2) + math.ceil(toilet_water_h/2) + 5, width=toilet_water_w,\
                         height= toilet_water_h, rotation= 180)

    toilet_tub_w = 120; toilet_tub_h = 120

    toilet.add_furniture("tub", "tub", x=toilet.x - math.ceil(toilet_w/2) + math.ceil(toilet_tub_w/4),\
                         y= toilet.y + math.ceil(toilet_h/2) - math.ceil(toilet_tub_h/2), width=toilet_tub_w,\
                         height= toilet_tub_h, rotation= 0)

    toilet_sink_w = 70; toilet_sink_h = 70
    toilet.add_furniture("sink", "toilet_sink", x=toilet.x,\
                         y= toilet.y + math.ceil(toilet_h/2) - math.ceil(toilet_sink_h/2 * 3/5),\
                         width=toilet_sink_w, height= toilet_sink_h, rotation=180)

    toilet_cabinet_w = 80; toilet_cabinet_h = 80
    toilet.add_furniture("toilet cabinet", "cabinet", x=toilet.x + math.ceil(toilet_w/2) - math.ceil(toilet_cabinet_h/2 * 3/5) ,\
                         y= toilet.y - math.ceil(toilet_cabinet_w/2) -20,\
                         width=toilet_cabinet_w, height= toilet_cabinet_h, rotation=-90)

    # -- foyer

    foyer.add_furniture("foyer plant sx", "plant_2", x=math.ceil(foyer.x - foyer_w/2 + plant_w/2),\
                         y= math.ceil(foyer.y- foyer_h/2 + plant_h/2), width=plant_w,\
                         height=plant_h, rotation= 0, flip_x= False, flip_y=False)

    foyer.add_furniture("foyer plant dx", "plant_2", x=math.ceil(foyer.x + foyer_w/2 - plant_w/2),\
                         y= math.ceil(foyer.y - foyer_h/2 + plant_h/2), width=plant_w,\
                         height=plant_h, rotation= 0, flip_x= True, flip_y= False)

    # -- living room
    living_room_tv_w = 100; living_room_tv_h = 100
    living_room.add_furniture("living room tv", "tv_on", x= living_room.x,\
                         y= math.ceil(living_room.y - living_room_h/2 + living_room_tv_h/2 * 2/5),\
                         width=living_room_tv_w, height= living_room_tv_h, rotation=0)

    living_room_sofa_w = 130; living_room_sofa_h = 130
    living_room.add_furniture("living room sofa", "sofa", x= living_room.x,\
                         y= living_room.y + 10,\
                         width=living_room_sofa_w, height= living_room_sofa_h, rotation=180)

    small_table_sofa_w = 70; small_table_sofa_h = 70
    living_room.add_furniture("living room small table", "small_table", x= living_room.x,\
                         y=  math.ceil(living_room.y - (living_room_sofa_h/2 * 1/2) - (small_table_sofa_h/2 * 1/2)),\
                         width=small_table_sofa_w, height= small_table_sofa_h, rotation=180)

    armchair_w = 100; armchair_h = 100
    living_room.add_furniture("living room armchair sx", "armchair", x= math.ceil(living_room.x - living_room_sofa_w/2 - armchair_w/2* 1/2) ,\
                         y=  math.ceil(living_room.y - (living_room_sofa_h/2 * 1/2) - (small_table_sofa_h/2 * 1/2)),\
                         width=armchair_w, height= armchair_h, rotation=90)
    living_room.add_furniture("living room armchair dx", "armchair", x= math.ceil(living_room.x + living_room_sofa_w/2 + armchair_w/2* 1/2) ,\
                         y=  math.ceil(living_room.y - (living_room_sofa_h/2 * 1/2) - (small_table_sofa_h/2 * 1/2)),\
                         width=armchair_w, height= armchair_h, rotation= -90)

    living_room.add_furniture("living room plant sx", "plant_2", x=math.ceil(living_room.x - living_room_w/2 + plant_w/2),\
                         y= math.ceil(living_room.y + living_room_h/2 - plant_h/2), width=plant_w,\
                         height=plant_h, rotation= 90)

    living_room.add_furniture("living room plant dx", "plant_2", x=math.ceil(living_room.x + living_room_w/2 - plant_w/2),\
                         y= math.ceil(living_room.y + living_room_h/2 - plant_h/2), width=plant_w,\
                         height=plant_h, rotation= 90, flip_x= True)

    # -- dining
    dining.add_furniture("dining chair top", "chair",x= dining.x,\
                         y= dining.y - 70, width=kitchen_chair_w,\
                         height= kitchen_chair_h, rotation=0)

    dining.add_furniture("dining chair right", "chair",x= dining.x + 80,\
                         y= dining.y, width=kitchen_chair_w,\
                         height= kitchen_chair_h, rotation=-90)

    dining.add_furniture("dining chair left", "chair",x= dining.x - 70,\
                         y= dining.y, width=kitchen_chair_w,\
                         height= kitchen_chair_h, rotation=+90)

    dining.add_furniture("dining chair bottom", "chair",x= dining.x + 20,\
                         y= dining.y + 60, width=kitchen_chair_w,\
                         height= kitchen_chair_h, rotation=180)

    dining_table_w = 140; dining_table_h = 140;
    dining.add_furniture("dining table", "big_table", x= dining.x,\
                         y= dining.y,\
                         width=dining_table_w, height= dining_table_h, rotation=0)

    # 3.2) include furniture (movable)

    # -- studio
    pens_w  = 25; pens_h = 25
    studio.add_furniture("green marker", "green_marker",x=math.ceil(studio.x - studio.width/2 + desk_studio_w/2)- 75,\
                         y=math.ceil(studio.y + studio.height/2 - desk_studio_h/2 - 20)-30, width=pens_w,\
                         height=pens_h, rotation= 180)

    studio.add_furniture("pen", "pen",x=math.ceil(studio.x - studio.width/2 + desk_studio_w/2) -70,\
                         y=math.ceil(studio.y + studio.height/2 - desk_studio_h/2 - 20)-30, width=pens_w,\
                         height=pens_h, rotation= 180)

    studio.add_furniture("pencil", "pencil",x=math.ceil(studio.x - studio.width/2 + desk_studio_w/2) -65,\
                         y=math.ceil(studio.y + studio.height/2 - desk_studio_h/2 - 20) -30, width=pens_w,\
                         height=pens_h, rotation= 180)

    # -- kitchen
    plate_w = 25; plate_h = 25
    kitchen.add_furniture("plate empty", "plate", x= kitchen.x - math.ceil(kitchen_w/2) + math.ceil(kitchen_furniture_h/2) + 20,\
                         y= kitchen.y + 25, width= plate_w,\
                         height= plate_h, rotation=0)
    cup_w = 15; cup_h=15
    kitchen.add_furniture("cup coffee", "coffee", x= kitchen.x - math.ceil(kitchen_w/2) + math.ceil(kitchen_furniture_h/2) + 20,\
                         y= kitchen.y + 50, width= cup_w,\
                         height= cup_h, rotation=0)

    kitchen.add_furniture("plate oranges", "plate",x= kitchen.x + 75,\
                         y= math.ceil(kitchen.y - kitchen_h/2 + kitchen_big_table_h/2 * 3/5) + 20, width=plate_w,\
                         height= plate_h, rotation=0)

    kitchen.add_furniture("plate apples", "plate",x= kitchen.x + 25,\
                         y= math.ceil(kitchen.y - kitchen_h/2 + kitchen_big_table_h/2 * 3/5) + 20, width=plate_w,\
                         height= plate_h, rotation=0)

    orange_w = 10; orange_h = 10

    kitchen.add_furniture("orange", "orange",x= kitchen.x + 80,\
                         y= math.ceil(kitchen.y - kitchen_h/2 + kitchen_big_table_h/2 * 3/5) + 25, width=orange_w,\
                         height= orange_h, rotation=0)
    kitchen.add_furniture("orange", "orange",x= kitchen.x + 70,\
                         y= math.ceil(kitchen.y - kitchen_h/2 + kitchen_big_table_h/2 * 3/5) + 25, width=orange_w,\
                         height= orange_h, rotation=0)
    kitchen.add_furniture("orange", "orange",x= kitchen.x + 75,\
                         y= math.ceil(kitchen.y - kitchen_h/2 + kitchen_big_table_h/2 * 3/5) + 15, width=orange_w,\
                         height= orange_h, rotation=0)

    apple_w = 10; apple_h = 10
    kitchen.add_furniture("apple", "apple",x= kitchen.x + 30,\
                         y= math.ceil(kitchen.y - kitchen_h/2 + kitchen_big_table_h/2 * 3/5) + 25, width=apple_w,\
                         height= apple_h, rotation=0)
    kitchen.add_furniture("apple", "apple",x= kitchen.x + 20,\
                         y= math.ceil(kitchen.y - kitchen_h/2 + kitchen_big_table_h/2 * 3/5) + 25, width=apple_w,\
                         height= apple_h, rotation=0)


    # -- bedroom
    smartphone_w = 15; smartphone_h = 15
    bedroom.add_furniture("smartphone", "smartphone",x= bedroom.x + 45,\
                         y= bedroom.y - math.ceil(bedroom_h/2) + math.ceil(bed_h/2) + 5, width=smartphone_w,\
                         height= smartphone_h, rotation= 0)

    notebook_w = 25; notebook_h = 25
    bedroom.add_furniture("red notebook", "notebook_red", x= math.ceil(bedroom.x - bedroom_w/2 + bedroom_cabinet_w/2) + 20,\
                         y= math.ceil(bedroom.y + bedroom_h/2 - (bedroom_cabinet_h/2 * 3/5)) + 5,\
                         width=notebook_w, height= notebook_h, rotation=180)

    bedroom.add_furniture("green notebook", "notebook_green", x= math.ceil(bedroom.x + bedroom_w/2 - bedroom_cabinet_w/2) + 20,\
                         y= math.ceil(bedroom.y + bedroom_h/2 - (bedroom_cabinet_h/2 * 3/5)) + 5,\
                         width=notebook_w, height= notebook_h, rotation=180)

    # -- toilet
    glasses_w = 25; glasses_h = 25
    toilet.add_furniture("glasses", "glasses", x= math.ceil(toilet.x + toilet_sink_w/2 - glasses_w/2),\
                         y= toilet.y + math.ceil(toilet_h/2 - toilet_sink_h/2 * 3/5 + 15),\
                         width=glasses_w, height= glasses_h, rotation=180)

    toilet.add_furniture("yellow notebook", "notebook_yellow", x=toilet.x + math.ceil(toilet_w/2) - math.ceil(toilet_cabinet_h/2 * 3/5) +5,\
                         y= toilet.y - math.ceil(toilet_cabinet_w/2) + 2,\
                         width=notebook_w, height= notebook_h, rotation=-90)


    # -- living room
    cards_sofa_w = 25; cards_sofa_h = 25
    living_room.add_furniture("cards", "cards", x= living_room.x + 20,\
                         y=  math.ceil(living_room.y - (living_room_sofa_h/2 * 1/2) - (small_table_sofa_h/2 * 1/2)) -10,\
                         width=cards_sofa_w, height= cards_sofa_h, rotation=180)

    # -- dining
    dining.add_furniture("pink notebook", "notebook_pink", x= dining.x + 55,\
                         y= dining.y - 30,\
                         width=notebook_w, height= notebook_h, rotation=0)

    # 4) Create pepper placeholder

    random_room = foyer
    pepper_displ_x = 0 ; pepper_displ_y = 0 # pepper_displ_x = 0; pepper_displ_y = -math.ceil(foyer.height/2) + 80
    pepper = Pepper(screen, env_group, random_room, pepper_displ_x, pepper_displ_y)
    pepper.compute_clearance()
    extra_hud_group.add(pepper.get_logo())

    return env_group, extra_hud_group, pepper

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




# -- test_room
# test_w = 300; test_h = 200
# test_roomN = Room(name="Test nord", screen=screen, x= studio.x -99, \
#                     y= studio.y - studio.height/2 - wall_size - test_h/2 , width=test_w, height=test_h, \
#                     env_group=env_group)

# test_roomS = Room(name="Test sud", screen=screen, x= studio.x + 99, \
#                     y= studio.y + studio.height/2 + wall_size + test_h/2 , width=test_w, height=test_h, \
#                     env_group=env_group)


# test_roomW = Room(name="Test west", screen=screen, x= studio.x - studio.width/2 - wall_size - test_w/2, \
#                     y= studio.y, width=test_w, height=test_h, \
#                     env_group=env_group)

# test_roomE = Room(name="Test east", screen=screen, x= studio.x + studio.width/2 + wall_size + test_w/2, \
#                     y= studio.y, width=test_w, height=test_h, \
#                     env_group=env_group)


# test_doorN = test_roomN.add_door(studio, status='close')
# timer2 = threading.Timer(1, lambda : test_doorN.open())
# timer2.start()

# test_doorS = test_roomS.add_door(studio, status='close')
# timer3 = threading.Timer(1, lambda : test_doorS.open())
# timer3.start()

# test_doorW = test_roomW.add_door(studio, status='close')
# timer4 = threading.Timer(1, lambda : test_doorW.open())
# timer4.start()
#
# test_doorE = test_roomE.add_door(studio, status='close')

