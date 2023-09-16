connect to choregraphe:
after ever launched all the software needed (look the instructions wrote before), in the choregraphe window, first go clink on connection> connect to a virtual robot.
then connection> connect to... and select the simulated robot on the port 9559 and localhost IP


launch app tablet:

# modim option 1) server
./start_modim.sh	-> start modim server
./launch_modim.sh 	-> load the modim application at localhost IP


# modim option 2) local
in tmux env use the command "tmux split-window" to split and have another prompt

go to $HOME/src/modim/src/GUI:
cd ./../src/modim/src/GUI

local server: python ws_server.py

launch the python script using the main project (through dialogue) python demo.py 
