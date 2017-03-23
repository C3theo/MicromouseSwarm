#!usr/bin/python

from core import pycore
import core_320

""" """
session = pycore.Session(persistent=True)

node1 = session.addobj(cls=pycore.nodes.CoreNode, name="n1")
node2 = session.addobj(cls=pycore.nodes.CoreNode, name="n2")
node3 = session.addobj(cls=pycore.nodes.CoreNode, name="n3")
node4 = session.addobj(cls=pycore.nodes.CoreNode, name="n4")

hub1 = session.addobj(cls=pycore.nodes.HubNode, name="hub1")
node1.newnetif(hub1, ["10.0.0.1/24"])
node2.newnetif(hub1, ["10.0.0.2/24"])
node3.newnetif(hub1, ["10.0.0.3/24"])
node4.newnetif(hub1, ["10.0.0.4/24"])


### Get (x,y) from each node








