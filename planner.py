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
            self.domain_file     = os.path.join("./..",self.domain_file)
            self.problem_file    = os.path.join("./..",self.problem_file)
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
        self.domain_file  = "house_sim_domain.pddl"
        self.problem_file = "house_sim_problem_template.pddl"
        
        if pathsFromSim:
            self.domain_file     = os.path.join("./..",self.domain_file)
            self.problem_file    = os.path.join("./..",self.problem_file)
            self.path2pddl       = os.path.join("./..",self.path2pddl)
    
    def getNumber_parenthesis(self, line): 
        increment = line.count('(')
        decrement = line.count(')')
        print(f"increment {increment}")
        print(f"decrement {decrement}")
        return increment - decrement
    
    #TODO
    def define_goal(self, plan_objectives):
        goals = "(on smartphone table_kitchen)"
        goal_line = "        (and " + goals + ")\n"
        return goal_line
    
    #TODO
    def define_problemInstance(self, init_states):
        lines_init = []
        for init_state in init_states:
            pass
        return lines_init
    
    def parse_goal(self, plan_objectives = None):
        # problem pddl lines
        lines = []

        #                               read 
        with open(os.path.join(self.path2pddl, self.problem_file), 'r') as problem_file:
            lines = [line for line in problem_file]
        
        #                               edit
        # 1) get idx of start and end for the edits
        idx_goal_start = -1;idx_goal_end = -1;
        counter_parenthesis = -1;                # open +1, close -1 from when i match goal
        for idx, line in enumerate(lines):
            res = re.match(r".*:goal.*", line)
            if res is not None:
                print(res.group())
                idx_goal_start = idx
                counter_parenthesis = 0
                counter_parenthesis += self.getNumber_parenthesis(line)
                continue
            
            if counter_parenthesis != -1:
                print(counter_parenthesis)
                counter_parenthesis += self.getNumber_parenthesis(line)
                
            if counter_parenthesis == 0:
                idx_goal_end = idx
                break
        
        print("line start goal {}".format(idx_goal_start))
        print("line end goal {}".format(idx_goal_end))
        
        # 2) remove goal lines
        lines = [*lines[:idx_goal_start], *lines[idx_goal_end +1:]]
        
        # 3) define template for goals
        
        line_goals = idx_goal_start+1
        
        lines.insert(idx_goal_start,    "    (:goal\n")
        lines.insert(line_goals,        self.define_goal(plan_objectives))
        lines.insert(idx_goal_start+2,  "    )\n")
        
        
        #                               write
        with open(os.path.join(self.path2pddl, "parsed_problem.pddl"), 'w') as problem_file:
            for line in lines:
                problem_file.write(line)
        
    def parse_init(self, init_instance = None):
        # problem pddl lines
        lines = []
    
        #                               read 
        with open(os.path.join(self.path2pddl, self.problem_file), 'r') as problem_file:
            lines = [line for line in problem_file]
        
        #                               edit
        # 1) get idx of start and end for the edits
        idx_init_start = -1;idx_init_end = -1;
        counter_parenthesis = -1;                # open +1, close -1 from when i match goal
        for idx, line in enumerate(lines):
            res = re.match(r".*:init.*", line)
            if res is not None:
                print(res.group())
                idx_init_start = idx
                counter_parenthesis = 0
                counter_parenthesis += self.getNumber_parenthesis(line)
                continue
            
            if counter_parenthesis != -1:
                print(counter_parenthesis)
                counter_parenthesis += self.getNumber_parenthesis(line)
                
            if counter_parenthesis == 0:
                idx_init_end = idx
                break
        
        print("line start init {}".format(idx_init_start))
        print("line end init  {}".format(idx_init_end))
        

            
        # 2) edit init 
        n_lines = idx_init_end - idx_init_start
        template_init = lines[idx_init_start:idx_init_end+1]
        print(template_init)
        
        #TODO edit template_init list using self.define_problemInstance(init_instance))
        
        
        print(lines[:idx_init_start])
        print(lines[idx_init_end+1:])
        
        
        lines = [*lines[:idx_init_start], *template_init ,*lines[idx_init_end+1:]]

        
        
        #                               write
        with open(os.path.join(self.path2pddl, "parsed_problem.pddl"), 'w') as problem_file:
            for line in lines:
                problem_file.write(line)
        
        




"""
                                                test section
"""

test = {"parse": 1, "solve": 0}

if test['parse']:
    parser = ParserPDDL()
    # parser.parse_goal(plan_objectives= None)
    parser.parse_init(init_instance = None)


if test['solve']:
    solver = SolverFF()
    plan = solver.forward(domain_file="house_sim_domain.pddl", problem_file="parsed_problem.pddl", verbose = False)
    solver.print_plan(plan)


