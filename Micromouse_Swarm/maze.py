from pathlib import Path

maze_folder = Path('maze_files')
maze_file = maze_folder / 'allamerica2013.maz'

def byte_maze(file):
    """
        Return array from binary .maze files

    """
    # 'received {!r}'.format(binascii.hexlify(data)) better way
    def hexformat(hexstr): return int(hexstr, 16)
    with open(file, "rb") as f:
        maze = ["{:02x}".format(ord(c)) for c in f.read()]
        maze = map(hexformat, maze)
        maze = zip(*[iter(maze)]*16)
        maze = map(list, maze)
    return maze


def text_maze(file):
    """
        Return integer numpy array from .txt file

        size: (33x33)
        wall: 1
        path:0
    """

    maze = np.genfromtxt(file, dtype=str, delimiter=1)
    maze = np_f.replace(maze, '.', '0')
    maze = np_f.replace(maze, ' ', '0')
    maze = np_f.replace(maze, '|', '1')
    maze = np_f.replace(maze, '-', '1')
    maze = np_f.replace(maze, '+', '1')

    return maze.astype(np.int)


def maze_to_graph(maze):
    """
        Return graph from maze text file.
    """

    height = len(maze)
    width = len(maze[0]) if height else 0
    graph = {(i, j): [] for j in range(width)
             for i in range(height) if not maze[i][j]}

    for row, col in graph.keys():
        if row < height - 1 and not maze[row + 1][col]:  # check N S neighbors
            graph[(row, col)].append('S', (row + 1, col))
            graph[(row + 1, col)].append('N', (row, col))
        if col < width - 1 and not maze[row][col + 1]:  # check E W neighbors
            graph[row, col].append('E', (row, col + 1))
            graph[row, col + 1].append('W', (row, col))
            d
    return graph
