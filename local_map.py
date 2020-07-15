# LOCAL MAP

"""Finding shortest distance between different points from a given map"""


def optimized_state(states):
    distances = []
    x, y = mapp.goal
    for state in states:
        i, j = state
        distance = abs(j - y) + abs(i - x)
        distances.append((distance, state))
    distances.sort()
    return distances[0][1]


def filter_path(duplicate_path):
    for num, coordinate in enumerate(duplicate_path):
        if num == len(duplicate_path) - 1:
            return duplicate_path
        try:
            x1 = duplicate_path[num][0]
            x2 = duplicate_path[num + 1][0]
            y1 = duplicate_path[num][1]
            y2 = duplicate_path[num + 1][1]
            if ((x1 == x2) and (abs(y2 - y1) == 1)) or ((y1 == y2) and (abs(x2
                                                                            - x1)
                                                                        == 1)):
                pass
            else:
                # duplicate_path.remove(duplicate_path[num + 1])
                del duplicate_path[num + 1]
                filter_path(duplicate_path)
        except IndexError:
            pass


def actions(state):
    row, column = state
    movements = [(row + 1, column), (row - 1, column), (row, column + 1),
                 (row, column - 1)]
    moves = [move for move in movements if move not in Node.explored_state
             and move not in mapp.wall and move[0] in range(mapp.height) and
             move[1] in range(mapp.width)]
    return moves


class Node:
    explored_state = []
    frontier = []
    path = []
    shortest_path = []

    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action
        self.frontier.append(self.state)

        while True:
            if not self.frontier:
                print("There is not solution")
                break
            elif self.state == mapp.goal:
                self.path.append(self.state)
                break

            self.action = actions(optimized_state(self.frontier))
            self.explored_state.append(self.state)

            if not self.action:
                self.frontier.remove(self.state)
            else:
                for i in self.action:
                    self.frontier.append(i)
                self.parent = self.state
                self.path.append(self.state)
                self.frontier.remove(self.state)

            self.state = optimized_state(self.frontier)
        self.path.reverse()
        path_1 = []
        for i in self.path:
            path_1.append(i)

        for i in filter_path(path_1):
            self.shortest_path.append(i)
        self.shortest_path.reverse()
        self.path.reverse()


class Map:

    def __init__(self, file):
        self.file = file
        self.start = None
        self.goal = None
        self.wall = []

        with open(self.file) as file:
            self.contents = file.read()

        self.contents = self.contents.splitlines()
        self.height = len(self.contents)
        self.width = max(len(content) for content in self.contents)

    def draw_walls(self):
        for i, row in enumerate(self.contents):
            for j, column in enumerate(row):
                if column == ' ':
                    if (i, j) in Node.shortest_path:
                        print('*', end='')
                    else:
                        print(' ', end='')
                elif column in locations:
                    print(column, end='')
                    if column == start:
                        self.start = (i, j)
                    elif column == goal:
                        self.goal = (i, j)
                else:
                    print('█', end='')
                    self.wall.append((i, j))
            print()


if __name__ == '__main__':
    locations = ['H', 'I', 'K', 'E', 'S', 'T']
    start = input('Please enter the start point\n')
    goal = input('Please enter the end point\n')
    mapp = Map('local_map.txt')
    mapp.draw_walls()
    print()
    node = Node(state=mapp.start, parent=None, action=None)
    mapp.draw_walls()
