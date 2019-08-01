"""
    Module
    using mmsim
"""
import struct
from collections import deque

import zmq


def _map_rotated_list(directions, rotation):
    q = deque(directions)
    q.rotate(rotation)
    return dict(zip(directions, q))


MAZE_SIZE = 16
GOAL_CELLS = [(7, 7), (7, 8), (8, 7), (8, 8)]
MAX_ITERATIONS = 1000

STEPS = ('front', 'left', 'right', 'back')
DIRECTIONS = ('north', 'east', 'south', 'west')

ADJACENT_POSITION_CHANGE = {
    'north': (0, 1), 'east': (1, 0), 'south': (0, -1), 'west': (-1, 0)}

DIRECTION_AFTER_STEP = dict(zip(
    ('front', 'left', 'back', 'right'),
    (_map_rotated_list(DIRECTIONS, rotation) for rotation in range(4))
))

class Mouse:
    def __init__(self, position=(0, 0), direction='north', maze=None):
        self.position = position
        self.direction = direction
        self.maze = maze

    def position_after_step(self, step):
        x, y = self.position
        direction = DIRECTION_AFTER_STEP[step][self.direction]
        xdiff, ydiff = ADJACENT_POSITION_CHANGE[direction]
        return (x + xdiff, y + ydiff)

    def weight_after_step(self, step):
        x, y = self.position_after_step(step)
        return self.maze.weights[x][y]

    def move(self):
        step = self.best_step()

        self.position = self.position_after_step(step)
        self.direction = DIRECTION_AFTER_STEP[step][self.direction]

    def is_allowed_step(self, step):
        x, y = self.position
        wall = DIRECTION_AFTER_STEP[step][self.direction]
        return not self.maze.walls[x][y][wall]


    def best_step(self):
        possible_steps = [step for step in STEPS if self.is_allowed_step(step)]
        weights = [self.weight_after_step(step) for step in possible_steps]
        best = weights.index(min(weights))
        return possible_steps[best]

    def recalculate_weights(self):
        x, y = self.position
        self.maze.weights[x][y] += 1

class Maze:
    """
        Class to represent Maze building/ updating walls and weignts based off Mouse object's position

        walls: array of bytes where each index is a cell and each byte represents a wall in a maze
        weights: number of times Mouse visits cell
    """

    def __init__(self):

        self.walls = [[{} for y in range(MAZE_SIZE)] for x in range(MAZE_SIZE)]
        self.weights = [[0 for y in range(MAZE_SIZE)]
                        for x in range(MAZE_SIZE)]

        for x in range(MAZE_SIZE):
            for y in range(MAZE_SIZE):
                self._set_walls(x, y, north=0, east=0,
                                south=0, west=0, visited=0)
        self._initialize_outter_walls()


    def _set_walls(self, x, y, **kwargs):
        for direction, wall in kwargs.items():
            self.walls[x][y][direction] = wall

    def _build_adjacent_cell_wall(self, direction, wall, mouse=None):
        x, y = mouse.position # how to get
        xdiff, ydiff = ADJACENT_POSITION_CHANGE[direction]
        x += xdiff
        y += ydiff
        direction = DIRECTION_AFTER_STEP['back'][direction] #why back??
        self.walls[x][y][direction] = wall

    def _build_walls(self, walls, mouse=None):
        x, y = mouse.position
        for direction, wall in walls.items():
            if not wall:
                continue
            if self.walls[x][y][direction] == wall:
                continue
            self.walls[x][y][direction] = wall
            self._build_adjacent_cell_wall(direction, wall, mouse=mouse)
        self.walls[x][y]['visited'] = 1

    def _initialize_outter_walls(self):
        for x in range(MAZE_SIZE):
            for y in range(MAZE_SIZE):
                if x == 0:
                    self._set_walls(x, y, west=1)
                if y == 0:
                    self._set_walls(x, y, south=1)
                if x == MAZE_SIZE - 1:
                    self._set_walls(x, y, east=1)
                if y == MAZE_SIZE - 1:
                    self._set_walls(x, y, north=1)

    def update_walls(self, mouse=None, server=None):
        left, front, right = struct.unpack('3B', server.req.recv()) 
        rotations = {'east': 0, 'south': 1, 'west': 2, 'north': 3}
        walls = deque([left, front, right, 0])
        walls.rotate(rotations[mouse.direction])
        walls = dict(zip(DIRECTIONS, walls))
        return walls


class MazeServer:
    """
        Class to handle communication with Micromouse Simulation server
    """
    def __init__(self, address='tcp://127.0.0.1:6574'):
        ctx = zmq.Context()
        self.req = ctx.socket(zmq.REQ)
        self.req.connect(address)
        self.reset()

    def reset(self):
        self.req.send(b'reset')
        return self.req.recv()

    def read_walls(self, mouse=None):
        """
            1. W: is the W byte character, idicating a request to read walls at the current position.
            2. x-position: is a byte number indicating the x-position of the mouse.
            3. y-position: is a byte number indicating the y-position of the mouse.
            4. orientation: a byte character, indicating the mouse orientation (N for North, E for East, S for South and W
                for West). Indicates where the mouse is heading to.
        """
        
        direction = mouse.direction[0].upper().encode()
        self.req.send(b'W' + struct.pack('2B', *mouse.position) + direction)
    

    def send_state(self, mouse=None, maze=None):
        direction = mouse.direction[0].upper().encode()
        state = b'S' + struct.pack('2B', *mouse.position) + direction
        state += b'F'
        for row in maze.weights:
            for weight in row:
                state += struct.pack('B', weight)
        state += b'F'
        for row in maze.walls:
            for walls in row:
                value = walls['visited']
                value += walls['east'] << 1
                value += walls['south'] << 2
                value += walls['west'] << 3
                value += walls['north'] << 4
                state += struct.pack('B', value)
        self.req.send(state)
        return self.req.recv()


def run_search():
    maze_server = MazeServer()
    maze = Maze()
    mouse = Mouse(maze=maze)

    maze_2 = Maze()
    mouse_2 = Mouse(maze=maze_2, position=(15,0))

    for _ in range(MAX_ITERATIONS):
        maze_server.read_walls(mouse=mouse)
        walls = maze.update_walls(mouse=mouse, server=maze_server)
        maze._build_walls(walls, mouse=mouse)
        mouse.recalculate_weights()
        maze_server.send_state(mouse=mouse, maze=maze)
        if mouse.position in GOAL_CELLS:
            break
        mouse.move()

        # TODO:
        # Mouse/walls do not display moves at the same time
        # maze_server.read_walls(mouse=mouse_2)
        # walls = maze.update_walls(mouse=mouse_2, server=maze_server)
        # maze_2._build_walls(walls, mouse=mouse_2)
        # mouse_2.recalculate_weights()
        # maze_server.send_state(mouse=mouse_2, maze=maze_2)
        # if mouse_2.position in GOAL_CELLS:
        #     break
        # mouse_2.move()


if __name__ == '__main__':
    run_search()
