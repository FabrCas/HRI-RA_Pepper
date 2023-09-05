import os
import sys
import time
import signal
from pepperSocket import SimSocket

# main loop in the docker iso execution (python 2.7)
running_ended =  False


def get_connectionData():
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


# intialization: not required if you use pepper_tools
def init_AppSession(connection_url):   
    app = qi.Application(["App", "--qi-url=" + connection_url ])
    app.start()             
    session = app.session
    return app, session

def handler_sigint(sig, frame):
    print('\nYou pressed Ctrl+C!')
    # sys.exit(0)
    global running_ended
    running_ended = True


def main():
	socket_simulator = SimSocket()
	while True:
		if running_ended:break

		# 3 different types of command to send
		# add knowledge		-> i.e [{'object':'smartphone', 'room':"bedroom", 'furniture':"bed"}, {'object':'glasses', 'room':"toilet", 'furniture':"sink"}, ...]
		# remove knowledge	-> i.e ["smartphone", "glasses"]
		# perform task		-> i.e [{"type": "move_object", "args": ['glasses', "table_living"], "free hands": True}, ...]

		command = ""
		text_input = raw_input("Enter 1(add), 2(remove), 3(task) or exit\n")

		if text_input.strip().lower() 	== "1":
			command = [{'object':'smartphone', 'room':"bedroom", 'furniture':"bed"}, {'object':'glasses', 'room':"toilet", 'furniture':"sink"}]
		elif text_input.strip().lower() == "2":
			command = ["smartphone", "glasses"]
		elif text_input.strip().lower() == "3":
			command = [{"type": "move_object", "args": ['glasses', "table_living"], "free hands": True}]
		elif text_input.strip().lower() == "exit":
			print("terminating execution...")
			break

		socket_simulator.send_command(command)



if __name__ == "__main__":

	signal.signal(signal.SIGINT, handler_sigint)
	print("Python version: {}".format(sys.version))
	start_exe_time = time.time()
	main()
	end_exe_time = time.time()
	print("Execution ended, running time: {} [s]".format(round((end_exe_time - start_exe_time), 3)))