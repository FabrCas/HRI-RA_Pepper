import threading
import time
import os
import json


#                                               python 2.7.17 code

class SimSocket(object):
    
    def __init__(self):
        super(SimSocket, self).__init__()
        # look for /home/faber/Documents/EAI2/tmp/...
        self.pipe_path_HS2P = "tmp/pipe_sim_HS2P"      # house simulator to pepper simulator
        self.pipe_path_P2HS = "tmp/pipe_sim_P2HS"      # pepper simulator to house simulator
       

        self.path2pipes = "./../EAI2Host"   # from playground folder
        
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
    

    def setPepperServices(self, animations_service, tts_service):
        self.animations_service = animations_service
        self.tts_service = tts_service

    def createFIFO(self, path):
        

        # go back to home relative path
        # if not "EAI2" in os.getcwd():        

        # print("Current location (cwd): {}".format(os.getcwd()))
        os.chdir("./..")
        os.chdir("./EAI2Host")
        # print("Current location (cwd): {}".format(os.getcwd()))

            
        # create os pipe file if does not exist
        if not os.path.exists(self.path2pipes):
            os.mkfifo(path, self.mode)
        
    def send_command(self, command):
        # try to parse json object to string
        if not(type(command) is str) and not(command is None):  
            command = json.dumps(command)       # from dict/list to stirng 

        # send command of define from input and send
        with open(self.pipe_path_P2HS, "w") as pipe:
            # while True:
            if command is None:
                command = raw_input("Enter a command to send: ")
            
            pipe.write(command)    
            pipe.flush()
            print("command has been flushed")
    
    def receive_command(self):
        with open(self.pipe_path_HS2P, "r") as pipe:
            while True:
                command = pipe.readline() # .strip()
                if command:
                    print("Received command: {}".format(command))
                    self.command_list.append(command)

                    # do something with the command
                                            
                    if "microphone" in command:                                     #TODO
                        status = command.split()[1]
                        print("changing microphone status to {}".format(status))    
                    elif "sleep" in command:                                        #TODO
                        status = command.split()[1]             
                        print("changing sleep status to {}".format(status))     

                    elif "none plan" in command.strip().lower():                                          #TODO (text to speech message)
                        self.tts_service.say("I cannot execute the task, please give me more information", _async=True)

                    elif "pepper open door" in command.strip().lower():
                        self.animations_service.interactDoor()

                    elif "pepper close door" in command.strip().lower():
                        self.animations_service.interactDoor()

                    elif "pepper open window"in command.strip().lower():
                        self.animations_service.interactWin()

                    elif "pepper close window"in command.strip().lower():
                        self.animations_service.interactWin()

                    elif "pepper grab" in command.strip().lower():
                        self.animations_service.search()
                        self.animations_service.grab()

                    elif "pepper place" in command.strip().lower():
                        self.animations_service.search()
                        self.animations_service.place()

                    
                                
                    
                                                            
 
"""
                                                test section
"""


testing     = 1
test_send   = 1

if __name__ == "__main__" and testing:         
    # print((os.getcwd()))
    process = SimSocket()

    #   [request]
    if test_send:
        while True:
            process.send_command(None)

    #   [receive]
    else:
        while True:
            print("-")
            time.sleep(5)