import os
import sys
from naoqi import ALProxy
from services import Touch, Sonar, Motion
import qi 

sys.path.append(os.getenv('PEPPER_TOOLS_HOME')+'/cmd_server')
import pepper_cmd
from pepper_cmd import *


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



# connection and load session services
app = qi.Application(["App", "--qi-url=" + connection_url ])
app.start()             
session = app.session


memory_service 			=   session.service("ALMemory")
audioPlayer_service	 	= 	session.service("ALAudioPlayer")
motion_service 			= 	session.service("ALMotion")
dialog_service			= 	session.service('ALDialog')
anim_speech_service 	= 	session.service("ALAnimatedSpeech")
robot_posture_service 	= 	session.service("ALRobotPosture")
touch_service 			= 	session.service("ALTouch")

# asr_service  			=	session.service("ALSpeechRecognition")   # does not work for simulation kek 



activate = [0,0,0,0,0,1]

						# head motion code
if activate[0]:
	jointNames = ["HeadYaw", "HeadPitch"]
	angles = [1.6, -0.2]
	times  = [5.0, 5.0]
	isAbsolute = True
	motion_service.angleInterpolation(jointNames, angles, times, isAbsolute)

						# animated speech
if activate[1]:
	configuration = {"bodyLanguageMode":"contextual"}
	anim_speech_service.say("Hello. How are you?", configuration)


						# posture
if activate[2]:
	posture = "Stand"   # go back to normal posture
	speed = 0.7
	robot_posture_service.goToPosture(posture,speed)


						# touch sensors
if activate[3]:
	def onTouched(value):
		print("touched: {}".format(value))

	# # callback function
	anyTouch = memory_service.subscriber("TouchChanged")
	idAnyTouch = anyTouch.signal.connect(onTouched)
	touch_service = Touch(memory_service)
	touch_service.act("Head_mid")

	# anyTouch.signal.disconnect(idAnyTouch)			# disable touch

						# sonar sensor 
if activate[4]:
	sonar = Sonar(memory_service)
	sonar.setPosRobot((4,1))   # change pepper position for compute correctly the distances
	sonar.setPosHuman((5,8))

	sonar.setSonarFrontal()
	sonar.get_values()

if activate[5]:
	print("motion test")

	# Wake up robot
	motion_service.wakeUp()

	# Send robot to Pose Init
	robot_posture_service.goToPosture("StandInit", 0.5)

	x     = 1.0	
	y     = 0.0
	theta = 0.0
	# frequency = 1.0
	motion_service.moveToward(x, y, theta)

	# If we don't send another command, he will move forever
	# Lets make him slow down(step length) and turn after 3 seconds
	time.sleep(3)
	x     = 0.5
	theta = 0.6
	motion_service.moveToward(x, y, theta)

	# Lets make him slow down(frequency) after 3 seconds
	time.sleep(3)
	frequency = 0.5
	motion_service.moveToward(x, y, theta)

	# Lets make him stop after 3 seconds
	time.sleep(3)
	motion_service.stopMove()

	# Go to rest position	
	motion_service.rest()


	# motion = Motion(motion_service)
	# motion.setSpeed(lin_vel = 0.001, ang_vel = 0, motion_time = 5)


	# begin() # connect to robot/simulator with IP in PEPPER_IP env variable



	# pepper_cmd.robot.startSensorMonitor()  # non-blocking
	# pepper_cmd.robot.startLaserMonitor()   # non-blocking

	# pepper_cmd.robot.turn(2)
	# pepper_cmd.robot.setSpeed(0,1.5,0,4,stopOnEnd=True)

	# end()
