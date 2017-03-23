import pygame
from pygame.locals import *
from collections import namedTuple

import pdb


class Maze():
    
    def __init__(self, mazeLayer, mazeArray):
        self.state = 'create'
        self.mazeArray = mazeArray
        self.mLayer = mazeLayer
        self.mLayer.fill((0,0,0,0))

        #Draw Grid
        for y in xrange(16):
            pygame.draw.line(self.mLayer,(0,0,0,255),(0,y*20),(320,y*20),3) # horizontal
            for x in xrange(16):
                    pygame.draw.line(self.mLayer,(0,0,0,255),(x*20,0),(x*20, 320),3) #vertical

        self.totalCells = 256
        self.pos = (0,0)
        self.visited = []
        self.compass = {"W":8,"S":4,"E":2,"N":1}

    def move(self):
        x,y =self.pos
        if self.way == "N":
            y += 1
        elif self.way == "S":
            y -= 1
        elif self.way == "E":
            x += 1
        elif self.way == "W":
            x -= 1
        neighbor_pos = x,y
            
        return neighbor_pos

    def depthSearch(self):
        """ """
        
        self.visited.append(self.pos)
        neighbors = self.findNeighbors()
        self.clearWall()

        for self.pos in neighbors:
            if self.pos not in self.visited:
                self.depthSearch()
     

    def update(self):       
        if self.state == 'create': self.depthSearch()
                    
    def clearWall(self):
        
        x, y = self.pos
        y = 15 - y

        dx, dy =  x*20, y*20

        for self.way in self.compass.keys():
            if self.pathFree():
                if self.way == 'W':
                    pygame.draw.line(self.mLayer,(0,0,0,0),(dx, dy+2),(dx, dy+18), 3)#knock down East
                elif self.way == 'S': 
                    pygame.draw.line(self.mLayer, (0,0,0,0), (dx+2, dy+20), (dx+18, dy+20), 3)#knock down North
                elif self.way == 'E': 
                    pygame.draw.line(self.mLayer, (0,0,0,0), (dx+20, dy+2), (dx+20, dy+18), 3)#knock down West
                elif self.way == 'N': 
                    pygame.draw.line(self.mLayer, (0,0,0,0), (dx+2, dy), (dx+18, dy), 3)#knock down South
            
    def draw(self, screen):
        
        screen.blit(self.mLayer, (0,0))

    def pathFree(self):
        
        x,y = self.pos
        return (self.compass[self.way] & (self.mazeArray[x][y]&0xF)) == 0

    def findNeighbors(self):
        """Returns position of all accessible neighbors."""
        
        neighbors = []
        for self.way in self.compass.keys():
            if self.pathFree():
                adj = self.move()
                neighbors.append((adj))
      
        return neighbors


def to_hex(hexstr):
    """  """
    return int(hexstr,16)

def readMaze(file):
    """ Read binary Maze files into 16x16 maze"""
    
    with open(file, "rb") as f:
        maze = ["{:02x}".format(ord(c)) for c in f.read()]
        maze = map(to_hex,maze)
        maze = zip(*[iter(maze)]*16)
        maze = map(list,maze)
        
    return maze


def main():
    pygame.init()

    screen = pygame.display.set_mode((320,320))
    pygame.display.set_caption('Micromouse Maze')
    pygame.mouse.set_visible(0)

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((255,255,255))

    mazeLayer = pygame.Surface(screen.get_size())
    mazeLayer = mazeLayer.convert_alpha()
    mazeLayer.fill((0,0,0,0))

    mazeFile = 'allamerica2013.maz'
    mazeArray = readMaze(mazeFile)
    
    newMaze = Maze(mazeLayer, mazeArray)

    screen.blit(background,(0,0))
    pygame.display.flip()
    clock = pygame.time.Clock()



    while 1:
        clock.tick(60)
        for event in pygame.event.get(): # grab each event from the pygame event list
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
#        pygame.time.delay(1000)
        newMaze.update()
        
        screen.blit(background,(0,0))
        newMaze.draw(screen)
        pygame.display.flip()

        

if __name__ == '__main__': main()
