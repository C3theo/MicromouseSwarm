#!/usr/bin/env python2.7

import sys, time
from socket import *

import thread
from queue import Queue

import pdb


'Defines how mouse traverses maze. '

class Mouse(object):
    'Searches and stores all available paths in mazes '
    count = 0
    start = [(0,0),(0,14),(15,0),(0,15)]
    compass = {"W":8,"S":4,"E":2,"N":1}
     

    def __init__(self, maze):
        self.maze = maze
        self.visited = []
        self.pos = Mouse.start[count]
        self.isStart()

        txthread = thread.start_new_thread(mouse.txData , ())
        
        
    def isStart(self):
        'Checks valid start postion (less than 4 walls) '
        n = self.findNeigbors()
        x,y = self.pos
        if bin(self.maze[x][y]).count('1') == 4:
            pos = n.pop()
            self.isStart()
            
    
    def getWay(turn):
        'Returns cardinal direction given binary word(WSEN).'
        return nesw.keys()[nesw.values().index(turn)]
    
    def move(self):
        'Returns position of neighbor.'
        x,y = self.pos
        if self.way == "N":
            y += 1
        elif self.way == "S":
            y -= 1
        elif self.way == "E":
            x += 1
        elif self.way == "W":
            x -= 1
        pos = (x,y)
        return pos

    
    def pathFree(self, pos, way):
        'Returns open paths '
        x,y = pos
        return (nesw[way] & (m[x][y]&0xF)) == 0


    def findNeighbors(self):
        'Returns position of all accessible neighboring cells.'
        neighbors = [move(pos,way) for way in nesw.keys() if self.pathFree()]
##        for way in nesw.keys():
##            if self.pathFree():
##                adj = move(pos,way)
##                neighbors.append((adj))

        return neighbors

    def depthSearch(self):
        'Depth First Search used to search all paths within maze'
        self.visited.append(self.pos)
        time.sleep(1000)
        neighbors = self.findNeighbors()
        for self.pos in neighbors:
            if self.pos not in self.visited:
                self.depthSearch()

        

class Messenger:
    """  """
    PORT = 5000
    
    def __init__(self):
        
        self.ip = commands.getoutput('hostname -I')
        self.comm = socket(AF_INET, SOCK_DGRAM)
        self.comm.bind(('', PORT))
        self.comm.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        
    def rxVisited(self, mouse):
        """ Update visited stack from those received from other nodes """
        data, addr = s.recvfrom(1024)
        data.decode()
        mouse.visited.append(data)

    def txVisited(self, visited):
        """Broadcast vsited stack to to other nodes """
        data = repr(visited)
        s.sendto(data, ('<broadcast>', PORT))

def readMaze(file):
    """ Read binary Maze files into 16x16 maze"""
    hexformat = lambda hexstr: int(hexstr,16)
    with open(file, "rb") as f:
        maze = ["{:02x}".format(ord(c)) for c in f.read()]
        maze = map(hexformat,maze)
        maze = zip(*[iter(maze)]*16)
        maze = map(list,maze)
        
    return maze


def main():

    maze = 'allamerica2013.maz'
    
    maze = readMaze(maze)
    mouse = Mouse(maze)
    
    
    thread.start_new_thread(mouse.rxData, mouse)
    thread.start_new_thread(mouse.txData, mouse.visited)
   

if __name__ == "__main__" : main()

  
    





