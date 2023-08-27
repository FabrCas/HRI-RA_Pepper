import threading
import time
import os


class secondSocket(object):
    
    def __init__(self):
        super().__init__()
        # look for /home/faber/Documents/EAI2/tmp/...
        self.pipe_path_HS2P = "./tmp/pipe_sim_HS2P"      # house simulator to pepper simulator
        self.pipe_path_P2HS = "./tmp/pipe_sim_P2HS"      # pepper simulator to house simulator
       
        
        self.mode  = 0o600 # octal encode 
        
        # create pipes
        self.createFIFO(self.pipe_path_HS2P)
        self.createFIFO(self.pipe_path_P2HS)
        
        # list for command received during the exectuion
        self.command_list = []
        
    
        # create a new deamon thread to listen
        #time.sleep(0.2)
        listener_thread = threading.Thread(target=self.receive_command)
        listener_thread.daemon = True
        listener_thread.start()
        
    # function to exe the commands as a queue of instructions
    def exe_commmands(self):
        while len(self.command_list) != 0:
            command = self.command_list.pop(0)
            # if self.interpreter is not None:
            self.interpreter.execute(command)
            
    def setInterpreter(self, interpreter):
        self.interpreter = interpreter     
        
    def createFIFO(self, path):
        # go back to path pointer to ./EAI2
        if "2DPathSimulator" in os.getcwd():
            os.chdir("../")
            print(f"Current location (cwd): {os.getcwd()}")
        
        if not "EAI2" in os.getcwd():
           print("changed location to EAI2")
           os.chdir('./Documents/EAI2')
           
        # print(f"Looking for pipe in -> {os.getcwd()}")
        
        if not os.path.exists("./tmp/"):
            print("not exists tmp folder")
            os.mkdir('./tmp/')
            
        # create os pipe file if does not exist
        if not os.path.exists(path):
            os.mkfifo(path, self.mode)
        
    def send_command(self, command):
        print(os.getcwd()) 
        with open(self.pipe_path_P2HS, "w") as pipe:
            # while True:
            if command is None:
                command = input("Enter a command to send: ")
            
            pipe.write(command + "\n")    
            pipe.flush()
            print("command has been flushed")
    
    def receive_command(self):
        with open(self.pipe_path_HS2P, "r") as pipe:
            while True:
                command = pipe.readline() # .strip()
                if command:
                    print(f"Received command: {command}")
                
                self.command_list.append(command)
                # do something with the command
 
 
"""
                                                test section
"""
testing = 1
if testing:              
    print(os.getcwd())
    process = secondSocket()
    test_send = True


    #   [request]
    if test_send:
        while True:
            process.send_command(None)

    #   [receive]
    else:
        while True:
            print("-")
            time.sleep(5)

