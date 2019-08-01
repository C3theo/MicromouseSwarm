#!/bin/bash

### Sets up controlnet 
### Need to repeatedly execute python scripts??

export ServiceHOME=/home/theo/CORE/myservices
homefolder="$(pwd)"
#homefolder="/tmp/pycore.55045-n1.conf"
nodeid=`echo "$homefolder" | grep -Eo "[[:digit:]]+" | tail -n1` ## Need n1 to be wlan

#sleep certain period to wait for routing complete
sleep 8

#monitor traffic through upd port 50000 for 10 seconds
duration=10

#-E ntime
#    Terminate after ntime seconds
#-c npacket
#    Terminate program after reading npacket packets. 

# -p prot[,port..][:prot[,port..]..
#    Only dump packets with specific protocols and ports. For example, -p1:6:17 dumps only packets with protocols 1 (icmp), 6 (tcp) and 17 (udp). You can also break down udp and tcp packets by port numbers - for example -p1:6,21,23 will only dump icmp packets, ftp packets (protocol 6, port 21) and telnet packets (protocol 6, port 23). 
# however, it has a big difference from -f "  ", see http://ipaudit.sourceforge.net/documentation/manpages/ipaudit.html. Thus we do not use it.

# For UDP broadcast, all packet headers have total size 42 bytes, to get real payload size, use packetsize-42 
ipaudit -p17 -E $duration -t -S -m eth0 -o traffic.log &

ipaudit -f "udp 50000" -E $duration -t -S -m eth0 -o traffic.log &

# stdbuf -oL nohup is used to enable redirect flush once per line


########### Controlnet Setup ################
# Setup host to receive and subnet to send


if [ $nodeid -eq 1 ]; then
# set up host
  echo $ServiceHOME/bcastrecv.py  >> tmp.log ## host
  stdbuf -oL nohup $ServiceHOME/bcastsend.py 192.168.0.255 >> send.log
# setup subnet to receive 
else
  echo $CoreHOME/bcastsend.py >> 192.168.0.255 tmp.log
  stdbuf -oL nohup $ServiceHOME/bcastsend.py 192.168.0.255 >> recv.log
fi



# sleep duration time  + 1 seconds until ipaudit completes
sleep $((duration+2))


#if [ ! -d $CoreHOME/trafficlog ]; then
#  mkdir $CoreHOME/trafficlog
#fi

# add nodeid in the beginning of each line
#sed "s/^/$nodeid /" traffic.log > modtraffic.log
# merge and copy log file to one permanent location
#cat modtraffic.log >> $CoreHOME/trafficlog/traffic.log

