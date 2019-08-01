"""
    Unit tests for Micromouse Wireless Micromouse Maze Solver

 """


import unittest
from mock import Mock

from micro_mouse import Mouse, ActionThread


class MazeTestCase(unittest.TestCase):
	


class MouseTestCase(unittest.TestCase):
	def setUp(self):
		self.m = Mouse()
		self.m.name = 'n1'

#		self.m.visited = [] how to test visited paths
		self.m.x, self.y = self.m.pos
# DFS tests

	def test_maze_mapped(self):
    	self.m.depthFirstSearch()
    	self.assertLess(len(m.visited), len(m.maze))

	def test_valid_start(self):
		self.m.findStart()
		self.assertEqual(bin(m.maze[self.x][self.y]).count('1'), 4)

	def test_in_bounds(self):
    	self.assertTrue((0 < self.x < 15) and (0 < self.y < 15))

    def test_maze_solved(self):
    	self.assertIn(m.pos in waypoint['goal'])
    	
    def test_peekNeighbors(self): ## isolated tests
#    	assertTrue(self.m.peek_neighbors, self.m.inBounds)
    	
    def test_all_neighbors_visited(self):
    	self.m.findNeighbors()
    	self.assert
    	
    def test_newNeighbors(self):
    	self.m.findNeighbors()
    	self.assertTrue(len(n) > 0)
    

	
# Read byte maze

# Read txt maze

# Queue index

# Visited updated

# Check threads

# Visted updtaes before Maze mapped

# Network 

class ManetTesCase(unittest.TestCase):
'Mouse to Mouse'
	def setUp(self):
		
# Send visited

# Receive visited

# class Controlnet_test(unittest.TestCase):
# 'Mouse to Mouse'






