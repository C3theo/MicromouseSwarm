from collections import deque
import struct

import zmq


def _map_rotated_list(lst, rotation):
    import pdb; pdb.set_trace()
    que = deque(lst)
    que.rotate(rotation)
    return dict(zip(lst, que))


MAZE_SIZE = 16
GOAL_CELLS = [(7, 7), (7, 8), (8, 7), (8, 8)]
MAX_ITERATIONS = 1000

STEPS = ('front', 'left', 'right', 'back')
DIRECTIONS = ('north', 'east', 'south', 'west')
DIRECTION_AFTER_STEP = dict(zip(
    ('front', 'left', 'back', 'right'),
    (_map_rotated_list(DIRECTIONS, rotation) for rotation in range(4))
))
ADJACENT_POSITION_CHANGE = {
    'north': (0, 1), 'east': (1, 0), 'south': (0, -1), 'west': (-1, 0)}

maze_walls = [[{} for y in range(MAZE_SIZE)] for x in range(MAZE_SIZE)]
maze_weights = [[0 for y in range(MAZE_SIZE)] for x in range(MAZE_SIZE)]
mouse_position = (0, 0)
mouse_direction = 'north'

ctx = zmq.Context()
req = ctx.socket(zmq.REQ)
req.connect('tcp://127.0.0.1:6574')


def server_reset():
    req.send(b'reset')
    return req.recv()


def server_read_walls():
    direction = mouse_direction[0].upper().encode()
    req.send(b'W' + struct.pack('2B', *mouse_position) + direction)
    return struct.unpack('3B', req.recv())


def server_send_state():
    direction = mouse_direction[0].upper().encode()
    state = b'S' + struct.pack('2B', *mouse_position) + direction
    state += b'F'
    for row in maze_weights:
        for weight in row:
            state += struct.pack('B', weight)
    state += b'F'
    for row in maze_walls:
        for walls in row:
            value = walls['visited']
            value += walls['east'] << 1
            value += walls['south'] << 2
            value += walls['west'] << 3
            value += walls['north'] << 4
            state += struct.pack('B', value)
    req.send(state)
    return req.recv()


def _set_walls(x, y, **kwargs):
    for direction, wall in kwargs.items():
        maze_walls[x][y][direction] = wall


def _build_adjacent_cell_wall(direction, wall):
    x, y = mouse_position
    xdiff, ydiff = ADJACENT_POSITION_CHANGE[direction]
    x += xdiff
    y += ydiff
    direction = DIRECTION_AFTER_STEP['back'][direction]
    maze_walls[x][y][direction] = wall


def _build_walls(walls):
    x, y = mouse_position
    for direction, wall in walls.items():
        if not wall:
            continue
        if maze_walls[x][y][direction] == wall:
            continue
        maze_walls[x][y][direction] = wall
        _build_adjacent_cell_wall(direction, wall)
    maze_walls[x][y]['visited'] = 1


def _initialize_outter_walls():
    for x in range(MAZE_SIZE):
        for y in range(MAZE_SIZE):
            if x == 0:
                _set_walls(x, y, west=1)
            if y == 0:
                _set_walls(x, y, south=1)
            if x == MAZE_SIZE - 1:
                _set_walls(x, y, east=1)
            if y == MAZE_SIZE - 1:
                _set_walls(x, y, north=1)


def initialize_maze():
    for x in range(MAZE_SIZE):
        for y in range(MAZE_SIZE):
            _set_walls(x, y, north=0, east=0, south=0, west=0, visited=0)
    _initialize_outter_walls()


def update_walls(left, front, right):
    rotations = {'east': 0, 'south': 1, 'west': 2, 'north': 3}
    walls = deque([left, front, right, 0])
    walls.rotate(rotations[mouse_direction])
    walls = dict(zip(DIRECTIONS, walls))
    _build_walls(walls)


def position_after_step(step):
    x, y = mouse_position
    direction = DIRECTION_AFTER_STEP[step][mouse_direction]
    xdiff, ydiff = ADJACENT_POSITION_CHANGE[direction]
    return (x + xdiff, y + ydiff)


def weight_after_step(step): ## access weights in Maze class
    x, y = position_after_step(step)
    return maze_weights[x][y]


def move(step):
    global mouse_direction
    global mouse_position
    mouse_position = position_after_step(step)
    mouse_direction = DIRECTION_AFTER_STEP[step][mouse_direction] # change direction


def is_allowed_step(step):
    x, y = mouse_position
    wall = DIRECTION_AFTER_STEP[step][mouse_direction]
    return not maze_walls[x][y][wall]


def recalculate_weights():
    x, y = mouse_position
    maze_weights[x][y] += 1


def best_step():
    possible_steps = [step for step in STEPS if is_allowed_step(step)]
    weights = [weight_after_step(step) for step in possible_steps]
    best = weights.index(min(weights))
    return possible_steps[best]


def run_search():
    server_reset()
    initialize_maze()
    # import pdb; pdb.set_trace()
    for _ in range(MAX_ITERATIONS):
        # import pdb; pdb.set_trace()
        update_walls(*server_read_walls())
        recalculate_weights()
        server_send_state()
        if mouse_position in GOAL_CELLS:
            break
        move(best_step())


if __name__ == '__main__':
    run_search()