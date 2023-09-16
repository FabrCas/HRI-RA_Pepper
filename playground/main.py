import os
import sys
import time
import signal
from pepperSocket import SimSocket					# RA module connection
from naoqi import ALProxy
from services import Touch, Sonar, Motion, Animations


# if using pepper tools
sys.path.append(os.getenv('PEPPER_TOOLS_HOME')+'/cmd_server')
import pepper_cmd
from pepper_cmd import * 


# paths from ./playground folder
modim_path = "./modim_app/"
topics_path = "./topics/"


running_ended =  False # boolean flag for main loop in the docker iso execution (python 2.7)


# ---------------------------------------- [environment functions]

def export_connectionData():
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
	return pip, pport, connection_url

def export_modimData():
	# /home/faber/src/modim/demo/README.md
	modim_home_path = "$HOME/src/modim"
	modimg_app_path = "$HOME/playground/modim_app/sample"

	modim_home = os.getenv("MODIM_HOME")
	modim_app  = os.getenv("MODIM_APP")

	if modim_home is None:
		os.environ['MODIM_HOME'] = modim_home_path
		modim_home = os.getenv("MODIM_HOME")
	if modim_app is None:
		os.environ['MODIM_APP'] = modimg_app_path
		modim_app  = os.getenv("MODIM_APP")

	return modim_home, mod



# ---------------------------------------- [callbacks]
def handler_sigint(sig, frame):
    print('\nYou pressed Ctrl+C!')
    # sys.exit(0)
    global running_ended
    running_ended = True


def callback_ans(answer_message):
	print(answer_message)
	
	pass

def callback_inp(input_message):
	print(input_message)
	pass
# ---------------------------------------- [init functions]

# initialization: not required if you use pepper_tools or call directly the ALProxy
def init_AppSession(connection_url):   
    app = qi.Application(["App", "--qi-url=" + connection_url ])
    app.start()             
    session = app.session
    return app, session


def main():
	socket_simulator = SimSocket()
	pip, pport, connection_url = export_connectionData()

	# define paths
	project_path  = "/home/faber/playground/"
	topic_path = project_path + "topics/main.top"
	modim_path = project_path + "modim/app"

	running =  True  # main loop flag 

	# connection and load session services
	try:
		app, session = init_AppSession(connection_url)
	except:
		print ("\nCan't connect to Naoqi at IP {} (port {}).\nPlease check your script's arguments."
			" Run with -h option for help.\n".format(pip, pport))
		sys.exit(1)

	# load services using ALProxy
	memory_service 			= 	session.service("ALMemory")
	motion_service			=   session.service("ALMotion")
	posture_service         = 	session.service("ALRobotPosture")
	tts_service 			= 	session.service("ALTextToSpeech")
	dialog_service 			=	session.service('ALDialog')



	# configure services
	tts_service.setLanguage("English")
	tts_service.setVolume(1.0)
	tts_service.setParameter("speed", 1.0)
	dialog_service.setLanguage('English')

	# load custom services
	touch 			= Touch(memory_service)
	animations 		= Animations(motion_service, posture_service)
	sonar           = Sonar(memory_service)
	motion          = Motion(motion_service)

	# 							start demo
	# animations.wakeUp()
	# animations.greet()
	# tts_service.say("Hello human, my name is Pepper and in this demo, i can show you my abilities as house assistant.")


	topic_path = topic_path.decode('utf-8')
	topic_name = dialog_service.loadTopic(topic_path.encode('utf-8'))
	dialog_service.activateTopic(topic_name)
	dialog_service.subscribe('house_pepper')

	ans = memory_service.subscriber("Dialog/LastAnswer")
	ans.signal.connect(callback_ans)
	inp = memory_service.subscriber("Dialog/LastInput")
	inp.signal.connect(callback_inp)

	while running:
		if running_ended:break    # break if you press CTRL+C (SignInt)

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

			running = False

			# Stop the dialog engine, then deactivate and unlaod topic
			dialog_service.unsubscribe('house_pepper')
			dialog_service.deactivateTopic(topic_name)
			dialog_service.unloadTopic(topic_name)   

			# animations.rest()
			# continue and exit
			continue
		
		# touch actions by the user
		elif "head" in user_input.strip().lower():
			if touch.set("Head"):
				tts_service.say("You touched my head", _async=True)    
		
		elif "lhand" in  user_input.strip().lower():
			if touch.set("LHand"):
                # tts_service.say("?"+" "*5, _async=True)    
				tts_service.say("You touched my left hand", _async=True) 

		elif "rhand" in user_input.strip().lower():
			if touch.set("RHand"):
                # tts_service.say("?"+" "*5, _async=True)   
				tts_service.say("You touched my right hand", _async=True) 




		# ----------------------------- interaction with house simulator
		if False:
			# 3 different types of command_hs to send
			# add knowledge		-> i.e [{'object':'smartphone', 'room':"bedroom", 'furniture':"bed"}, {'object':'glasses', 'room':"toilet", 'furniture':"sink"}, ...]
			# remove knowledge	-> i.e ["smartphone", "glasses"]
			# perform task		-> i.e [{"type": "move_object", "args": ['glasses', "table_living"], "free hands": True}, ...]


			text_input = raw_input("Enter 1(add), 2(remove), 3(task) or exit\n")

			command_hs = ""


			if command_hs != "":

				if text_input.strip().lower() 	== "1":
					command_hs = [{'object':'smartphone', 'room':"bedroom", 'furniture':"bed"}, {'object':'glasses', 'room':"toilet", 'furniture':"sink"}]
				elif text_input.strip().lower() == "2":
					command_hs = ["smartphone", "glasses"]
				elif text_input.strip().lower() == "3":
					command_hs = [{"type": "move_object", "args": ['glasses', "table_living"], "free hands": True}]
				elif text_input.strip().lower() == "exit":
					print("terminating execution...")
					break

				socket_simulator.send_command(command_hs)



if __name__ == "__main__":

	signal.signal(signal.SIGINT, handler_sigint)
	print("Python version: {}".format(sys.version))
	start_exe_time = time.time()
	main()
	end_exe_time = time.time()
	print("Execution ended, running time: {} [s]".format(round((end_exe_time - start_exe_time), 3)))