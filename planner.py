# code used to generate the high level plan 
# requires the installation of metric-FF or classic FF planning software in the folder EAI2/Metric-FF  

import subprocess
import os 
import re


class SolverFF():
    def __init__(self, pathsFromSim = False):
        
        # paths from ./EAI2
        self.domain_file  = "house_sim_domain.pddl"
        self.problem_file = "house_sim_problem.pddl"
        self.path2ff      = "./Metric-FF"
        self.path2pddl    = "./pddl"

        # adjust paths in case of sim launching
        if pathsFromSim:
            # self.domain_file     = os.path.join("./..",self.domain_file)
            # self.problem_file    = os.path.join("./..",self.problem_file)
            self.path2ff         = os.path.join("./..",self.path2ff)
            self.path2pddl       = os.path.join("./..",self.path2pddl)

    
    def forward(self, domain_file = None, problem_file = None, verbose = False): 
        
        if domain_file is None: domain_file = self.domain_file
        if problem_file is None: problem_file = self.problem_file
        
        output = subprocess.run([os.path.join(self.path2ff, "ff") + " -o " + os.path.join(self.path2pddl, domain_file) +
                                " -f " + os.path.join(self.path2pddl, problem_file)], shell=True, capture_output=True, text= True)

        if verbose: print(output.stdout)
        try:
            plan = self.parse_outputFF(output.stdout)
        except:
            print("Error from FF planning software:\n")
            print(output.stderr)
            print(output.stdout)
            plan = None
            
        return plan


    def parse_outputFF(self,output):
        plan = []
        lines = output.split("\n")
        
        # look for the first line which describes the plan
        idx_start = -1
        for idx, line in enumerate(lines):
            #print(line)
            match_start= re.match(r"^step.*\d", line)
            if match_start is not None:
               # print(match_start.group())
                idx_start = idx
                break
        
        if idx_start == -1: return None
        
        # takes all the lines with the plan
        idx_end = idx_start
        for line in lines[idx_start:]:
            # print(line.strip())
            match_step = re.match(r'^.*\d:.*$', line.strip())

            if match_step is not None:
                # print("-------------------------------------------------------------")
                # print(match_step.group())
                idx_end += 1
        
        plan_lines = [line.split(":")[1].strip() for line in lines[idx_start: idx_end]]

        
        for plan_line in plan_lines:
            words = plan_line.split(" ")
            if len(words) > 1:
                step = {"action": words[0], "arguments":  words[1:]}
            else:    
                step = {"action": words[0]}
            plan.append(step)

        return plan
    
    """
        function that descibes the meaning of the action arguments
    """
    def argAction_semantic(self, step_plan):
        map_arg = {}
        action = step_plan['action']
        args = step_plan['arguments']
        
        if action.strip().lower() == "move2":
            map_arg = {"in room":args[0], "from position":args[1], "to position":args[2]  , "type": "motion"}
        elif action.strip().lower() == "move2room":
            map_arg = {"from room":args[0], "to room":args[1], "through door":args[2]  , "in direction": args[3], "type": "motion"}        
        elif action.strip().lower() == "open_door" or action.strip().lower() == "close_door":
            map_arg = {"which door": args[0], "in room": args[1],"type": "open/close"}
        elif action.strip().lower() == "open_win" or action.strip().lower() == "close_win":
            map_arg = {"which window": args[0], "in room": args[1],"type": "open/close"}
        elif action.strip().lower() == "grab_object":
            map_arg = {"which item": args[0], "in room": args[1], "on what":args[2], "type": "grab/place"}
        elif action.strip().lower() == "place_object":
            map_arg = {"which item": args[0], "in room": args[1], "on what":args[2], "type": "grab/place"}
        else:
            raise ValueError(f"The command {action} is not modelled in the PDDL")
            
        return map_arg

        """
        semantic symbologism in names:
        d_ -> door
        wl_-> window left
        wr_-> window right
        l_ -> left
        r_ -> right
        """
    
    def print_plan(self, plan):
        for i, step_plan in enumerate(plan):
            print("{:<2}) action = {:<15}".format(i, step_plan['action']))
            arguments = self.argAction_semantic(step_plan)
            print("     " + str(arguments))

        
# output = subprocess.run(["ls -n"], shell=True, capture_output=True, text= True)
# output = subprocess.run(["pyperplan","-H ",planner_name," ",domain_file, " ",problem_file], shell=True, capture_output=True, text= True)
# ./Metric-FF/ff -o ./pddl/domain.pddl -f ./pddl/problem.pddl

# class used to generate the PDDL files
class ParserPDDL():
    
    def __init__(self, pathsFromSim = False):
        self.path2pddl          = "./pddl"
        self.domain_file        = "house_sim_domain.pddl"
        self.problem_file       = "house_sim_problem_template.pddl"
        self.generated_file     = "parsed_problem.pddl"
        self.firstParsing = True   # boolean flag used to understand when starting from template or starging from an already generated PDDL
        
        if pathsFromSim:
            # self.domain_file     = os.path.join("./..",self.domain_file)
            # self.problem_file    = os.path.join("./..",self.problem_file)
            self.path2pddl       = os.path.join("./..",self.path2pddl)

        self.predicates = self.get_predicates()
        self.objects = self.get_objects()

        
    def get_objects(self):
        """
                get name declared internally in the PDDL
        """
        
        objects = {}
        objects['room'] = "foyer living_room dining toilet studio bedroom kitchen outdoor".split(" ")
        objects['door'] = "d_foyer_outdoor d_foyer_living  d_toilet_living d_studio_living d_bedroom_living d_living_dining d_dining_kitchen".split(" ")
        objects['window'] = "wl_foyer  wl_toilet wl_studio wl_bedroom wl_dining wl_kitchen wr_foyer  wr_toilet wr_studio wr_bedroom wr_dining wr_kitchen".split(" ")
        objects['item'] = "green_marker pen pencil plate_empty cup_coffee plate_oranges plate_apples orange1 orange2 orange3 apple1 apple2 smartphone red_notebook green_notebook glasses yellow_notebook cards pink_notebook".split(" ")
        objects['furniture'] = "desk_studio pool_studio kitchenette table_kitchen bed cabinet_bedroom_l cabinet_bedroom_r tv_bedroom water tub sink cabinet_toilet tv_living sofa table_living armchair_l armchair_r table_dining".split(" ")
        objects['what'] = [*objects['door'], *objects['window'], *objects['item'], *objects['furniture']]
        
        return objects 
        
        
    def get_doorName(self, room1, room2):
        room1 = room1.strip().lower()
        room2 = room2.strip().lower()
        
        if (room1 in "foyer" or room2 in "foyer") and (room1 in "outdoor" or room2 in "outdoor"):
            return "d_foyer_outdoor"  
        elif (room1 in "foyer" or room2 in "foyer") and (room1 in "living room" or room2 in "living room"):     
            return "d_foyer_living"
        elif (room1 in "toilet" or room2 in "toilet") and (room1 in "living room" or room2 in "living room"):
            return "d_toilet_living"
        elif (room1 in "studio" or room2 in "studio") and (room1 in "living room" or room2 in "living room"):
            return "d_studio_living"
        elif (room1 in "bedroom" or room2 in "bedroom") and (room1 in "living room" or room2 in "living room"):
            return "d_bedroom_living"
        elif (room1 in "dining" or room2 in "dining") and (room1 in "living room" or room2 in "living room"):
            return "d_living_dining"
        elif (room1 in "dining" or room2 in "dining") and (room1 in "kitchen" or room2 in "kitchen"):
            return "d_dining_kitchen"
        else:
            raise ValueError("The rooms chosen have no door!")
        
        
    
    def get_predicates(self):
        """
            what -> for room_element in pddl
        """
        predicates = {}
        # predicates['connected']      = "(connected ?[from_room] ?r2 - room  ?d - direction)"
        # predicates['isPositioned']   = "(isPositioned ?o - room_element ?r - room ?d - direction)"
    
        predicates['in']             = "(in ?what ?room)"
        predicates['on']             = "(on ?item ?what)"
        predicates['openDoor']       = "(openDoor ?door)"
        predicates['openWin']        = "(openWin ?window)"
        predicates['PepperIn']       = "(PepperIn ?room)"
        predicates['PepperAt']       = "(PepperAt ?what)"
        predicates['PepperHas']      = "(PepperHas ?item)"
        predicates['freeHands']      = "(freeHands)"
        
        return predicates
        
    # TODO
    def planStep2Predicates(self, plan_step):
        action = plan_step['action'].lower().strip()
        args = plan_step['arguments']
        predicates = []
        # if action == "move2":
            
        # elif action == "move2room":
            
        # elif action == "open_door":
            
        # elif action == "close_door":
            
        # elif action == "open_win":
            
        # elif action == "close_win":
            
        # elif action == "grab_object":
            
        # elif action == "place_object":
        return predicates
          
    def tasks2Predicates(self, tasks_description):
        """
            tasks_description is a list of task, each task is a dictionary with the following structure:
            - type
            - *args
            - boolean: free hands
            5 types of task for task description: motion, open/close, grab/place
            
            ff tries always to satisfies the first tasks before the other, so place the reach position and reach room as final tasks (priority problem)
            
        """
        goal = "        (and "
        freeHands_inserted = False
        
        # to handle single task problems
        if type(tasks_description) is dict:
            tasks_description = [tasks_description] 
        
        for task_description in tasks_description:
            
            if task_description['type'] == "reach_position":
                predicate_task = self.predicates['PepperAt']
                assert task_description['args'][0] in self.objects['what']
                predicate_task = predicate_task.replace("?what", task_description['args'][0])
                
            elif task_description['type'] == "reach_room":
                predicate_task = self.predicates['PepperIn']
                assert task_description['args'][0] in self.objects['room']
                predicate_task = predicate_task.replace("?room", task_description['args'][0])
                
            elif task_description['type'] == "open_door":
                predicate_task = self.predicates['openDoor']
                assert task_description['args'][0] in self.objects['door']
                predicate_task = predicate_task.replace("?door", task_description['args'][0])
                
            elif task_description['type'] == "close_door":
                predicate_task = "(not " + self.predicates['openDoor']+")"
                assert task_description['args'][0] in self.objects['door']
                predicate_task = predicate_task.replace("?door", task_description['args'][0])
                
            elif task_description['type'] == "open_window":
                predicate_task = self.predicates['openWin']
                assert task_description['args'][0] in self.objects['window']
                predicate_task = predicate_task.replace("?window", task_description['args'][0])
                
            elif task_description['type'] == "close_window":
                predicate_task = "(not " + self.predicates['openWin']+")"
                assert task_description['args'][0] in self.objects['window']    
                predicate_task = predicate_task.replace("?window", task_description['args'][0])
                
            elif task_description['type'] == "move_object":                     #"(on ?item ?what)"
                predicate_task = self.predicates['on']
                assert task_description['args'][0] in self.objects['item']
                assert task_description['args'][1] in self.objects['what']
                predicate_task = predicate_task.replace("?item", task_description['args'][0])
                predicate_task = predicate_task.replace("?what", task_description['args'][1])
                
            # insert the freeHands one max
            if task_description["free hands"] and not(freeHands_inserted):
                freeHands_inserted = True
                
            goal += predicate_task + " "
            
        if freeHands_inserted:
             goal = goal + " " + self.predicates['freeHands']
             
        goal +=  ")\n" 
            
        return goal
        
    
    
    def getNumber_parenthesis(self, line): 
        increment = line.count('(')
        decrement = line.count(')')
        # print(f"increment {increment}")
        # print(f"decrement {decrement}")
        return increment - decrement
    
    
    def _chunk_init(self, init):
        chunks = []
        last_idx = 0
        for idx,line in enumerate(init):
            res = re.match(r".*;.*doors.*", line)
            if res is not None:
                # print(res.group(), idx)
                chunks.append((last_idx,idx))
                last_idx = idx
                
            res = re.match(r".*;.*window.*\[left\].*", line)
            if res is not None:
                # print(res.group(), idx)
                chunks.append((last_idx,idx))
                last_idx = idx
            res = re.match(r".*;.*window.*\[right\].*", line)
            if res is not None:
                # print(res.group(), idx)
                chunks.append((last_idx,idx))
                last_idx = idx
            res = re.match(r".*;.*objects.*", line)
            if res is not None:
                # print(res.group(), idx)
                chunks.append((last_idx,idx))
                last_idx = idx
            res = re.match(r".*;.*furniture.*", line)
            if res is not None:
                # print(res.group(), idx)
                chunks.append((last_idx,idx))
                last_idx = idx
            res = re.match(r".*;.*pepper.*", line)
            if res is not None:
                # print(res.group(), idx)
                chunks.append((last_idx,idx))
                last_idx = idx
            
        chunks.append((last_idx, len(init)))    
        
        return chunks
    
    
    def remove_objectKnowledge(self, init_items, object: str):
        query = object.strip().lower()
        to_remove = []
        for idx, line in enumerate(init_items):
            if query in line:
                # print(line)
                to_remove.append(idx)
                
        if to_remove != []:     
            to_remove.sort(reverse= True)       
        
            for idx in to_remove:
                del init_items[idx]
        else:
            raise ValueError(f"wrong name object selected in function: {self.remove_objectKnowledge.__name__}")
            
        
        return init_items
        
    def add_objectKnowledge(self, init_items, info):
        
        object = info['object']
        room = info['room']
        furniture = info['furniture']

        
        if room is None and furniture is None:
            raise ValueError("No new data to save")
        
        init_items[-2] = "\n"
        
        if not(room is None):   # in predicate
            p = self.predicates['in']
            p = p.replace("?what", object)
            p = p.replace("?room", room)
            init_items.insert(len(init_items)-2, "        " + p +"\n")
        if not(furniture is None): #on predicate
            p = self.predicates['on']
            p = p.replace("?item", object)
            p = p.replace("?what", furniture)
            init_items.insert(len(init_items)-2, "        " +p + "\n")
        
        
           
        
        # predicates['in']             = "(in ?what ?room)"
        # predicates['on']             = "(on ?item ?what)"
        
        
    def define_init(self, starting_init, unknown_list, learned_list):
        lines_init = []
        
        #                       chunk init 
        chunks = self._chunk_init(starting_init)
        
        header_init         = starting_init[chunks[0][0]:chunks[0][1]]
        # print(header_init)
        init_doors          = starting_init[chunks[1][0]:chunks[1][1]]
        # print(init_doors)
        init_window_left    = starting_init[chunks[2][0]:chunks[2][1]]
        # print(init_window_left)
        init_window_right   = starting_init[chunks[3][0]:chunks[3][1]]
        # print(init_window_right)
        init_items          = starting_init[chunks[4][0]:chunks[4][1]]
        # print(init_items)
        init_furniture      = starting_init[chunks[5][0]:chunks[5][1]]
        # print(init_furniture)
        init_pepper         = starting_init[chunks[6][0]:chunks[6][1]]
        # print(init_pepper)
        
        #                       initial state for the environment
        # 1) remove doors
        to_remove_door = []
        doors_closed = [self.get_doorName("outdoor","foyer"), self.get_doorName("living","toilet"),
                       self.get_doorName("living","studio"), self.get_doorName("living","bedroom"), self.get_doorName("kitchen","dining")]
        for idx,line in enumerate(init_doors):
            if ("openDoor" in line) and (any(door_name in line for door_name in doors_closed)):
                to_remove_door.append(idx)
        to_remove_door.sort(reverse= True)       
        # print(to_remove_door)
        for idx in to_remove_door:
            del init_doors[idx]
        
        # 2) remove left windows   
        to_remove_win = []
        win_closed = ["foyer", "bedroom", "kitchen", "studio"]
        for idx,line in enumerate(init_window_left):
            if ("openWin" in line) and (any(win_name in line for win_name in win_closed)):
                to_remove_win.append(idx)
        to_remove_win.sort(reverse= True)       
        # print(to_remove_win)
        for idx in to_remove_win:
            del init_window_left[idx]
            
            
        # 3) remove right windows      
        to_remove_win = []
        win_closed = ["foyer", "bedroom", "kitchen", "studio"]
        for idx,line in enumerate(init_window_right):
            if ("openWin" in line) and (any(win_name in line for win_name in win_closed)):
                to_remove_win.append(idx)
        to_remove_win.sort(reverse= True)       
        # print(to_remove_win)
        for idx in to_remove_win:
            del init_window_right[idx]
        
        
        #                         select unknown predicates
        for unknown in unknown_list:
            self.remove_objectKnowledge(init_items, unknown)
            self.remove_objectKnowledge(init_furniture, unknown)
        
        for learned in learned_list:
            self.add_objectKnowledge(init_furniture, learned)
            
        # self.add_objectKnowledge(init_furniture, "gameboy","studio","desk_studio")
        
        lines_init = [*header_init, *init_doors, *init_window_left, *init_window_right, *init_items, *init_furniture, *init_pepper]
        
        return lines_init
    
    def parse_goal(self, tasks_description = None, verbose = False):
        # problem pddl lines
        lines = []

        #                               read 
        if self.firstParsing:
            input_file = self.problem_file
        else:
            input_file = self.generated_file
        
        with open(os.path.join(self.path2pddl, input_file), 'r') as problem_file:
            lines = [line for line in problem_file]
        
        #                               edit
        # 1) get idx of start and end for the edits
        idx_goal_start = -1;idx_goal_end = -1;
        counter_parenthesis = -1;                # open +1, close -1 from when i match goal
        for idx, line in enumerate(lines):
            res = re.match(r".*:goal.*", line)
            if res is not None:
                # print(res.group())
                idx_goal_start = idx
                counter_parenthesis = 0
                counter_parenthesis += self.getNumber_parenthesis(line)
                continue
            
            if counter_parenthesis != -1:
                # print(counter_parenthesis)
                counter_parenthesis += self.getNumber_parenthesis(line)
                
            if counter_parenthesis == 0:
                idx_goal_end = idx
                break
        
        if verbose: print("line start goal {}".format(idx_goal_start))
        if verbose: print("line end goal {}".format(idx_goal_end))
        
        # 2) remove goal lines
        lines = [*lines[:idx_goal_start], *lines[idx_goal_end +1:]]
        
        # 3) define template for goals
        
        line_goals = idx_goal_start+1
        
        lines.insert(idx_goal_start,    "    (:goal\n")
        lines.insert(line_goals,        self.tasks2Predicates(tasks_description))
        lines.insert(idx_goal_start+2,  "    )\n")
        
        
        #                               write
        with open(os.path.join(self.path2pddl, self.generated_file), 'w') as problem_file:
            for line in lines:
                problem_file.write(line)
                
        if self.firstParsing: self.firstParsing = False
        
    def parse_init(self, unknown = [], learned = [], previous_plan = None):    #previous_plan used to update the init by actions
        # problem pddl lines
        lines = []
    
        #                               read 
        if self.firstParsing:
            input_file = self.problem_file
        else:
            input_file = self.generated_file
        with open(os.path.join(self.path2pddl, input_file), 'r') as problem_file:
            lines = [line for line in problem_file]
        
        #                               edit
        # 1) get idx of start and end for the edits
        idx_init_start = -1;idx_init_end = -1;
        counter_parenthesis = -1;                # open +1, close -1 from when i match goal
        for idx, line in enumerate(lines):
            res = re.match(r".*:init.*", line)
            if res is not None:
                # print(res.group())
                idx_init_start = idx
                counter_parenthesis = 0
                counter_parenthesis += self.getNumber_parenthesis(line)
                continue
            
            if counter_parenthesis != -1:
                # print(counter_parenthesis)
                counter_parenthesis += self.getNumber_parenthesis(line)
                
            if counter_parenthesis == 0:
                idx_init_end = idx
                break
        
        # 2) edit init 
        init_file = lines[idx_init_start:idx_init_end+1]
        lines_init = self.define_init(init_file, unknown_list = unknown, learned_list = learned)   # learned list of dictionaries with this structure {'object':x, 'room':x, 'furniture':x} 
        
        # 3) update by previous plan if exists
        if previous_plan is not None:
            self.update_init(lines_init, previous_plan)
        
        # 3) collect together chunks
        lines = [*lines[:idx_init_start], *lines_init ,*lines[idx_init_end+1:]]    
        #                               write
        with open(os.path.join(self.path2pddl, self.generated_file), 'w') as problem_file:
            for line in lines:
                problem_file.write(line)
        
        if self.firstParsing: self.firstParsing = False
    
    #TODO
    def update_init(self,lines_init, plan):
        pass
        for step in plan:
            predicates = []  # self.planStep2Predicates(plan)
            for predicate in predicates:
                lines_init.insert(len(lines_init)-2, "        " + predicate + "\n")
            
    
    
    # re-generate pddl problem file starting from template (look for when you reset the environment? #TODO)
    def reset(self):
        self.firstParsing = True

"""
                                                test section
"""

test = {"parse": 1, "solve": 1}

if test['parse']:
    parser = ParserPDDL()
    
    #                                   test goal parser
    t1 = {"type": "reach_position", "args": ['desk_studio'], "free hands": True}
    # t2 = {"type": "close_door", "args": ["d_toilet_living"], "free hands": True}
    # t3 = {"type": "open_door", "args": ["d_dining_kitchen"], "free hands": True}
    t4 = {"type": "close_window", "args": ["wl_studio"], "free hands": False}
    t5 = {"type": "open_window", "args": ["wr_studio"], "free hands": True}
    # t6 = {"type": "move_object", "args": ["smartphone", "sofa"], "free hands": False}
    # t7 = {"type": "reach_room", "args": ["foyer"], "free hands": False}
    
    # tasks_description1 = [t2, t3, t4]
    # tasks_description2 = [t5, t6, t7]
    task_description = [t1, t4, t5]
    parser.parse_goal(tasks_description= task_description)
    # parser.parse_goal(tasks_description= tasks_description1)
    # input("press something")
    # parser.parse_goal(tasks_description= tasks_description2)
    
    #                                   test init parser
    # parser.parse_init(, unknown = ["smartphone", "glasses"], learned = [{'object':'smartphone', 'room':"bedroom", 'furniture':"bed"}, {'object':'glasses', 'room':"toilet", 'furniture':"sink"}])
    parser.parse_init()


if test['solve']:
    solver = SolverFF()
    plan= solver.forward(domain_file="house_sim_domain.pddl", problem_file="parsed_problem.pddl", verbose = False)
    print(plan)
    solver.print_plan(plan)


