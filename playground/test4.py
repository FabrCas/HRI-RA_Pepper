import os, sys
sys.path.append(os.getenv('PEPPER_TOOLS_HOME')+'/cmd_server')
import qi
from naoqi import ALProxy

if os.getenv('PEPPER_PORT') is None:
	os.environ["PEPPER_PORT"] = "9559"

# test without peppertools


# definition

pepper_ip = os.getenv('PEPPER_IP')
pepper_port = int(os.getenv('PEPPER_PORT'))
connection_url = "tcp://" + pepper_ip + ":" + str(pepper_port)


app = qi.Application(["App", "--qi-url=" + connection_url ])
app.start()       

session = app.session
print("Connection to Naoqi estabilished")


# memory_service= session.service("ALMemory")

   
# asr_service = session.service("ALSpeechRecognition")


# asr = ALProxy("ALSpeechRecognition", pepper_ip, pepper_port)

asr = ALProxy("ALSpeechRecognition", pepper_ip, pepper_port)

app.run()