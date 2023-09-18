import pygame as pg
import random
import math
import os
import threading
import time
from copy import deepcopy
import json             # used to serialize string to array/dict and the opposite
from planner import ParserPDDL, SolverFF

class InputInterpreter(object):
    def __init__(self, simulation_objects):
        super().__init__()
        self.ui = simulation_objects['UI_DOs']
        self.boxes = simulation_objects['text_boxes']
        self.env = simulation_objects['environment']
        self.pepper = simulation_objects['pepper']
        
        self.changed_reset              = False
        self.changed_debug              = False
        self.changed_test_clearance     = False
        self.changed_test_grab          = False
        self.changed_test_motion        = False
        self.changed_test_open_close    = False
        self.changed_test_plan          = False
        self.changed_test_message       = False
        self.changed_show_obstacles     = False
        self.changed_show_clearance     = False
        self.changed_show_direction     = False
        self.changed_show_forces        = False
        self.changed_show_target        = False
        self.auto_run()
        

    def auto_run(self):
        pass

        
    def execute(self, message):
        # set boolean flag for change based on input to True

        if "daje roma" in message.strip().lower():
            daje_roma = pg.mixer.Sound('static/sounds/daje_roma_daje.mp3')
            pg.mixer.Sound.play(daje_roma)
        if "reset" in message.strip().lower():
            print("Resetting the environment...")
            self.changed_reset = True
            print(self.changed_reset)
        if "debug" in message.strip().lower():
            print("Changing the debug mode...")
            self.changed_debug = True
        if "obs" in message.strip().lower():
            print("Changing the show obstacles mode...")
            self.changed_show_obstacles = True
        if "test_c" in message.strip().lower():   # test clearance
            print("Started the clearance test")
            self.changed_test_clearance = True
        if "test_m" in message.strip().lower():   # test motion
            print("Started the motion test")
            self.changed_test_motion = True
        if "test_g" in message.strip().lower():   # test grab/place
            print("Started the grab test on smartphone")
            self.changed_test_grab = True
        if "test_o" in message.strip().lower():   # test open/close
            print("Started the open/close test on door and windows")
            self.changed_test_open_close = True
        if "test_p" in message.strip().lower():   # test planning
            print("Started the planning test")
            self.changed_test_plan = True
        if "message" in message.strip().lower():
            print("Sending a message to the docker environment")
            self.changed_test_message = True
        if "clearance" in message.strip().lower():   # clearance
            print("Changing the show of clearance...")
            self.changed_show_clearance = True
        if "target" in message.strip().lower():   # clearance
            print("Changing the show of target...")
            self.changed_show_target = True
        if "direction" in message.strip().lower():   # clearance
            print("Changing the show of direction...")
            self.changed_show_direction = True
        if "forces" in message.strip().lower():
            print("Changing the show of forces (APF)...")
            self.changed_show_forces = True
        if "commands" in message.strip().lower() or 'help' in message.strip().lower():
            print("showing the command list in the console...")
            self.show_commands()
    
    
    def show_commands(self):
        
        command_map = {
            'reset'     :'Reset simulation',
            'debug'     :'toggle debug mode',
            'obs'       :'toggle obstacle mode',
            'test_c'    :'start the clearance test',
            'test_m'    :'start the motion test',
            'test_g'    :'start the grab test',
            'test_o'    :'start the open/close test',
            'test_p'    :'start planning test',
            'clerance'  :'show neearest point',
            'target'    :'show target of the motion',
            'direction' :"show motion's direction",
            'forces'    :'toggle forces visibility ',
        }
        
        self.boxes[1].add_message("List of available commands:")
        for command, description in command_map.items():
            self.boxes[1].add_message(f"> {command}: {description}")
        
        
    # ---- toggle functions
    
    def toggle_reset(self):
        
        if self.changed_reset:
            reset  = True
            print(f"------------------------------- {reset} -------------------------")
        else:
            reset  = False
        
        # restore default value for input interpreter
        self.changed_reset = False
            

        return reset
    
    
    def toggle_debug(self, debug):
        if self.changed_debug:

            # change value
            if debug: debug = False
            else: debug = True

            # restore default value for input interpreter
            self.changed_debug = False

            # output message
            self.boxes[1].add_message(f"Debug mode: {debug}")

        return debug

    def toggle_show_obstacles(self, show_obstacles):
        if self.changed_show_obstacles:

            # change value
            if show_obstacles: show_obstacles = False
            else: show_obstacles = True

            # restore default value for input interpreter
            self.changed_show_obstacles = False

            # output message
            self.boxes[1].add_message(f"Show obstacles mode: {show_obstacles}")

        return show_obstacles

    def toggle_test_clearance(self, test_clearance):
        if self.changed_test_clearance:

            # change value
            if test_clearance:test_clearance = False;
            else: test_clearance = True

            # restore default value for input interpreter
            self.changed_test_clearance = False

            # output message
            self.boxes[1].add_message(f"Test clearance: {test_clearance}")

        return test_clearance
    
    def toggle_test_grab(self, test_grab):
        if self.changed_test_grab:

            # change value
            if test_grab:test_grab = False;
            else: test_grab = True

            # restore default value for input interpreter
            self.changed_test_grab = False

            # output message
            self.boxes[1].add_message(f"Test grab: {test_grab}")

        return test_grab
    
    def toggle_test_open_close(self, test_oc):
        if self.changed_test_open_close:

            # change value
            if test_oc:test_oc = False;
            else: test_oc = True

            # restore default value for input interpreter
            self.changed_test_open_close = False

            # output message
            self.boxes[1].add_message(f"Test open/close: {test_oc}")

        return test_oc
    
    def toggle_test_plan(self, test_p):
        if self.changed_test_plan:

            # change value
            if test_p:test_p = False;
            else: test_p = True

            # restore default value for input interpreter
            self.changed_test_plan = False

            # output message
            self.boxes[1].add_message(f"Test plan: {test_p}")

        return test_p

    def toggle_clearance(self, show_clearance):
        if self.changed_show_clearance:

            # change value
            if show_clearance:show_clearance = False
            else:show_clearance = True

            # restore default value for input interpreter
            self.changed_show_clearance = False

            # output message
            self.boxes[1].add_message(f"Show clearance: {show_clearance}")

        return show_clearance

    def toggle_test_message(self, test_message):
        if self.changed_test_message:

            # change value
            if test_message:test_message = False
            else:test_message = True

            # restore default value for input interpreter
            self.changed_test_message = False
            
        return test_message

    def toggle_target(self, show_target):
        if self.changed_show_target:

            # change value
            if show_target:show_target = False
            else:show_target = True

            # restore default value for input interpreter
            self.changed_show_target = False

            # output message
            self.boxes[1].add_message(f"Show target: {show_target}")

        return show_target

    def toggle_direction(self, show_direction):
        if self.changed_show_direction:

            # change value
            if show_direction:show_direction = False
            else:show_direction = True

            # restore default value for input interpreter
            self.changed_show_direction = False

            # output message
            self.boxes[1].add_message(f"Show direction: {show_direction}")

        return show_direction

    def toggle_forces(self, show_forces):
        if self.changed_show_forces:

            # change value
            if show_forces:show_forces = False
            else:show_forces = True

            # restore default value for input interpreter
            self.changed_show_forces = False

            # output message
            self.boxes[1].add_message(f"Show forces: {show_forces}")

        return show_forces

    def toggle_test_motion(self, test_motion):
        if self.changed_test_motion:

            # change value
            if test_motion:test_motion = False;
            else: test_motion = True

            # restore default value for input interpreter
            self.changed_test_motion = False

            # output message
            self.boxes[1].add_message(f"Test motion: {test_motion}")

        return test_motion


class PepperMotion(object):
    def __init__(self, pepper):
        super().__init__()
        self.pepper = pepper

        # APF variables
        self.apf_not_switched = True    # to show message when change profile in mixed configuration
        self.last_apf = {}              # to print force vectors
        self.last_positions = [pg.math.Vector2(self.pepper.x, self.pepper.y)]       # to activate vortex heuristic
        self.verse = 0
        self.saved_vortex = None

    def reset_motion_variables(self):
        self.apf_not_switched = True
        self.last_apf = {}
        self.last_positions = [pg.math.Vector2(self.pepper.x, self.pepper.y)]       # last 2 positions
        self.verse = 0
        self.saved_vortex = None

    def in_rect(self, rect: pg.Rect, pos: pg.math.Vector2):
        """
        :param rect: rect shape for the control (pg.Rect)
        :param pos: point to the check (pg.math.Vector2)
        :return: boolean variable that represent if a point is in a rect (bounds included)
        """
        if pos.x < rect.x or pos.x > rect.x + rect.width:
            return False
        elif pos.y < rect.y or pos.y > rect.y + rect.height:
            return False
        else:
            return True

    def euclidean_distance(self, v1, v2):
        """
        :param v1: first 2D vector
        :param v2: Second 2D vector
        :return: euclidean distance between the 2 vectors
        """
        return math.sqrt((v1.x - v2.x)**2 + (v1.y - v2.y)**2)

    def random_position(screen, width, height, margin=20):
        x_r = random.randint(0 + margin, width  - margin)
        y_r = random.randint(0 + margin, height - margin)
        return x_r, y_r

    # APF
    def _clearance_walls(self):
        walls = self.pepper.actual_room.bounds
        v1 = pg.math.Vector2(int(self.pepper.x), int(self.pepper.y))
        min_distance = math.inf
        point_min_distance = None

        for side, segments in walls.items():
            for segment in segments:
                points = []
                if side == "north":
                    xs = range(int(segment[0].x), int(segment[1].x)+1)    # compute variable xs
                    points = list(zip(xs, [int(segment[0].y)]*len(xs)))
                elif side == "south":
                    xs = range(int(segment[0].x), int(segment[1].x)+1)    # compute variable xs
                    points = list(zip(xs, [int(segment[0].y)] * len(xs)))
                elif side == "east":
                    ys = range(int(segment[0].y), int(segment[1].y)+1)    # compute variable ys
                    points = list(zip([int(segment[0].x)] * len(ys), ys))
                elif side == "west":
                    ys = range(int(segment[0].y), int(segment[1].y)+1)    # compute variable ys
                    points = list(zip([int(segment[0].x)] * len(ys), ys))

                for point in points:
                    v2 = pg.math.Vector2(point[0], point[1])
                    dis = self.euclidean_distance(v1, v2)
                    if dis < min_distance:
                        min_distance = dis
                        point_min_distance = v2

        return point_min_distance, min_distance

    def _clearance_obstacles(self):

        # the pepper position as reference for the euclidean distance
        v1 = pg.math.Vector2(int(self.pepper.x), int(self.pepper.y))

        # initialize variables of the distances
        min_distance = math.inf
        point_min_distance = None

        # lists of obstacles elements
        windows =   list(self.pepper.actual_room.windows.values())
        doors =     list(self.pepper.actual_room.doors.values())
        all_furniture = list(self.pepper.actual_room.furniture.values())

        # full set of points for the distance
        points_window = []
        points_door = []
        points_furniture = []

        # windows points
        for win in windows:
            try:
                win_left_rect = win[0].rect_gfx.rect
                win_right_rect = win[1].rect_gfx.rect
            except:
                break

            # compute the points relative to the edge for the left window
            xs = list(range(win_left_rect.left, win_left_rect.right))
            ys = list(range(win_left_rect.top, win_left_rect.bottom))

            top_points_l    = list(zip(xs, [win_left_rect.top] * len(xs)))
            left_points_l   = list(zip([win_left_rect.left] * len(ys), ys))
            right_points_l  = list(zip([win_left_rect.right] * len(ys), ys))
            bottom_points_l = list(zip(xs, [win_left_rect.bottom] * len(xs)))

            # compute the points relative to the edge for the right window
            xs = list(range(win_right_rect.left, win_right_rect.right))
            ys = list(range(win_right_rect.top, win_right_rect.bottom))

            top_points_r = list(zip(xs, [win_right_rect.top] * len(xs)))
            left_points_r = list(zip([win_right_rect.left] * len(ys), ys))
            right_points_r = list(zip([win_right_rect.right] * len(ys), ys))
            bottom_points_r = list(zip(xs, [win_right_rect.bottom] * len(xs)))


            points_window = [*points_window, *top_points_l, *left_points_l, *right_points_l, *bottom_points_l, \
                      *top_points_r, *left_points_r, *right_points_r, *bottom_points_r]

        # door points
        for door in doors:
            rect_door = door.rect_gfx.rect

            # compute the points relative to the edge for each door
            xs = list(range(rect_door.left, rect_door.right))
            ys = list(range(rect_door.top, rect_door.bottom))

            top_points   = list(zip(xs, [rect_door.top] * len(xs)))
            left_points   = list(zip([rect_door.left] * len(ys), ys))
            right_points  = list(zip([rect_door.right] * len(ys), ys))
            bottom_points = list(zip(xs, [rect_door.bottom] * len(xs)))

            points_door = [*points_door, *top_points, *left_points, *right_points, *bottom_points]

        # furniture points
        for furniture in all_furniture:
            rect_furniture = furniture.rect_gfx.rect

            # compute the points relative to the edge for each door
            xs = list(range(rect_furniture.left, rect_furniture.right))
            ys = list(range(rect_furniture.top,  rect_furniture.bottom))

            top_points = list(zip(xs, [rect_furniture.top] * len(xs)))
            left_points = list(zip([rect_furniture.left] * len(ys), ys))
            right_points = list(zip([rect_furniture.right] * len(ys), ys))
            bottom_points = list(zip(xs, [rect_furniture.bottom] * len(xs)))

            points_furniture = [*points_furniture, *top_points, *left_points, *right_points, *bottom_points]

        points = [*points_window, *points_door, *points_furniture]

        for point in points:
            v2 = pg.math.Vector2(point[0], point[1])
            dis = self.euclidean_distance(v1, v2)
            if dis < min_distance:
                min_distance = dis
                point_min_distance = v2

        return point_min_distance, min_distance

    def compute_clearance(self):
        point_min_distance_walls, min_distance_walls = self._clearance_walls()
        point_min_distance_obs, min_distance_obs = self._clearance_obstacles()

        if min_distance_walls < min_distance_obs:
            return point_min_distance_walls, min_distance_walls
        else:
            return point_min_distance_obs, min_distance_obs

    def apf(self, goal_position: pg.math.Vector2, speed, profile = "conical"): # valid values for profile = "conical", "paraboloidal", "mixed".

        # -------------------------- compute the attractive force
        error: pg.math.Vector2 = goal_position - self.pepper.get_position()
        ka = 0.05; kb = 2  # ka = 0.05; kb = speed

        if profile == 'conical':
            ka = speed
            f_a = ka * (error/error.length())   # constant force
        elif profile == "paraboloidal":
            f_a = ka * error
        elif profile == 'mixed':                                   # use mixed version
            p = kb/ka
            if error.length() <= p: # use paraboloidal when close to the goal
                f_a = ka * error
                if self.apf_not_switched:
                    self.pepper.output_box.add_message(f"Mixed profile: switching from Conical to Paraboloidal")
                    self.apf_not_switched = False
            else:                   # use conic when too far
                f_a = kb * (error / error.length())
        else:
            raise ValueError("Invalid type for the APF profile!")

        # avoid saturation (by paraboloidal profile) clipping to cruise standard speed
        # if f_a.length() > speed:
        #     f_a = pg.math.Vector2.normalize(f_a)
        #     f_a = speed * f_a

        # -------------------------- compute the repulsive force
        gamma = 2
        range_influence = 20 # 50
        k_r = 700 # 600  # 500
        clearance_point, clearance = self.compute_clearance()

        if clearance > range_influence:
            f_r = pg.math.Vector2(0, 0)
        else:
            # try:
            try:
                repulsive_gain = (k_r/(clearance**2)) * ((1/clearance) - (1/range_influence))**(gamma-1)
            except:
                repulsive_gain = 5
            
            if repulsive_gain > 5:
                repulsive_gain = 5
                
                
            clearance_gradient = (self.pepper.get_position() - clearance_point)
            f_r = repulsive_gain * clearance_gradient

        # -------------------------- compute the vortex field heuristic force

        # parameter for the selection of force vortex direction
        epsilon = 0.1
        
        if f_r.length() == 0:               # if there is no repulsive force neither vortex filed force is present
            f_v = pg.math.Vector2(0, 0)
            self.saved_vortex = None
        else:   
            if self.saved_vortex is None:         
                f_v1 = f_r.rotate(-90)
                f_v2 = f_r.rotate(90)
                
                e1 = self.euclidean_distance(f_a, f_v1)
                e2 = self.euclidean_distance(f_a, f_v2)
                # print(f_v1, e1)
                # print(f_v2, e2)
                
                delta = e1 -e2
                # # print(delta)
                if delta > epsilon:
                    f_v = f_v2
                elif delta < -epsilon:
                    f_v = f_v1
                else:    # delta in the interval - epsiolon + episolon (stalemate case)
                    # print("bad case")
                    # heuristic, it's better to move toward the center of the rooom
                    room_center = pg.math.Vector2(self.pepper.actual_room.x, self.pepper.actual_room.y)
                    to_center = room_center - pg.math.Vector2(self.pepper.x, self.pepper.y)
                    
                    d1 = self.euclidean_distance(to_center, f_v1)
                    d2 = self.euclidean_distance(to_center, f_v2)
                    
                    if d1 > d2:
                        f_v = f_v2
                    else:
                        f_v = f_v1
                        
                    # if f_v.length() < 0.5:
                    norms = []
                    for pos in self.last_positions:
                        norms.append(self.euclidean_distance(pg.math.Vector2(self.pepper.x, self.pepper.y), pos))
                    

                    # if all(norm < 1.5 for norm in norms) and len(norms)>8:
                    avg_norms = sum(norms) / len(norms)
                    # print(avg_norms)
                    if avg_norms < 6 and len(norms)>6:
                        self.saved_vortex= pg.math.Vector2.normalize(f_v)
                        self.saved_vortex *= speed
                        
                    # self.saved_vortex = f_v
            else:
                print("using saved one")
                print(self.saved_vortex)
                f_v = self.saved_vortex 



        # -------------------------- estimate the total resulting force

        # standard form without heuristics
        # f_t = f_a + f_r + f_v
        
        # Amp_v   = f_v.length()/(f_a + f_r + f_v).length()
        # Amp_r   = f_r.length()/(f_a + f_r + f_v).length()
        # Amp_a   = f_a.length()/(f_a + f_r + f_v).length()
        
        
        # # clamp vortex force 
        # if f_v.length() > speed:
        #     f_v = pg.math.Vector2.normalize(f_v)
        #     f_v = speed * Amp_v *  f_v
            
        # if f_a.length() > speed:
        #     f_a = pg.math.Vector2.normalize(f_a)
        #     f_a = speed * Amp_a *  f_a
            
        # if f_r.length() > speed:
        #     f_r = pg.math.Vector2.normalize(f_r)
        #     f_r = speed * Amp_r *  f_r
        
        
        f_t = f_a + f_r + f_v

        # f_v = None

        # detach_vortex = 1.2
        # if f_r.length() >= detach_vortex * f_a.length():
        #     if self.saved_vortex == None:
        #         f_v = f_v.rotate(180)
        #         self.saved_vortex = f_v

                
        #     if f_v.length() > speed:
        #         f_v = pg.math.Vector2.normalize(f_v)
        #         f_v = speed  * f_v
                
        #     f_t = f_v


        # avoid saturation (by paraboloidal profile) clipping to cruise standard speed
        if f_t.length() > speed:
            f_t = pg.math.Vector2.normalize(f_t)
            f_t = speed * f_t
            
        # print(f_t.length())
        
        # if stealmate invert sense for the heuristic
        # if f_t.length() < 0.4 and self.verse != 0:
            # print("aoaaaaaa")
            # self.verse *= -1
        
        # else:
        #     norms = []
        #     for pos in self.last_positions:
        #         norms.append(self.euclidean_distance(pg.math.Vector2(self.pepper.x, self.pepper.y), pos))

        #     print(norms)
        #     if all(norm < 1.5 for norm in norms) and len(norms)>8:
        #         print("cambioooooo")
        #         self.verse *= -1
                
        # save info forces
        self.last_apf['f_a'] = f_a
        self.last_apf['f_r'] = f_r
        self.last_apf['f_v'] = f_v
        self.last_apf['f_t'] = f_t

        return f_t


class HouseSimulatorSocket(object):
    
    def __init__(self, interpreter, pepper, local_folder = False):
        super().__init__()
        self.local_folder = local_folder
        # self.pipe_path = "../tmp/pipe_sim"
        if not local_folder:
            self.pipe_path_HS2P = "./../tmp/pipe_sim_HS2P"      # house simulator to pepper simulator
            self.pipe_path_P2HS = "./../tmp/pipe_sim_P2HS"      # pepper simulator to house simulator
        else:
            self.pipe_path_HS2P = "./tmp/pipe_sim_HS2P"      # house simulator to pepper simulator
            self.pipe_path_P2HS = "./tmp/pipe_sim_P2HS"      # pepper simulator to house simulator
        
        
        self.mode  = 0o600 # octal
        self.interpreter = interpreter
        self.pepper = pepper
        
        # create pipes
        self.createFIFO(self.pipe_path_HS2P)
        self.createFIFO(self.pipe_path_P2HS)
        
        # list for command received during the exectuion
        self.command_list = []
        
        # create a new deamon thread to listen (background thread)
        
        # time.sleep(0.2)
        self.listener_thread = threading.Thread(target = self.receive_command)
        self.listener_thread.daemon = True
        self.listener_thread.start()
        
        
        # planner
        self.previous_plan = None
        self.parser = ParserPDDL(pathsFromSim= True)
        self.solver = SolverFF(pathsFromSim=True)
        self.counter = 0
        
        
    # function to exe the commands as a queue of instructions
    def exe_commmands(self):
        while len(self.command_list) != 0:
            command = self.command_list.pop(0)
            # if self.interpreter is not None:
            self.interpreter.execute(command)
    
    def setInterpreter(self, interpreter):
        self.interpreter = interpreter
    
    def createFIFO(self, path):
        print(os.getcwd())
        
        # go back to path pointer to ./EAI2
        # if "2DPathSimulator" in os.getcwd():
        #     os.chdir("../")
        #     print(f"Current location (cwd): {os.getcwd()}")
        
        # if not os.path.exists("../tmp/"):
        #     print("not exists tmp folder")
        #     os.mkdir('../tmp/')
        if not self.local_folder:
            if not os.path.exists("./../tmp/"):
                print("not exists tmp folder")
                os.mkdir('./../tmp/')
        else:
            if not os.path.exists("./tmp/"):
                print("not exists tmp folder")
                os.mkdir('./tmp/')
            
        if not os.path.exists(path):
            os.mkfifo(path, self.mode)
            
     
    def send_command(self, command):
        with open(self.pipe_path_HS2P, "w") as pipe:
            # while True:
            if command is None:
                command = input("Enter a command to send: ")

            pipe.write(command)
            pipe.flush()
            print("command has been flushed")
            
    def receive_command(self):

        with open(self.pipe_path_P2HS, "r") as pipe:
            while True:
                command = pipe.readline()                       #.strip()
                
                # optional: check syntax of the command
                if command:
                    print(f"Received command: {command}")
                
                    # exe
                    task_descriptor = None
                    try:                # try to decode as a task descriptor
                        task_descriptor = json.loads(command)   # for the opposite, object to string: serialized_dict = json.dumps(my_dict)
                        if task_descriptor == []: continue
                    
                        if type(task_descriptor[0]) is str:
                            print("to remove object info sent")
                            self.parser.unknown_list = [*self.parser.unknown_list, *task_descriptor]
                            # unknow  for init
                        else:
                            if "type" in list(task_descriptor[0].keys()):
                                print("new task has been sent")
                                self.send_task(task_descriptor)
                                
                            elif "object" in list(task_descriptor[0].keys()):
                                print("new info about house item has been sent")  
                                self.parser.learned_list = [*self.parser.learned_list, *task_descriptor]
                   
                    except:
                        if self.interpreter is not None:
                            self.interpreter.execute(command)
                    


                        
                    # save the story for the actual session
                    self.command_list.append(command)
                
                    
    
    def send_task(self, task):
        if self.pepper.plan is None:   # is free and not busy
            #2) parse for first set of tasks
            self.parser.parse_goal(tasks_description= task)
            self.parser.parse_init(previous_plan = self.previous_plan)
            
            #3) exe first set of tasks
            plan = self.solver.forward()
            
            self.previous_plan = deepcopy(plan)
            
            if not(plan is None):
                self.solver.print_plan(plan)
            else:
                print("plan is None")
                self.send_command("None plan")
            
            #4)execute the plan with pepper
            print(plan)
            self.pepper.provide_plan(plan, self)
            self.counter += 1 
            self.counter = self.counter%2
        
        else:
            self.pepper.output_box.add_message(f"Pepper is busy cannot execute the task")
            plan = None
    
        return plan
    
    def test_plan(self):

        print("previous plan:", self.previous_plan)
        # 1) task atoms definition, and complete ones
        t1 = {"type": "move_object", "args": ['glasses', "table_living"], "free hands": True}
        t2 = {"type": "reach_position", "args": ['free_space'], "free hands": True}
        t3 = {"type": "reach_room", "args": ['studio'], "free hands": True}
        t4 = {"type": "move_object", "args": ['cards', "table_kitchen"], "free hands": True}
        t5 = {"type": "reach_position", "args": ['sofa'], "free hands": True}
        t6 = {"type": "reach_room", "args": ['dining'], "free hands": True}
        
        t7 = {"type": "close_window", "args": ['wl_dining'], "free hands": True}
        t8 = {"type": "close_window", "args": ['wr_dining'], "free hands": True}
        t9 = {"type": "open_window", "args": ['wl_bedroom'], "free hands": True}
        t10 = {"type": "open_window", "args": ['wr_bedroom'], "free hands": True}
        # simple task
        task_simple = [t6,t2]
        
        # open/close task
        task_oc = [t7,t8,t9,t10,t2]
        
        # mixed task
        task_description0 = [t3,t2]
        task_description  = [t1,t2,t3]
        task_description2 = [t4,t5]
        
        tasks_description = [task_oc, task_description0,task_description, task_description2]
        task = tasks_description[self.counter]
        
        
        if self.pepper.plan is None:   # is free and not busy
            #2) parse for first set of tasks
            self.parser.parse_goal(tasks_description= task)
            self.parser.parse_init(previous_plan = self.previous_plan)
            
            #3) exe first set of tasks
            plan = self.solver.forward()
            
            self.previous_plan = deepcopy(plan)
            
            if not(plan is None):
                self.solver.print_plan(plan)
            
            #4)execute the plan with pepper
            print(plan)
            self.pepper.provide_plan(plan, self)
            self.counter += 1 
            self.counter = self.counter%2
        
        else:
            self.pepper.output_box.add_message(f"Pepper is busy cannot execute the task")
            plan = None
        
        return plan
        
"""
                                                test section
"""

testing_pipe = 0
test_send = 0

if testing_pipe:
    command_socket = HouseSimulatorSocket(None, local_folder= True)

    #   [request]
    if test_send:
        while True:
            command_socket.send_command(None)
            
    #   [receive]
    else:
        i = 0
        while True:
            print(i)
            i+= 1
            time.sleep(5)


