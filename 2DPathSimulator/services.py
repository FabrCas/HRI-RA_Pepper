import pygame as pg
import random
import math


class InputInterpreter(object):
    def __init__(self, simulation_objects):
        super().__init__()
        self.ui = simulation_objects['UI_DOs']
        self.boxes = simulation_objects['text_boxes']
        self.env = simulation_objects['environment']
        self.pepper = simulation_objects['pepper']
        self.reset = False
        self.changed_debug = False
        self.changed_show_obstacles = False
        self.boxes[1].add_message("Started the simulation")

        # self.auto_run()

    def auto_run(self):
        print("Computing the clearance...")
        self.pepper.socket._distances_wall()

    def execute(self, message):
        if "daje roma" in message.strip().lower():
            daje_roma = pg.mixer.Sound('static/sounds/daje_roma_daje.mp3')
            pg.mixer.Sound.play(daje_roma)
        if "reset" in message.strip().lower():
            print("Resetting the environment...")
            self.reset = True
        if "debug" in message.strip().lower():
            print("Changing the debug mode...")
            self.changed_debug = True
        if "obs" in message.strip().lower():
            print("Changing the show obstacles mode...")
            self.changed_show_obstacles = True
        if "clearance" in message.strip().lower():   #clearance
            pass



    def update_debug(self, debug):
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
            self.boxes[1].add_message(f"show obstacles mode: {show_obstacles}")

        return show_obstacles


class PepperSocket():
    def __init__(self, pepper):
        super().__init__()
        self.pepper = pepper


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


    def _clearance_walls(self):
        walls = self.pepper.actual_room.bounds
        v1 = pg.math.Vector2(int(self.pepper.x), int(self.pepper.y))
        min_distance = math.inf
        point_min_distance = None
        # print("v1", v1)
        for side, segments in walls.items():
            # print(f"side: {side}")
            for segment in segments:
                # print(f"segment {segment}")
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
                # print(f"points {list(points)}")

                for point in points:
                    v2 = pg.math.Vector2(point[0], point[1])
                    dis = self.euclidean_distance(v1, v2)
                    if dis < min_distance:
                        min_distance = dis
                        point_min_distance = v2
                        # print(f"new point min distance: {point_min_distance} {min_distance}")

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

        print(f"numbers of windows: {len(windows)}")
        print(f"numbers of doors: {len(doors)}")
        print(f"numbers of furniture: {len(all_furniture)}")

        # full set of points for the distance
        points_window = []
        points_door = []
        points_furniture = []

        # windows points
        for win in windows:
            win_left_rect = win[0].rect_gfx.rect
            win_right_rect = win[1].rect_gfx.rect
            # print(win_left_rect)
            # print(win_right_rect)

            # compute the points relative to the edge for the left window
            xs = list(range(win_left_rect.left, win_left_rect.right))
            ys = list(range(win_left_rect.top, win_left_rect.bottom))

            top_points_l    = list(zip(xs, [win_left_rect.top] * len(xs)))
            left_points_l   = list(zip([win_left_rect.left] * len(ys), ys))
            right_points_l  = list(zip([win_left_rect.right] * len(ys), ys))
            bottom_points_l = list(zip(xs, [win_left_rect.bottom] * len(xs)))

            # print(top_points_l)
            # print(left_points_l)
            # print(right_points_l)
            # print(bottom_points_l)

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


