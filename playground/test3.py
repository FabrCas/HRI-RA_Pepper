#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 22:06:46 2022

@author: faber
"""
import os, sys
sys.path.append(os.getenv('PEPPER_TOOLS_HOME')+'/cmd_server')

from naoqi import ALProxy
import pepper_cmd
from pepper_cmd import *


pepper_ip = os.getenv('PEPPER_IP')
pepper_port = int(os.getenv('PEPPER_PORT'))


""" ----------------------- start: FUNCTIONS ----------------------------- """
def take_photos(number_pictures):
    
    # try:
    #     photoCaptureProxy = ALProxy("ALPhotoCapture", pepper_ip, pepper_port)
    # except Exception as error:
    #     print("Error when creating ALPhotoCapture proxy:")
    #     print(str(error))
    #     exit(1)
    # photoCaptureProxy.setResolution(2)
    # photoCaptureProxy.setPictureFormat("jpg")
    # photoCaptureProxy.takePictures(number_pictures, "/home/Desktop", "test_image")
    begin()
    pepper_cmd.robot.sax()
    end()
def say(message):
    try:
        tts = ALProxy("ALTextToSpeech", pepper_ip, pepper_port)
    except Exception as error:
        print("Error in the ALTextToSpeech proxy:")
        print(str(error))
        exit(1)
        
    tts.say(message)

""" ----------------------- end: FUNCTIONS ------------------------------- """



""" ----------------------- start: test ---------------------------- """
if True: 
    print(pepper_ip)
    print(pepper_port)
""" ----------------------- end: test ------------------------------ """



""" ----------------------- start: execution ---------------------------- """
# say("Hello world!")
take_photos(3)
exit(0)
""" ----------------------- end: execution ------------------------------ """