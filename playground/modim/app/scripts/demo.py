import sys
import time
import os
import random
import json

try:
    sys.path.insert(0, os.getenv('MODIM_HOME')+'/src/GUI')
except Exception as e:
    print "Please set MODIM_HOME environment variable to MODIM folder."
    sys.exit(1)

# Set MODIM_IP to connnect to remote MODIM server

import ws_client
from ws_client import *


def i1():

    im.init()

    im.ask('welcome')  # wait for button

    a = im.ask("tasks")  #tasks

    if (a!='timeout'):
        im.execute(a)
        im.execute('goodbye')


        # if (a!='timeout'):
        # while(not(a=="exit")):
        #     im.execute(a)
        #     im.execute('welcome')
        #     a = im.ask("tasks")
        #     if (a=='timeout'): break

        # im.execute("exit")
        # im.execute('goodbye')



    im.init()
    

if __name__ == "__main__":

    mws = ModimWSClient()

    # local execution
    mws.setDemoPathAuto(__file__)
    # remote execution
    # mws.setDemoPath('<ABSOLUTE_DEMO_PATH_ON_REMOTE_SERVER>')

    print("---------------path--------------------")
    print(os.getcwd())
    print("---------------------------------------")

    mws.run_interaction(i1)


