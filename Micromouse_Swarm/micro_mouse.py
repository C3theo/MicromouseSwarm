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

> 3 threads = TX, RX, Search

>Multicast send/recv
>One node as sender and then others receive
>Reuse Socket address

GUI

CORE API- 'coresendmesg'
>send pos to host (controlnet)
>send shutdown message when mazecomplete

Pygame
>Receive mouse position on port/socket
>Controlnet/ssh 

 """

import commands
import Queue
import struct
import sys
import threading
import time
from collections import deque
from socket import *

import numpy as np
import numpy.core.defchararray as np_f


class Mouse:
    """
        Class that represents one of many robot mice traversing a maze
    """
    
    compass = {"W":8,"S":4,"E":2,"N":1}
    waypoints = {'start':[(0,0),(0,14),(15,0),(0,15)], 'goal':[(8,8)]} 
    nodes = ['n1','n4','n3','n4']
    ready_pos = dict(zip(nodes, waypoints['start']))

    def __init__(self, maze=, name = 'n1'):
        self.maze = maze
        self.name = name
        self.visited = []
        self.pos = Mouse.read_pos[name]
        self.find_start()
  
    def find_start(self):
        'Find valid start postion (less than 4 walls) '
        x, y = self.pos
        if bin(self.maze[x][y]).count('1') == 4: pass
           
            
    def find_neighbor(self):
        'Returns position of neighbor cell.'
        x,y = self.pos
        if self.way == "N": y += 1
        elif self.way == "S": y -= 1
        elif self.way == "E": x += 1
        elif self.way == "W": x -= 1
        return x,y
    
    def in_bounds(self):
        return (0< self.x <len(maze)-1) and (0 < self.y < len(maze)-1)
    
    def peek_neighbors(self):
        'return list of all neighbor cells' 
        return [findNeighbors() for self.way in nesw.keys() if inBounds()]

    def is_free(self, pos, way):
        ' Check path open'
        x, y = self.pos
        return (nesw[way] & (maze[x][y]&0xF)) == 0
        
    def find_paths(self):
        'Return list of accessible paths.' 
        return [findNeighbor() for self.way in nesw.keys() if self.pathFree()]

    def depth_first_search(self):

        self.visited.append(self.pos)
        
        # send
        txVisited(self.visited)
        
        # recv
        newpaths = rxVisited(swarm_update)
        
        # update with other stacks
        updateVisited(newpaths)
        
        time.sleep(500) # give time to update stack from other mice
        neighbors = self.findNeighbors()
        
        for self.pos in neighbors:
            if self.pos not in self.visited:
                self.depthSearch()
            elif len(self.visited) < len(maze): ## all paths visited
                break
           		
    def updateVisited(self, swarm_update):
        'Updates visited stack with those received from other nodes' 
        new_visited = set(swarm_update)
        self.visited = self.visited.union(new_visited)




def breadth_first_search():
    """
    """


def depth_first_search(graph), Event):
    """
    """

	start, goal = (1, 1), (len(maze) - 2, len(maze[0]) - 2)
	stack = deque([("", start)])
	visited = set() 
	while stack:
		path, current = stack.pop()
		if current == goal:
			return path
		if current in visited:
			continue

		if not Event.is_set():
			visited.add(current)
			Event.set()
		
		for direction, neighbour in graph[current]:
			stack.append((path + direction, neighbour))
	return "No Path Found!"
	
def rx_visited_cells(Event):
    """
        Update current stack with received visited
    """

    data, addr = s.recvfrom(1024)
	Event.clear()


def tx_visited_cells():
    """
        Broadcast visited cells
    """
    data = struct.pack(str, visited) 
    s.sendto(data, ('<broadcast>', PORT))
	# Event.()

class ActionThread(threading.Thread):
    """
        Thread for receiving and transmitting visited paths
    """


    def __init__(self, threadID, name ):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
		self.maze = maze
        
    def run(self):
		threadLock.acquire()
        if self.name == 'Search': 
			find_path_dfs(maze)
			threadLock.release()
        if self.name == 'TX': 
			txVisited()
			threadLock.release()
		if self.name == 'RX': 
			rxVisited()
			threadLock.release()


def main():
	Event = threading.Event
	
    maze = 'allamerica2013.maz'
    maze = txtMaze(maze)
	
	multicast_group = '224.0.0.0'
	server_address = ('', 10000)
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	ttl = struct.pack('b', 1)
	sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
	
    while True:
		search = ActionThread(1, 'Search')
		tx = ActionThread(2, 'TX')
		rx = ActionThread(3, 'RX')  

		tx.start()
		rx.start()
		search.start()  
		
		threads = []
		threads.append(tx)
		threads.append(rx)
		threads.append(search)
		
		for t in threads:
			t.join()
	
if __name__ == "__main__" :
    main()
