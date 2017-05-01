import subprocess

import threading

from socket import *

import Queue

"""
MOUSE GUI

> execute scripts using coresendmsg
> Receive cell posiion and convert to CORE coordinates system
> move nodes using coresendmsg

"""
	

def moveNode(coremsg):
	""" Update CORE-GUI """
	print coremsg
	subprocess.call(coremsg, shell=True)


def rxPosition():
	cell, addr = ctrlsock.recv(1024)
	ctrlsock.close()
	
	return cell
	
		
def worker():
	while True:
		item = q.get()
		moveNode(item)
		q.task_done()
		 

CTRLPORT = 1337
hostip = '172.168.0.254' 



ctrlsock = socket(AF_INET, SOCK_STREAM)
ctrlsock.bind(("0.0.0.0", CTRLPORT))

		
q = Queue.Queue()

def main():
	ctrlsock.listen(4)
	while True:
		c, addr = ctrlsock.accept()

		nodenum = addr[0][-1]
		print 'Connected to node'+nodenum
		data = c.recv(1024).decode()
		q.put(data)
		#print data
		for x in range(5):
			#print 'thread'+str(x)
			t = threading.Thread(target=worker)
			#t.daemon = True
			t.start()
#		moveNode(data)
		#q.join()
		c.close()


if __name__ == "__main__" : main()		


