#!/bin/bash
cd hri_software/docker
./run.bash
docker exec -it pepperhri tmux a
cd ../..
