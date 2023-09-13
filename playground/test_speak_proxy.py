#!/usr/bin/env python3

# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 22:06:46 2022

@author: faber
"""

import os, sys
sys.path.append(os.getenv('PEPPER_TOOLS_HOME')+'/cmd_server')
if os.getenv('PEPPER_PORT') is None:
    os.environ["PEPPER_PORT"] = "9559"

# sys.path.append(os.path.join(os.getenv('PEPPER_TOOLS_HOME'),'/cmd_server'))
# print(os.getcwd())
# print(os.getenv('PEPPER_TOOLS_HOME'))

from naoqi import ALProxy  #The ALProxy object lets you create a proxy to a module.

import pepper_cmd
from pepper_cmd import *


pepper_ip       = os.getenv('PEPPER_IP')
pepper_port     = int(os.getenv('PEPPER_PORT'))
connection_url  = "tcp://" + pepper_ip + ":" + str(pepper_port)



""" ----------------------- start: FUNCTIONS ----------------------------- """

def say(message):
    # start the 
    try:
        tts = ALProxy("ALTextToSpeech", pepper_ip, pepper_port)
    except Exception as error:
        print("Error in the ALTextToSpeech proxy:")
        print(str(error))
        exit(1)

    tts.say(message)

def init_AppSession(connection_url):
    try:
        connection_url = "tcp://" + pepper_ip + ":" + str(pepper_port)
        # app = qi.Application(["Module name", "--qi-url=" + connection_url ])
        
        app = qi.Application(["App", "--qi-url=" + connection_url ])
        app.start()             
        session = app.session
        print("Connection to Naoqi estabilished")
        return app, session
    except RuntimeError:
        print("Can't connect to Naoqi")



""" ----------------------- end: FUNCTIONS ------------------------------- """



""" ----------------------- start: test ---------------------------- """
if True: 
    print(pepper_ip)
    print(pepper_port)
""" ----------------------- end: test ------------------------------ """



# check connection to naoqi
# try:
#         connection_url = "tcp://" + pepper_ip + ":" + str(pepper_port)
#         app = qi.Application(["Module name", "--qi-url=" + connection_url ])
#         print("Connection to Naoqi verified")
# except RuntimeError:
#     print("Can't connect to Naoqi")
# if you use pepper_tools is not required
# app, session = init_AppSession(connection_url)


""" ----------------------- start: execution ---------------------------- """
say("Hello world!")



exit(0)


# begin()
#pepper_cmd.robot.say("this is from pepper cmd") 
#pepper_cmd.sax()
#end()

""" ----------------------- end: execution ------------------------------ """



"""
                               [how to use pepper tools]
export PEPPER_IP and PEPPER_PORT
from pepper_cmd import *
begin()
pepper_cmd.robot.<fn>()        # use modules
end()
"""
