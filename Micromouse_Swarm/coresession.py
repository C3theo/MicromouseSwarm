#!usr/bin/python

from core import pycore


""" MANET Coordinated Maze Discovery

IMPORTANT: script needs to be run with ROOT privileges

This is to be run with Pygame GUI


>Setup core session with wlan and nodes.
>Each node runs micromouse.py which sends and receives visited stack between nodes
>Nodes update position in memory and sends back to host
>Shutdown session when maze fully mapped

node machine type: netns
"""

## Setup Core session
session = pycore.Session(persistent=True)

wlan_node1 = session.addobj(cls=pycore.nodes.HubNode, name="wlan1") ## wlan same as node in Core API
node1 = session.addobj(cls=pycore.nodes.CoreNode, name="n1")
node2= session.addobj(cls=pycore.nodes.CoreNode, name="n2")
node3 = session.addobj(cls=pycore.nodes.CoreNode, name="n3")
node4= session.addobj(cls=pycore.nodes.CoreNode, name="n4")


node1.newnetif(wlan_node1, ["10.0.0.1/24"])
node2.newnetif(wlan_node1, ["10.0.0.2/24"])
node3.newnetif(wlan_node1, ["10.0.0.3/24"])
node4.newnetif(wlan_node1, ["10.0.0.4/24"])


### Get (x,y) from each node
# node sends coresendmesg which updates within GUI
For Pygae


switch.setposition(x,y)


### Controlnet
# setup here or within service startup ???

## when Maze fully mapped
session.shutdown()






