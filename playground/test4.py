import os, sys
sys.path.append(os.getenv('PEPPER_TOOLS_HOME')+'/cmd_server')
import qi


# test without peppertools


# definition

pepper_ip = os.getenv('PEPPER_IP')
pepper_port = int(os.getenv('PEPPER_PORT'))
connection_url = "tcp://" + pepper_ip + ":" + str(pepper_port)


app = qi.Application(["App", "--qi-url=" + connection_url ])
app.start()          
session = app.session
print("Connection to Naoqi estabilished")

memory_service=app.session.service("ALMemory")


