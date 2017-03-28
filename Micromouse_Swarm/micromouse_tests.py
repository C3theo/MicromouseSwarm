import unittest
from mock import Mock

from micrmouse import Mouse
from micromouse import ActionThread

"""
    Unit tests for Micromouse Wireless Micromouse Maze Solver

 """

#### Mouse 
#class MouseTestCase(unittest.TestCase):
#	"""Base class for all Mouse tests. """
#	def assertPosEqual(self, m, pos )
#		self.assertEqual()


# dunder main == dunder main test main -  sys.exitof(main.sys.argv)
# double under

class MouseSearchTest(unittest.TestCase):
	def setUp(self):
		self.m = Mouse()
		self.m.name = 'n1'
	
#		self.m.visited = [] how to test visited paths
		self.m.x, self.y = self.m.pos
### DFS tests
	def test_mazeMapped(self):
    	self.m.depthFirstSearch()
    	self.assertLess(len(m.visited), len(m.maze))
    			  
	def test_validstart(self):
		self.m.findStart()
		self.assertEqual(bin(m.maze[self.x][self.y]).count('1'), 4)
		
	def test_inBounds(self):
    	self.assertTrue((0< self.x <15) and (0 < self.y < 15))
    
    def test_mazeSolved(self):
    	self.assertIn(m.pos in waypoint['goal'])
    	
    def test_peekNeighbors(self): ## isolated tests
#    	assertTrue(self.m.peek_neighbors, self.m.inBounds)
    	
    def test_all_neighbors_visited(self):
    	self.m.findNeighbors()
    	self.assert
    	
    def test_newNeighbors(self):
    	self.m.findNeighbors()
    	self.assertTrue(len(n) > 0)
    
class MouseUpdateTest(unittest.TestCase):
	def fake_visited_stack(self):
		return
    
    def setUp(self):
    
    
    def test_:
    def test_:
    def test_:
    def test_:
    def test_:
    def test_:
    
#with self.assertRaises(TypeError)
	
# Read byte maze

# Read txt maze

# Queue index

# Visited updated

# Check threads

# Visted updtaes before Maze mapped


### Network 

class Manet_test(unittest.TestCase):
'Mouse to Mouse'
	def setUp(self):
		
# Send visited

# Receive visited

#class Controlnet_test(unittest.TestCase):
#'Mouse to Mouse'






