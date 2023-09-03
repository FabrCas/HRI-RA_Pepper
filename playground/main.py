import os
import sys
import time
import signal
from pepperSocket import SimSocket

# main loop in the docker iso execution (python 2.7)
running_ended =  False


def get_connectionData():
	# take from env variables	
	pip = os.getenv('PEPPER_IP')
	if pip is None: PEPPER_IP = "127.0.0.1" 	# localhost
	pport = os.getenv('PEPPER_PORT')
	if pport is None: PEPPER_PORT = 9559 		# default port
	connection_url = "tcp://" + pepper_ip + ":" + str(pepper_port)
	return pip, pport, connection_url

def init_AppSession(connection_url):   # not required initialization if you use pepper_tools
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