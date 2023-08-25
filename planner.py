# code used to generate the high level plan 
# requires the installation of metric-FF or classic FF planning software in the folder EAI2/Metric-FF  

import subprocess
import os 
import re
# from pddl


class SolverFF():
    def __init__(self, pathsFromSim = False, ):
        
        # paths from ./EAI2
        self.domain_file  = "./domain.pddl"
        self.problem_file = "./problem.pddl"
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
        
        plan = self.parse_outputFF(output.stdout)
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
        # print(plan_lines)
        
        for plan_line in plan_lines:
            words = plan_line.split(" ")
            if len(words) > 1:
                step = {"action": words[0], "arguments":  words[1:]}
            else:    
                step = {"action": words[0]}
            plan.append(step)

        return plan

# output = subprocess.run(["ls -n"], shell=True, capture_output=True, text= True)
# output = subprocess.run(["pyperplan","-H ",planner_name," ",domain_file, " ",problem_file], shell=True, capture_output=True, text= True)
# ./Metric-FF/ff -o ./pddl/domain.pddl -f ./pddl/problem.pddl

# class used to generate the PDDL files
class ParserPDDL():
    
    def __init__(self):
        self.path2pddl          = "./pddl"
        self.self.domain_file   = "./domain.pddl"
        self.problem_file       = "./problem.pddl"

    def parse_domain(self):
        pass
    
    def parse_problem_motion(self):
        pass
    
    def parse_problem_move_obj(self):
        pass




"""
                                                test section
"""

solver = SolverFF()
plan = solver.forward(domain_file="grid-world.pddl", problem_file="grid-world-p.pddl", verbose = False)
print(plan)
print(len(plan))
