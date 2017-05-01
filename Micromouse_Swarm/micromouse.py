#!/usr/bin/python

import sys, time
import commands

import pickle
from socket import *

import threading
from collections import deque

import numpy as np
import numpy.core.defchararray as np_f

import subprocess 



""" Wireless Micromouse Maze Solver

>Read maze from file
>Create graph
>Search maze using depth first search
>Pack visited Struct into stack
>Broadcast visited to other mice
>Send position to host (controlnet)
>Update visited with received stacks
>Avoid taking paths traveled by other mice
>Exit when all cells traveled


 """
           				
			
def find_path_dfs(maze):
	global visited
	global s
#	start, goal = (1, 1), (len(maze) - 2, len(maze[0]) - 2)
	start = {'n2':(1,1), 'n3':(len(maze) - 2, len(maze[0]) - 2), 'n4':(1,31), 'n5':(31,1) }
	start, goal = start[gethostname()], (17,17)
	#txPosition(start)
	stack = deque([("", start)])
	graph = maze2graph(maze)
	while stack:
		path, current = stack.pop()
		if current == goal:
			return path
		if current in visited:
			continue
		visited.add(current)
		txPosition(current)
		tx = threading.Thread(target=txVisited).start()
		rx = threading.Thread(target=rxVisited).start()

		
		time.sleep(3)
		print 'Searching'
		for direction, neighbour in graph[current]:
			stack.append((path + direction, neighbour))
	return "No Path Found!"
	

	
def rxVisited():
	'Update current stack with received visited '
	global visited
	global s
	global myip
	print 'RX'
	data, addr = s.recvfrom(1024)
	new_visited = pickle.loads(data)
	visited = visited | new_visited
	print(addr[0])
	print(visited)


def txVisited():
	'Broadcast visited cells'
	global visited
	global BROADCAST
	global PORT
	global s
	print'TX'
	data = pickle.dumps(visited)
	s.sendto(data, (BROADCAST, PORT))
	
	
def txPosition(cell):
	global ctrlip

	ypos, xpos = cell
	xpos = xpos/2*50
	ypos = ypos/2*50
	hostname = gethostname()
	nodenum = hostname[-1]
	
	coreString = 'coresendmsg node number=%c xpos=%d ypos=%d' % (nodenum, xpos, ypos)
	ctrl = socket(AF_INET, SOCK_STREAM)
	ctrl.connect((ctrlip, 1337))
	data = coreString.encode()
	ctrl.send(data)
	ctrl.close()



def textMaze(file):
    'Read txt maze (33x33). 1 = wall 0 = path'
    maze = np.genfromtxt(file,dtype=str,delimiter=1)
    maze = np_f.replace(maze,'.','0')
    maze = np_f.replace(maze,' ','0')
    maze = np_f.replace(maze,'|','1')
    maze = np_f.replace(maze,'-','1')
    maze = np_f.replace(maze,'+','1')
    return maze.astype(np.int)
    
def maze2graph(maze):
    'Create graph for each cell including all neighbors (text maze)'
    height = len(maze)
    width = len(maze[0]) if height else 0
    graph = {(i,j): [] for j in range(width) for i in range(height) if not maze[i][j]}
    for row, col in graph.keys():
        if row < height-1 and not maze[row+1][col]: # check N S neighbors
            graph[(row, col)].append(('S',(row+1, col)))
            graph[(row+1, col)].append(('N', (row, col)))
        if col < width -1 and not maze[row][col+1]: #check E W neighbors
            graph[row, col].append(('E', (row,col+1)))
            graph[row, col+1].append(('W', (row, col)))
    return graph    


PORT = 5000
BROADCAST = '192.168.0.255'

myip = commands.getoutput("hostname -I")

ctrlip = '172.168.0.254'

s = socket(AF_INET, SOCK_DGRAM)
s.bind(('', PORT))
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)



visited = set()

def main():
	print(myip)

	maze = '2016apec.maze'
	maze = textMaze(maze)
	find_path_dfs(maze)
	
if __name__ == "__main__" : main()







