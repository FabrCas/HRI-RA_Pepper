import os,sys,qi

sys.path.append(os.getenv('PEPPER_TOOLS_HOME')+'/cmd_server')
import pepper_cmd
from pepper_cmd import * 

"""
Configuration section 
"""

# take from env variables
pip = os.getenv('PEPPER_IP')
if pip is None: PEPPER_IP = "127.0.0.1" # localhost
pport = os.getenv('PEPPER_PORT')
if pport is None: PEPPER_PORT = 9559 	# default port

print ("pip -> {}".format(pip))
print ("pport -> {}".format(pport))


if __name__ == "__main__":
	print("connecting to pepper...")

	try:
		"""
		url = "tcp://" + pip + ":" + str(pport)

		print("connection URL -> {} connection_url".format(url))
		
		app = qi.Application(["App", "--qi-url=" + url])
		app.start()
		session = app.session
		
		"""
		if False:
			tts_service = session.service("ALTextToSpeech")
			tts_service.setLanguage("English")
			tts_service.setParameter("speed", 90)
			tts_service.say("Hello. How are you?, configuration")


		begin()

		pepper_cmd.robot.startSensorMonitor()

		#app.run()
		

		end()
	except RuntimeError:
		print("Can't connect to Naoqi")