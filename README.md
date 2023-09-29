# Pepper house assistant
Project of Human-Robot Interaction and Reasoning Agents for the Elective in AI course (second part).
The core of this work is the interaction with Pepper robot to perform simulated house tasks.
 This proposal includes:

 1. The development of a human-robot interaction module using NAOqi library and Choregraphe simulator.
 2. MODIM interaction using Pepper's tablet.
 3. Designing of a RA module for high-level action planning, and low-level motion planning.
 4. Designing a 2D house environment simulator to represent the execution of tasks.

The full description of the project is contained in the [report](https://github.com/FabrCas/HRI-RA_Pepper/blob/main/report.pdf).

A demo of the project's execution is available at the following [link](https://www.youtube.com/watch?v=gS-ZhO2bwkg)


## Required Choregraphe installation
For the execution is necessary the installation of Choregraphe simulator. 
follow the instructions at this [link](http://doc.aldebaran.com/2-8/software/choregraphe/installing.html)
 
## Required Pygame

    pip install pygame 

## Required metric FF planner
Required the usage of FF planning software. downloadable at page:
https://fai.cs.uni-saarland.de/hoffmann/ff/Metric-FF.tgz
Place the file in the following folder:
from command line

    mkdir Metric-FF
    cd Metric-FF
    gunzip Metric-FF.tgz
    tar -xvf Metric-FF.tar
    make


## Setup Pepper Environment
0. Install docker
```
curl -fsSL get.docker.com -o get-docker.sh
sudo sh get-docker.sh
rm get-docker.sh
sudo usermod -aG docker $USER
```

1. Clone

```
git clone https://bitbucket.org/iocchi/hri_software.git
```

2. Download files

[NaoQi](https://drive.google.com/file/d/11BKWwQe1uLxf3aVoEP1xJsgcUfIX-bYY), 
[Ctc](https://drive.google.com/file/d/1D9oXwiA1vYKGFO7qh81vVsRO189AGZvd),
[PyNaoQi](https://drive.google.com/file/d/18uqf8iAfqnzRZHS206oSAWFYhCgoZ11p)

place them in ```docker/downloads``` folder.

3. Download pepper tools

```
mkdir -p $HOME/src/Pepper
cd $HOME/src/Pepper
git clone https://bitbucket.org/mtlazaro/pepper_tools.git
```
4. Create a folder `$HOME/playground` that will be shared with the docker container.

```
mkdir -p $HOME/playground
```

4. Download modim folder and put it in `$HOME/src`

``` 
git clone https://bitbucket.org/mtlazaro/modim.git 
```
5. Create a playground folder for new demo files (default `$HOME/playground`) and `playground/html` for HTML files

```
mkdir -p $HOME/playground/html
cd $HOME/playground/html
cp -a $HOME/src/modim/demo/sample .
```

6. Go to Dockerfile in `hri_software/docker` and add environment `MODIM_HOME`, in row 96, after ` ENV PEPPER_TOOLS_HOME`

```
ENV MODIM_HOME /home/robot/src/modim
```

7. Do build, go to `hri_software/docker` and build image

```
./build.bash
```

8. Modify file `run.bash` in `hri_software/docker`, add in row 16

```
 MODIM_HOME=$HOME/src/modim
```

and in row 47 of the same file add

```
-v $MODIM_HOME:/home/robot/src/modim
```

9. Run image

```
./run.bash
```

10. Launch Docker 
```
docker exec -it pepperhri tmux
```

## Execution
1. Launch house simulator
```
python ./2DPathSimulator/sim_launcher.py
```
2. Launch Choregraphe
Go to `path_to/softbank`and execute:
```
./choregraphe-bin
```
3. Launch docker
Go to `path_to/hri_software/docker` and execute:
```
./run.bash
```
to start the docker image, open terminal and run:

```
docker exec -it pepperhri tmux
```
4. Launch modim server 
Split windows using command `tmux split-window` and:
In one terminale go to `$HOME/src/modim/src/GUI` and run 
```
python ws_server.py
```
5. Launch NAOqi
In another terminal launch NAOqi to `path_to/hri_software/docker/downloads/naoqi-sdk-2.5.5.5-linux64` with the folloing command:
```
./naoqi
```
6. Launch project
move to playground folder `cd path_to/playground` and run the main file

```
python main.py 
```
