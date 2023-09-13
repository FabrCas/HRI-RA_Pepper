import os
from naoqi import ALProxy



# take from env variables if available, otherwise define and write temporal env variables
pip = os.getenv('PEPPER_IP')
if pip is None:
	pip = "127.0.0.1" 	# localhost
	os.environ['PEPPER_IP'] = pip

pport = os.getenv('PEPPER_PORT')
if pport is None:
	pport = 9559 		# default port
	os.environ['PEPPER_PORT'] = str(pport)

# define the connection URL
connection_url = "tcp://" + pip + ":" + str(pport)



# load  the services
motion_service = ALProxy("ALMotion", pip, pport)
anim_speech_service = ALProxy("ALAnimatedSpeech", pip, pport)
robot_posture_service = ALProxy("ALRobotPosture", pip, pport)


						# head motion code
jointNames = ["HeadYaw", "HeadPitch"]
angles = [1.6, -0.2]
times  = [5.0, 5.0]
isAbsolute = True
motion_service.angleInterpolation(jointNames, angles, times, isAbsolute)

						# animated speech
configuration = {"bodyLanguageMode":"contextual"}
anim_speech_service.say("Hello. How are you?", configuration)


						# posture

posture = "Stand"   # go back to normal posture
speed = 0.7
robot_posture_service.goToPosture(posture,speed)
