from collections import deque
from _lib import getListOfNumbersForDay, IntCodeProgram, manhattanDistance

memory = getListOfNumbersForDay(15)

computer = IntCodeProgram(memory)

[NORTH, SOUTH, EAST, WEST] = range(1, 5)
[WALL, EMPTY, GOAL] = range(3)

class Cell(object):
    def __init__(self, x, y, cellType):
        self.x = x
        self.y = y
        self.cellType = cellType

    def __repr__(self):
        return "CELL(" + str(self.x) + "," + str(self.y) + ")"

    def neigh(self, direction):
        if direction == NORTH:
            loc = (self.x, self.y - 1)
        if direction == SOUTH:
            loc = (self.x, self.y + 1)
        if direction == WEST:
            loc = (self.x - 1, self.y)
        if direction == EAST:
            loc = (self.x + 1, self.y)
        if loc in grid:
            return grid[loc]
        return None

    def getNeighPosition(self):
        neighs = []
        neighs.append((self.x, self.y - 1))
        neighs.append((self.x, self.y + 1))
        neighs.append((self.x + 1, self.y))
        neighs.append((self.x - 1, self.y))
        return neighs

    def getUnknownNeighPosition(self):
        unknownNeigh = []
        if self.neigh(NORTH) is None:
            unknownNeigh.append((self.x, self.y - 1))
        if self.neigh(SOUTH) is None:
            unknownNeigh.append((self.x, self.y + 1))
        if self.neigh(EAST) is None:
            unknownNeigh.append((self.x + 1, self.y))
        if self.neigh(WEST) is None:
            unknownNeigh.append((self.x - 1, self.y))
        return unknownNeigh

    def getEmptyNeighPosition(self):
        emptyNeigh = []
        if self.neigh(NORTH) is not None and self.neigh(NORTH).cellType == EMPTY:
            emptyNeigh.append((self.x, self.y - 1))
        if self.neigh(SOUTH) is not None and self.neigh(SOUTH).cellType == EMPTY:
            emptyNeigh.append((self.x, self.y + 1))
        if self.neigh(EAST) is not None and self.neigh(EAST).cellType == EMPTY:
            emptyNeigh.append((self.x + 1, self.y))
        if self.neigh(WEST) is not None and self.neigh(WEST).cellType == EMPTY:
            emptyNeigh.append((self.x - 1, self.y))
        return emptyNeigh


grid = {
    (0, 0): Cell(0, 0, EMPTY)
}

currentCell = grid[(0, 0)]
currentDestination = None
currentPath = []

def getNextDestination():
    unknownLocations = set()
    for pos, cell in grid.items():
        if cell.cellType == EMPTY:
            for unknownNeigh in cell.getUnknownNeighPosition():
                unknownLocations.add(unknownNeigh)
    assert len(unknownLocations) > 0
    byManhattan = lambda pos: manhattanDistance(currentCell.x, currentCell.y, pos[0], pos[1])
    return sorted(unknownLocations, key=byManhattan)[0]

def getPath(startPosition, destination):
    # breath-first algorithm (i think)
    # see all cells we can reach in 1 step, then 2 steps, etc.
    # I think this should give us the shortest path while being relatively simple?

    marked_from = {}
    nodesQueue = deque()
    nodesQueue.append(grid[startPosition])
    _current = None

    byManhattanToDestination = lambda pos: manhattanDistance(destination[0], destination[1], pos[0], pos[1])
    isNextToDest = lambda pos: abs(destination[0] - pos[0]) + abs(destination[1] - pos[1]) == 1

    while len(nodesQueue) > 0:
        _current = nodesQueue.popleft()

        if isNextToDest((_current.x, _current.y)):
            # return path by tracing back the marks
            path = [(_current.x, _current.y), destination]
            cur = (_current.x, _current.y)
            while cur != (startPosition[0], startPosition[1]):
                new = marked_from[cur]
                path.insert(0, new)
                cur = new
            return path[1:]

        emptyNeigh = sorted(_current.getEmptyNeighPosition(), key=byManhattanToDestination)
        for nPos in emptyNeigh:
            if nPos not in marked_from:
                marked_from[nPos] = (_current.x, _current.y)
                nodesQueue.append(grid[nPos])

    return None

def getNextDirection():
    assert currentPath and len(currentPath) > 0
    # If the next cell in the path is the current location, skip
    while currentPath[0] == (currentCell.x, currentCell.y):
        currentPath.pop(0)
    return currentPath.pop(0)

INPUT_MAP = {
    (-1, 0): WEST,
    (1, 0): EAST,
    (0, -1): NORTH,
    (0, 1): SOUTH,
}

def getNextInputCommand():
    global currentDestination
    global currentPath
    if not currentDestination:
        currentDestination = getNextDestination()
        print "\tNew destination", currentDestination
    if not currentPath:
        currentPosition = (currentCell.x, currentCell.y)
        currentPath = getPath(currentPosition, currentDestination)
        print "\tNew path", currentPath
    assert currentPath
    nextDir = getNextDirection()
    return INPUT_MAP[(nextDir[0] - currentCell.x, nextDir[1] - currentCell.y)]

def printGrid():
    min_x = min([p[0] for p in grid.keys()])
    max_x = max([p[0] for p in grid.keys()])
    min_y = min([p[1] for p in grid.keys()])
    max_y = max([p[1] for p in grid.keys()])

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (x, y) == (0, 0):
                print "S",
            elif (x, y) not in grid:
                print ' ',
            elif (x, y) == (currentCell.x, currentCell.y):
                print "R",
            elif grid[(x, y)].cellType == WALL:
                print "#",
            elif grid[(x, y)].cellType == EMPTY:
                print ".",
        print ""

while True:
    print "--"
    # printGrid()
    print "current cell", currentCell
    nextInput = getNextInputCommand()

    targetLocation = None
    if nextInput == NORTH:
        targetLocation = (currentCell.x, currentCell.y - 1)
    if nextInput == SOUTH:
        targetLocation = (currentCell.x, currentCell.y + 1)
    if nextInput == EAST:
        targetLocation = (currentCell.x + 1, currentCell.y)
    if nextInput == WEST:
        targetLocation = (currentCell.x - 1, currentCell.y)

    computer.inputs = [nextInput]
    print "in", computer.inputs
    
    computer.run()
    
    assert computer._waitingForInput
    print "out", computer.outputs
    out = computer.outputs.pop()
    assert len(computer.outputs) == 0

    if len(currentPath) > 0:
        assert out == EMPTY
    else:
        # New info!
        print "new cell discovered at", targetLocation, ". It's a ", out
        newCellLoc = targetLocation
        newCell = Cell(targetLocation[0], targetLocation[1], out)
        grid[targetLocation] = newCell
        currentDestination = None
        currentPath = []

    if out != WALL:
        print "(moved to", targetLocation, ")"
        currentCell = grid[targetLocation]
    else:
        print "(did not moved, blocked by a wall)"

    if out == GOAL:
        print "OH WOW"
        print currentCell.x, currentCell.y
        goalPosition = (currentCell.x, currentCell.y)
        break

bestPath = getPath((0, 0), goalPosition)
print bestPath, len(bestPath)

printGrid()