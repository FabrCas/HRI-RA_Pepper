import os
import sys
from naoqi import ALProxy
from services import Touch, Sonar, Motion, Animations
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
tts_service 			= 	session.service("ALTextToSpeech")
robot_posture_service 	= 	session.service("ALRobotPosture")
touch_service 			= 	session.service("ALTouch")

player_service          =   session.service("ALAudioPlayer")

# asr_service  			=	session.service("ALSpeechRecognition")   # does not work for simulation kek 
# navigation_service 		=	session.service("ALNavigation")      # does not work for simulation kek2


activate = [0,0,0,
			0,0,0,
			0,0,0,1]

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


	navigation_service.startFreeZoneUpdate()

	# success = motion_service.setCollisionProtectionEnabled("Body", False)
	# if(not success):
	# 	print("Failed to disable collision protection")


	x     = 1.0	
	y     = 0.0
	theta = 0.0
	motion_service.moveToward(x, y, theta)

	# If we don't send another command, he will move forever
	# Lets make him slow down(step length) and turn after 3 seconds
	time.sleep(3)
	x     = 0.5
	theta = 0.6
	motion_service.moveToward(x, y, theta)

	# Lets make him slow down(frequency) after 3 seconds
	time.sleep(3)
	motion_service.moveToward(x, y, theta)

	# Lets make him stop after 3 seconds
	time.sleep(3)
	motion_service.stopMove()

	# motion = Motion(motion_service)
	# motion.setSpeed(lin_vel = 0.001, ang_vel = 0, motion_time = 5)
	# begin() # connect to robot/simulator with IP in PEPPER_IP env variable
	# pepper_cmd.robot.startSensorMonitor()  # non-blocking
	# pepper_cmd.robot.startLaserMonitor()   # non-blocking
	# pepper_cmd.robot.turn(2)
	# pepper_cmd.robot.setSpeed(0,1.5,0,4,stopOnEnd=True)
	# end()

if activate[6]:
	# Wake up robot
    # motion_service.wakeUp()

    # # Send robot to Pose Init
    # posture_service.goToPosture("StandInit", 0.5)

    # # Go to rest position
    # motion_service.rest()

	animations = Animations(motion_service, robot_posture_service)

	# animations.search()
	# animations.grab()


	# animations.search()
	# animations.place()

	animations.dance()
	# animations.interactWin()

if activate[7]:

	def callback_ans(answer_message):
		print(answer)
		pass

	def callback_inp(input_message):
		print(input_message)
		pass

	touch_service = Touch(memory_service)

	print(os.getcwd())

	dialog_service.setLanguage('English')
	project_path  = "/home/faber/playground/"
	topic_path = project_path + "topics/main.top"

	print(topic_path)	

	topic_path = topic_path.decode('utf-8')
	topic_name = dialog_service.loadTopic(topic_path.encode('utf-8'))

	# Adds the specified topic to the list of the topics that are currently used by the dialog engine to parse inputs of human.
	dialog_service.activateTopic(topic_name)

	# Start dialog
	# Starts the dialog engine. Starts the speech recognition on robot.
	# The dialog engine will stop when all subscribers will have unsubscribed.
	dialog_service.subscribe('house_pepper')
	
	ans = memory_service.subscriber("Dialog/LastAnswer")
	ans.signal.connect(callback_ans)
	inp = memory_service.subscriber("Dialog/LastInput")
	inp.signal.connect(callback_inp)

	flag_stop = True

	while flag_stop:
		try:
			user_input = raw_input("Interact with the robot:\nTo terminate the conversation insert [stop, finish] or touch Pepper's hands or head inserting [Head, LHand, RHand]\n")

		except KeyboardInterrupt:
			flag_stop = False

			# Stop the dialog engine, then deactivate and unlaod topic
			dialog_service.unsubscribe('house_pepper')
			dialog_service.deactivateTopic(topic_name)
			dialog_service.unloadTopic(topic_name)   

			# continue and exit
			continue

		if ("stop" in user_input.strip().lower()) or ("finish" in user_input.strip().lower()):

			flag_stop = False

			# Stop the dialog engine, then deactivate and unlaod topic
			dialog_service.unsubscribe('house_pepper')
			dialog_service.deactivateTopic(topic_name)
			dialog_service.unloadTopic(topic_name)   

			# continue and exit
			continue
		
		# touch actions by the user
		elif "head" in user_input.strip().lower():
			if touch_service.set("Head"):
				tts_service.say("You touched my head", _async=True)    
		
		elif "lhand" in  user_input.strip().lower():
			if touch_service.set("LHand"):
                # tts_service.say("?"+" "*5, _async=True)    
				tts_service.say("You touched my left hand", _async=True) 

		elif "rhand" in user_input.strip().lower():
			if touch_service.set("RHand"):
                # tts_service.say("?"+" "*5, _async=True)   
				tts_service.say("You touched my right hand", _async=True) 


if activate[8]:
	project_path  = "/home/faber/playground/"
	static_path = project_path + "static/"
	song_path = static_path + "Smash_Mouth_-_All_Star.wav"

	print(static_path)


	# fileId = player_service.loadFile(song_path)
	# player_service.play(fileId, _async=True)

	player_service.playFile(song_path, _async=True)

	# print(ao)s

	time.sleep(1)

	# player_service.stop()
	# player_service.stop(ao)
	# player_service.pause()

	for i in range(100):
		try:
			player_service.stop(i)
		except:
			pass

if activate[9]:   # modim test
	project_path  = "/home/faber/playground/"	
	modim_path = project_path + "modim/app"

	scripts = "modim/app/scripts"
	demo = "demo.py"

	print(scripts)
	# move to script folder of the app
	os.chdir(scripts)

	os.system("python " + demo)

	# go back to playground
	os.chdir("./../../..")

	print(os.getcwd())

	# ------




