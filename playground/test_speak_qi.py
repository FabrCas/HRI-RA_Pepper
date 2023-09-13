import os,sys,qi
import naoqi
from time import sleep

sys.path.append(os.getenv('PEPPER_TOOLS_HOME')+'/cmd_server')
import pepper_cmd
from pepper_cmd import * 

"""
Configuration section 
"""

# take from env variables
pip = os.getenv('PEPPER_IP')
if pip is None: pip = "127.0.0.1" # localhost


pport = os.getenv('PEPPER_PORT')
if pport is None:
	pport = 9559 		# default port
	os.environ['PEPPER_PORT'] = str(pport)

if pport is None: pport = 9559 	# default port

print ("pip -> {}".format(pip))
print ("pport -> {}".format(pport))


if __name__ == "__main__":
	print("connecting to pepper...")

	try:
		url = "tcp://" + pip + ":" + str(pport)
		print("connection URL -> {} connection_url".format(url))
		app = qi.Application(["App", "--qi-url=" + url])
		app.start()
		session = app.session
	except Exception as e:
		print("Can't connect to Naoqi")
		print(e)
		
	# if True:
	tts_service = session.service("ALTextToSpeech")
	tts_service.setLanguage("English")
	tts_service.setParameter("speed", 90)
	tts_service.say("Hello. How are you?, configuration")


	app.run()	# will exit when the connection is over or i can use the method stop() with an handler to exit from application
	
	# app.stop()


	# command using pepper_tools
	# begin()
	# pepper_cmd.robot.startSensorMonitor()
	# end()
