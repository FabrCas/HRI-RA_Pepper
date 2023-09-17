import os
import sys
import time
import json
import subprocess
import signal
from pepperSocket import SimSocket					# RA module connection
from naoqi import ALProxy
from services import Touch, Sonar, Motion, Animations

# importing the SimSocket the default directory is EAI2Host


# if using pepper tools
sys.path.append(os.getenv('PEPPER_TOOLS_HOME')+'/cmd_server')
import pepper_cmd
from pepper_cmd import *


# initialize global variables
running_ended =  False # boolean flag for main loop in the docker iso execution (python 2.7)
config_task = None # empty global config coming from the interaction with the tablet
socket_simulator = SimSocket()

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
	modimg_app_path = "$HOME/playground/modim/app"


	os.environ['MODIM_HOME'] = modim_home_path
	os.environ['MODIM_APP'] = modimg_app_path


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
	print "answer: "+answer_message
	yes_kw = ["task", "tablet", "job", "assignment", "action"]

	if "goodbye" in answer_message.strip().lower():
		animations.greet()

	elif "launch" in answer_message.strip().lower():
		print("launching tablet application")
		launch_tablet()

	elif any(name in answer_message.strip().lower() for name in yes_kw):
		animations.yes()

	elif "here it is" in answer_message.strip().lower():
		print("starting music")
		# print(song_path)
		global fileId
		player_service.playFile(song_path, _async=True)
		animations.dance()

	# add knowledge acquisition
	elif "smartphone" in answer_message.strip().lower():
		command = add_knowledge("smartphone")
		print(command)
		socket_simulator.send_command(command)
	elif "glasses" in answer_message.strip().lower():
		command = add_knowledge("glasses")
		print(command)
		socket_simulator.send_command(command)


def callback_inp(input_message):
	print "input: "+input_message

	if "stop" in input_message.strip().lower():
		print("stopping music")
		for i in range(100):
			try:
				player_service.stop(i)
			except:
				pass
		animations.continue_dance = False


# ---------------------------------------- [utilities]
# predefined task one 
def get_task(number):

	# [{"type": "move_object", "args": ['glasses', "table_living"], "free hands": True}, ...]
	command = []
	if number == 1:      # simple motion
		t1 = {"type": "reach_room", "args": ['dining'], "free hands": True}
		t2 = {"type": "reach_position", "args": ['free_space'], "free hands": True}
		command = [t1,t2]

	elif number == 2:   # open windows
		t1 = {"type": "reach_position", "args": ['free_space'], "free hands": True}
		t2 = {"type": "close_window", "args": ['wl_dining'], "free hands": True}
		t3 = {"type": "close_window", "args": ['wr_dining'], "free hands": True}
		t4 = {"type": "open_window", "args": ['wl_bedroom'], "free hands": True}
		t5 = {"type": "open_window", "args": ['wr_bedroom'], "free hands": True}
		command = [t1,t2,t3,t4,t5]

	elif number == 3:  # move known
		t4 = {"type": "move_object", "args": ['cards', "table_kitchen"], "free hands": True}
		t5 = {"type": "reach_position", "args": ['sofa'], "free hands": True}
		command = [t1,t2,t3,t4,t5]

	elif number == 4: # move unknown object (need to acquire knowledge)
		t1 = {"type": "move_object", "args": ['smartphone', "desk_studio"], "free hands": True}
		t2 = {"type": "reach_position", "args": ['free_space'], "free hands": True}
		t3 = {"type": "reach_room", "args": ['studio'], "free hands": True}
		command = [t1,t2,t3]   

	else:
		print("wrong number selected")

	return command

def add_knowledge(what):
	command = []
	if "smartphone" in what:
		command.append({'object':'smartphone', 'room':"bedroom", 'furniture':"bed"})
	if "glasses" in what: 
		command.append({'object':'glasses', 'room':"toilet", 'furniture':"sink"})
	return command 


def filter_output(output):

	lines_output = output.split('\n')

	keywords = []
	for line in lines_output:
		if "reply:" in line.lower().strip():
			text = line.split("(")[1]
			text = text.replace(")","")
			keywords.append(text)
	return keywords

# ---------------------------------------- [init functions]




def launch_tablet(script_name = "demo.py"):   # page: file:///home/faber/playground/modim/app/index.html
	print "launching table application."  

	try:
		# move to script folder of the app, we are the EAI2host folder
		print(os.getcwd())
		print(local_script_path)
		os.chdir("./../playground/"+ local_script_path)

		# execute app
		os.system("python " + script_name)
		# output = subprocess.check_output(["python", script_name], universal_newlines=True)
		# interaction_keywords = filter_output(output)
		# print(interaction_keywords)

		# go back to EAI2Host
		os.chdir("./../../../../EAI2Host")
		# os.chdir("./../../../../playground")

		print(os.getcwd())

	except Exception as e:
		print("cannot find the tablet script")
		print(e)

	# unload
	try:
		dialog_service.unsubscribe('house_pepper')
	except:
		pass
	try:
		dialog_service.deactivateTopic("house-assistant")
	except:
		pass
	try:
		dialog_service.unloadTopic("house-assistant")
	except:
		pass

	# load again to repeat tablet execution
	project_path  = "/home/faber/playground/"
	topic_path = project_path + "topics/main.top"
	topic_path = topic_path.decode('utf-8')
	topic_name = dialog_service.loadTopic(topic_path.encode('utf-8'))
	dialog_service.activateTopic(topic_name) 	 
	dialog_service.subscribe(topic_name)

	# Flush command to execute
	# task = interaction_keywords[1]
	# print("task selected -> {}".format(task))



# initialization: not required if you use pepper_tools or call directly the ALProxy
def init_AppSession(connection_url):   
    app = qi.Application(["App", "--qi-url=" + connection_url ])
    app.start()             
    session = app.session
    return app, session


def main():
	
	pip, pport, connection_url = export_connectionData()

	# 						define paths
	global song_path, local_script_path, local_taskConfig_path, topic_path
	project_path  = "/home/faber/playground/"

	# topic path
	topic_path = project_path + "topics/main.top"

	# tablet app path
	modim_path = project_path + "modim/app"
	modim_script_path = modim_path + "/scripts"
	local_script_path = "./modim/app/scripts"
	local_taskConfig_path = "/config/modim_config.json"

	# music path
	static_path = project_path + "static/"
	song_path = static_path + "Smash_Mouth_-_All_Star.wav"

	running =  True  # main loop flag 

	# connection and load session services
	try:
		app, session = init_AppSession(connection_url)
	except:
		print ("\nCan't connect to Naoqi at IP {} (port {}).\nPlease check your script's arguments."
			" Run with -h option for help.\n".format(pip, pport))
		sys.exit(1)

	# load services using ALProxy
	
	global player_service
	global dialog_service
	memory_service 			= 	session.service("ALMemory")
	motion_service			=   session.service("ALMotion")
	posture_service         = 	session.service("ALRobotPosture")
	tts_service 			= 	session.service("ALTextToSpeech")
	dialog_service 			=	session.service('ALDialog')
	player_service			=	session.service('ALAudioPlayer')



	# configure services
	tts_service.setLanguage("English")
	tts_service.setVolume(1.0)
	tts_service.setParameter("speed", 1.0)
	dialog_service.setLanguage('English')

	# load custom services
	global animations

	touch 			= Touch(memory_service)
	animations 		= Animations(motion_service, posture_service)
	sonar           = Sonar(memory_service)
	motion          = Motion(motion_service)

	# 							start demo
	# todo include animiations
	# animations.wakeUp()
	# animations.greet()
	# tts_service.say("Hello human, my name is Pepper and in this demo, i can show you my abilities as house assistant.")



	topic_path = topic_path.decode('utf-8')

	# global topic_name
	topic_name = dialog_service.loadTopic(topic_path.encode('utf-8'))

	
	dialog_service.activateTopic(topic_name) 	 
	dialog_service.subscribe('house_pepper')


	ans = memory_service.subscriber("Dialog/LastAnswer")
	ans.signal.connect(callback_ans)
	inp = memory_service.subscriber("Dialog/LastInput")
	inp.signal.connect(callback_inp)


	# socket house simulator, remove knowledge
	command_hs = ["smartphone", "glasses"]
	socket_simulator.send_command(command_hs)


	while running:
		if running_ended:break    # break if you press CTRL+C (SignInt)

		try:
			user_input = raw_input("Interact with the robot:\nTo terminate the conversation insert [end] or touch Pepper's hands or head inserting [Head, LHand, RHand]\n")

		except KeyboardInterrupt:

			running = False

			# Stop the dialog engine, then deactivate and unlaod topic
			dialog_service.unsubscribe('house_pepper')
			try:
				dialog_service.deactivateTopic(topic_name)
				dialog_service.unloadTopic(topic_name)
			except:
				for topic in dialog_service.getActivatedTopics():
					dialog_service.deactivateTopic(topic)
					dialog_service.unloadTopic(topic)

			   

			# continue and exit
			continue

		if ("end" in user_input.strip().lower()):

			running = False

			# Stop the dialog engine, then deactivate and unlaod topic
			try:
				dialog_service.unsubscribe('house_pepper')
			except:
				pass
			try:
				dialog_service.deactivateTopic(topic_name)
				dialog_service.unloadTopic(topic_name)   
			except:	
				for topic in dialog_service.getActivatedTopics():
					dialog_service.deactivateTopic(topic)
					dialog_service.unloadTopic(topic)   

			# continue and exit
			continue
		
		# touch actions by the user
		elif "head" in user_input.strip().lower():
			if touch.set("Head"):
				tts_service.say("You touched my head", _async=True)
				if motion_service.robotIsWakeUp():
					tts_service.say("This is my custom command for the rest, touch my head again to wake me", _async=True)
					animations.rest()
					tts_service.say("ZZZ \\pau=2000\\", _async=True)
				else:
					animations.wakeUp()
					tts_service.say("I'm awake now! Is nice to see you again!", _async=True)
		
		elif "lhand" in  user_input.strip().lower():
			if touch.set("LHand"):
                # tts_service.say("?"+" "*5, _async=True)    
				tts_service.say("You touched my left hand", _async=True) 
				tts_service.say("I can help you with anything?", _async=True) 

		elif "rhand" in user_input.strip().lower():
			if touch.set("RHand"):
                # tts_service.say("?"+" "*5, _async=True)   
				tts_service.say("You touched my right hand", _async=True) 
				tts_service.say("I can help you with anything?", _async=True)




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