#!/usr/bin/python

import sys, time
from socket import *

import commands
import threading
import Queue

from collections import NamedTuple

import pdb
import numpy
import commands

""" Wireless Micromouse Maze Solver

>Read maze from file
>Create graph
>Search maze using depth first search 
>Broadcast visited to other mice
>Send position to host (controlnet)
>Update visited with received stacks
>Avoid taking paths traveled by other mice
>Exit when all cells traveled

> 3 threads = TX, RX, Search


GUI

CORE - 'coresendmesg'
>send pos to host (controlnet)
>send shutdown message when mazecomplete

Pygame
>Receive mouse position on port/socket
>Controlnet/ssh 

 """
 
exitFlag = 0

class Mouse:
    'Search and store all available paths in maze'
    
    compass = {"W":8,"S":4,"E":2,"N":1}
    waypoints = {'start':[(0,0),(0,14),(15,0),(0,15)], 'goal':[(8,8)]} ## Need to figure out how to start each mouse in different locations within each script
    nodes = ['n1','n4','n3','n4']
    ready_pos = dict(zip(nodes,waypoints['start']))

     
    def __init__(self, maze, name = 'n1'):
        self.maze = maze
        self.name = name
        self.visited = []
        self.pos = Mouse.read_pos[name]
        self.findStart()
  
    def findStart(self):
        'Find valid start postion (less than 4 walls) '
        x, y = self.pos
        if bin(self.maze[x][y]).count('1') == 4: pass
        	# move to neighbor position and check again.
        	
    def findNeighbor(self):
        'Returns position of neighbor cell.'
        x,y = self.pos
        if self.way == "N": y += 1
        elif self.way == "S": y -= 1
        elif self.way == "E": x += 1
        elif self.way == "W": x -= 1
        return x,y
    
    def inBounds(self):
    	return (0< self.x <len(maze)-1) and (0 < self.y < len(maze)-1)
    
    def peekNeighbors(self):
    	'return list of all neighbor cells'	
    		return [for self.way in nesw.keys() findNeighbors() if inBounds()]

    def pathFree(self, pos, way):
        ' Check path open'
        x, y = self.pos
        return (nesw[way] & (maze[x][y]&0xF)) == 0
        
    def findPaths(self):
        'Return list of accessible paths.' 
        return [findNeighbor() for self.way in nesw.keys() if self.pathFree()]

    def depthSearch(self):
        'Find all paths throughout the maze (does not solve)'
        self.visited.append(self.pos)
        time.sleep(500) # give time to update stack from other mice
        neighbors = self.findNeighbors()
        for self.pos in neighbors:
            if self.pos not in self.visited:
                self.depthSearch()
            elif len(self.visited) < len(maze): ## all paths visited
            	break 

class ActionThread(threading.Thread):
    'Threads send, receive, or searching'

    PORT = 5000
    comm = socket(AF_INET, SOCK_DGRAM)
    comm.bind(('', PORT))
    comm.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

    def __init__(self, threadID, name, q, Mouse):
        self.ip = commands.getoutput('hostname -I')
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
        
    def run(self):
        if self.name == 'Search': depthSearch()
        if self.name == 'TX': txVisited()
	 	if self.name == 'RX': rxVisited(mouse)
             
def rxVisited(Mouse):
    'Update current stack with received visited '
    data, addr = s.recvfrom(1024)
    mouse.visited.append(int(data)) 


def txVisited(self, visited):
    'Broadcast visited cells'
    data = repr(visited)
    s.sendto(data, ('<broadcast>', PORT))


def byteMaze(file):
    'Read binary Maze files into 16x16 maze'
    hexformat = lambda hexstr: int(hexstr,16)
    with open(file, "rb") as f:
        maze = ["{:02x}".format(ord(c)) for c in f.read()]
        maze = map(hexformat,maze)
        maze = zip(*[iter(maze)]*16)
        maze = map(list,maze)  
    return maze

def textMaze(file):
	'Read txt maze 1 = wall 0 = path'
	with open(file, 'r') as f:
		


def maze2graph(maze):
	'Create graph for each cell including all neighbors'
	height = len(maze)
	width = len(maze[0]) if height else 0
	graph = {(i,j): [] for j in range(width) for i in range(height) if not maze[i][j]}
	for row, col in graph.keys():
		if row < height-1 and not maze[row+1][col]: # check N S neighbors
			graph[(row, col)].append('S',(row+1, col))
			graph[(row+1, col)].append('N', (row, col))
		if col < width -1 and not maze[row][col+1]: #check E W neighbors
			graph[row, col].append('E', (row,col+1))
			graph[row, col+1].append('W', (row, col))
	return graph 	
	

def main():

    maze = 'allamerica2013.maz'
    maze = byteMaze(maze)
    mouse = Mouse(maze, name)

    while 1:
        if mouse.pos != waypoints['goal']: 
        
### Action threads
			tx = ActionThread(1, 'TX')
			rx = ActionThread(2, 'RX')  
			search = ActionThread(3, 'Search')

			tx.start()
			rx.start()
			search.start()    
			
		else: 
		    print 'Maze mapped Successfully' ## Trigger core shutdown
		    tx.join()
			rx.join()
			search.join()   


if __name__ == "__main__" : main()

  
  

#    threadList = ['Search','TX','RX']   
#    queueLock = threading.Lock()
#    workQueue = Queue.Queue(6)
#    threads = []
#    threadID = 1    

#Priority Threads

#        for tName in threadList:
#	    thread = Messenger(threadID, tName, workQueue, mouse)
#	    thread.start()
#      	    threads.append(thread)
#            threadID += 1
#	   
#	queueLock.acquire() 
#	for tname in threadList: 
#	    workQueue.put(mouse.visited) 
#        queueLock.release()
#        
#        exitflag = 1
#        for t in threads:
#            t.join()
#            	
#	while not workQueue.empty():
#	    pass
#   exitflag = 1
#   for t in threads:
#       t.join()






