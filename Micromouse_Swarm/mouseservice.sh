#!/bin/bash

### Sets up controlnet 
### Need to repeatedly execute python scripts??

export ServiceHOME=/home/theo/CORE/myservices
homefolder="$(pwd)"
#homefolder="/tmp/pycore.55045-n1.conf"
nodeid=`echo "$homefolder" | grep -Eo "[[:digit:]]+" | tail -n1` ## Need n1 to be wlan

python micromouse.py



########### Controlnet Setup ################
# Setup host to receive and subnet to send



