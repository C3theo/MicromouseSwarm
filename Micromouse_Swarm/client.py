#!usr/bin/python

from socket import *
import commands

s = socket()
host = commands.getoutput('hostname -I')
port = 12345
s.connect((host, port))
print s.recv(1024)
