import os, sys

sys.path.append(os.getenv('PEPPER_TOOLS_HOME')+'/cmd_server')

import pepper_cmd
from pepper_cmd import *

begin()

pepper_cmd.robot.say('Hello')
pepper_cmd.robot.say('Porco schifo e uno sballo mi piasce')


end()
